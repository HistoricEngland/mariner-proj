import { defineConfig, devices } from "@playwright/test";

const baseURL = process.env.AXE_BASE_URL || "http://localhost:8002";

export default defineConfig({
    testDir: "./tests/accessibility",
    testMatch: "**/*.spec.ts",
    fullyParallel: false,
    retries: 0,
    workers: 1,
    timeout: 60_000,
    expect: {
        timeout: 10_000,
    },
    reporter: [
        ["list"],
        ["html", { outputFolder: "test-results/axe/html-report", open: "never" }],
        ["junit", { outputFile: "test-results/axe/results.xml" }],
    ],
    globalSetup: "./tests/accessibility/global-setup.ts",
    use: {
        baseURL,
        ignoreHTTPSErrors: true,
        screenshot: "only-on-failure",
        trace: "retain-on-failure",
    },
    projects: [
        {
            name: "public",
            testMatch: "public-pages.spec.ts",
            use: {
                ...devices["Desktop Chrome"],
            },
        },
        {
            name: "authenticated",
            testMatch: "authenticated-pages.spec.ts",
            use: {
                ...devices["Desktop Chrome"],
                storageState: "test-results/axe/.auth-state.json",
            },
        },
    ],
});
