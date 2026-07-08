import { test, expect } from "./axe-helper";

test.describe("Public pages — WCAG 2.2 AA accessibility", () => {
    test("Home page (/)", async ({ page, runAccessibilityCheck }) => {
        await page.goto("/");
        await page.waitForLoadState("networkidle");
        await runAccessibilityCheck("home");
    });

    test("Search page (/search)", async ({ page, runAccessibilityCheck }) => {
        await page.goto("/search");
        await page.waitForLoadState("networkidle");
        await runAccessibilityCheck("search");
    });

    test("Report page (/report/)", async ({ page, runAccessibilityCheck }) => {
        await page.goto("/report/");
        await page.waitForLoadState("networkidle");
        await runAccessibilityCheck("report");
    });

    test("Login page (/auth/)", async ({ page, runAccessibilityCheck }) => {
        await page.goto("/auth/");
        await page.waitForLoadState("networkidle");
        await runAccessibilityCheck("login");
    });

    test("Password reset (/password_reset/)", async ({
        page,
        runAccessibilityCheck,
    }) => {
        await page.goto("/password_reset/");
        await page.waitForLoadState("networkidle");
        await runAccessibilityCheck("password-reset");
    });
});
