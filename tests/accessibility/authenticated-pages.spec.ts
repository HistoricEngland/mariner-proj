import { test, expect } from "./axe-helper";
import * as fs from "fs";
import * as path from "path";

const AUTH_STATE_PATH = path.resolve("test-results/axe/.auth-state.json");
const authStateAvailable = fs.existsSync(AUTH_STATE_PATH);

test.describe("Authenticated pages — WCAG 2.2 AA accessibility", () => {
    test.skip(!authStateAvailable, "Authentication state not available — provide AXE_USERNAME and AXE_PASSWORD env vars to enable.");

    test("Resource list (/resource/)", async ({
        page,
        runAccessibilityCheck,
    }) => {
        await page.goto("/resource/");
        await page.waitForLoadState("networkidle");
        await runAccessibilityCheck("resource-list");
    });

    test("Edit history (/resource/history/)", async ({
        page,
        runAccessibilityCheck,
    }) => {
        await page.goto("/resource/history/");
        await page.waitForLoadState("networkidle");
        await runAccessibilityCheck("resource-history");
    });

    test("Graph list (/graph/)", async ({ page, runAccessibilityCheck }) => {
        await page.goto("/graph/");
        await page.waitForLoadState("networkidle");
        await runAccessibilityCheck("graph-list");
    });

    test("Reference data manager (/rdm)", async ({
        page,
        runAccessibilityCheck,
    }) => {
        await page.goto("/rdm");
        await page.waitForLoadState("networkidle");
        await runAccessibilityCheck("rdm");
    });

    test("User profile (/user/)", async ({ page, runAccessibilityCheck }) => {
        await page.goto("/user/");
        await page.waitForLoadState("networkidle");
        await runAccessibilityCheck("user-profile");
    });

    test("System settings (/settings/)", async ({
        page,
        runAccessibilityCheck,
    }) => {
        await page.goto("/settings/");
        await page.waitForLoadState("networkidle");
        await runAccessibilityCheck("system-settings");
    });
});
