import { test as base, type Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { createHtmlReport } from "axe-html-reporter";
import * as fs from "fs";
import * as path from "path";

const AXE_OUTPUT_DIR = path.resolve("test-results/axe");
const VIOLATION_THRESHOLD = parseInt(
    process.env.AXE_VIOLATION_THRESHOLD ?? "0",
    10,
);

/** WCAG 2.2 AA axe-core rule tags */
const WCAG_TAGS = ["wcag2a", "wcag2aa", "wcag22aa"];

export interface AccessibilityFixtures {
    runAccessibilityCheck: (pageName: string) => Promise<void>;
}

/**
 * Extended Playwright test fixture that provides `runAccessibilityCheck`.
 *
 * Usage in a spec:
 *   import { test } from "../accessibility/axe-helper";
 *   test("my page", async ({ page, runAccessibilityCheck }) => {
 *       await page.goto("/my-page");
 *       await runAccessibilityCheck("my-page");
 *   });
 */
export const test = base.extend<AccessibilityFixtures>({
    runAccessibilityCheck: async ({ page }, use) => {
        const check = async (pageName: string) => {
            await runAccessibilityCheck(page, pageName);
        };
        await use(check);
    },
});

export { expect } from "@playwright/test";

/**
 * Run axe-core analysis on the current page state and assert against the
 * configured violation threshold.
 */
export async function runAccessibilityCheck(
    page: Page,
    pageName: string,
): Promise<void> {
    const results = await new AxeBuilder({ page })
        .withTags(WCAG_TAGS)
        .analyze();

    // Ensure output directory exists
    fs.mkdirSync(AXE_OUTPUT_DIR, { recursive: true });

    // Write per-page JSON results
    const safePageName = pageName.replace(/[^a-z0-9_-]/gi, "_");
    const jsonPath = path.join(AXE_OUTPUT_DIR, `${safePageName}.json`);
    fs.writeFileSync(jsonPath, JSON.stringify(results, null, 2));

    // Generate per-page HTML report
    const htmlPath = path.join(AXE_OUTPUT_DIR, `${safePageName}.html`);
    createHtmlReport({
        results,
        options: {
            outputDirPath: AXE_OUTPUT_DIR,
            reportFileName: `${safePageName}.html`,
        },
    });

    const violationCount = results.violations.length;

    // Always log violations for visibility
    if (violationCount > 0) {
        console.log(
            `\n--- Accessibility violations for "${pageName}" (${violationCount}) ---`,
        );
        for (const violation of results.violations) {
            console.log(
                `  [${violation.impact?.toUpperCase()}] ${violation.id}: ${violation.help}`,
            );
            console.log(`    WCAG: ${violation.tags.join(", ")}`);
            console.log(`    Help: ${violation.helpUrl}`);
            for (const node of violation.nodes) {
                console.log(`    Target: ${node.target.join(", ")}`);
                if (node.failureSummary) {
                    console.log(`    Fix: ${node.failureSummary}`);
                }
            }
        }
        console.log("---\n");
    }

    // Apply threshold logic
    if (violationCount > VIOLATION_THRESHOLD) {
        throw new Error(
            `Accessibility check failed for "${pageName}": ` +
                `${violationCount} violation(s) found, threshold is ${VIOLATION_THRESHOLD}. ` +
                `See ${jsonPath} and ${htmlPath} for details.`,
        );
    } else if (violationCount > 0) {
        console.log(
            `⚠ "${pageName}": ${violationCount} violation(s) within threshold (${VIOLATION_THRESHOLD}). Passing with warnings.`,
        );
    } else {
        console.log(`✓ "${pageName}": No accessibility violations found.`);
    }
}
