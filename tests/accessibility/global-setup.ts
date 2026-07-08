import { chromium, type FullConfig } from "@playwright/test";
import * as fs from "fs";
import * as path from "path";

const AUTH_STATE_PATH = path.resolve("test-results/axe/.auth-state.json");

/**
 * Global setup that authenticates against the Arches login page and persists
 * the browser storage state for reuse across authenticated test specs.
 *
 * Credentials are read from environment variables:
 *   AXE_USERNAME  (default: "admin")
 *   AXE_PASSWORD  (default: "admin")
 *
 * If AXE_SKIP_AUTH is set to "true", authentication is skipped and only
 * public-page tests will run.
 */
async function globalSetup(config: FullConfig): Promise<void> {
    const skipAuth = process.env.AXE_SKIP_AUTH === "true";
    if (skipAuth) {
        console.log(
            "AXE_SKIP_AUTH=true — skipping authentication setup. Authenticated tests will be skipped.",
        );
        if (fs.existsSync(AUTH_STATE_PATH)) {
            fs.unlinkSync(AUTH_STATE_PATH);
        }
        return;
    }

    const username = process.env.AXE_USERNAME || "admin";
    const password = process.env.AXE_PASSWORD || "admin";
    const baseURL =
        process.env.AXE_BASE_URL ||
        config.projects[0]?.use?.baseURL ||
        "http://localhost:8002";

    console.log(`Authenticating as "${username}" against ${baseURL}/auth/ …`);

    const browser = await chromium.launch();
    const context = await browser.newContext({ ignoreHTTPSErrors: true });
    const page = await context.newPage();

    try {
        // Navigate to login page to get CSRF token
        const loginResponse = await page.goto(`${baseURL}/auth/`, {
            waitUntil: "networkidle",
        });

        if (!loginResponse || !loginResponse.ok()) {
            throw new Error(
                `Failed to load login page: ${loginResponse?.status()} ${loginResponse?.statusText()}`,
            );
        }

        // Extract CSRF token from cookie or hidden field
        const csrfToken = await page
            .locator('input[name="csrfmiddlewaretoken"]')
            .getAttribute("value");

        if (!csrfToken) {
            throw new Error("Could not extract CSRF token from login form.");
        }

        // Fill and submit the login form using accessible label selectors
        await page.getByLabel("Username").fill(username);
        await page.getByLabel("Password").fill(password);
        await page.getByRole("button", { name: "Sign in" }).click();

        // Wait for either a successful redirect OR the login failure alert
        const result = await Promise.race([
            page
                .waitForURL(
                    (url) => !url.pathname.includes("/auth"),
                    { timeout: 15_000 },
                )
                .then(() => "success" as const),
            page
                .locator("#login-failed-alert[style*='display:block'], #login-failed-alert[style*='display: block']")
                .waitFor({ state: "attached", timeout: 15_000 })
                .then(() => "login-failed" as const),
        ]);

        if (result === "login-failed") {
            const message = await page
                .locator("#login-fail-message")
                .textContent();
            throw new Error(
                `Login rejected by server: ${message?.trim() || "Invalid username and/or password."}`,
            );
        }

        // Verify we're no longer on the login page
        const currentURL = page.url();
        if (currentURL.includes("/auth")) {
            throw new Error(
                `Still on login page after submit. URL: ${currentURL}. ` +
                    "Check that AXE_USERNAME and AXE_PASSWORD are correct.",
            );
        }

        console.log(`Authentication successful. Redirected to: ${currentURL}`);

        // Ensure output directory exists
        fs.mkdirSync(path.dirname(AUTH_STATE_PATH), { recursive: true });

        // Save storage state for authenticated tests
        await context.storageState({ path: AUTH_STATE_PATH });
    } catch (error) {
        console.error("Authentication failed:", error);
        console.error(
            "Authenticated page tests will be skipped. " +
                "Ensure AXE_USERNAME and AXE_PASSWORD are set correctly, " +
                "or set AXE_SKIP_AUTH=true to suppress this warning.",
        );
        // Remove any stale auth state so authenticated tests get skipped
        if (fs.existsSync(AUTH_STATE_PATH)) {
            fs.unlinkSync(AUTH_STATE_PATH);
        }
    } finally {
        await browser.close();
    }
}

export default globalSetup;
