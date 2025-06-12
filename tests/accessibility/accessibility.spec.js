import { test, expect } from '@playwright/test';
import { AxeBuilder } from '@axe-core/playwright';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const pagesToTest = [
  '/', // Home page
  '/search', // Search page
  '/auth'
  // Add more URLs as needed
];

// Use import.meta.url to get the directory in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const reportDir = path.resolve(__dirname, '../../test-results/axe');

// Use async fs for compatibility
async function ensureDir(dir) {
  try {
    await fs.mkdir(dir, { recursive: true });
  } catch {
    // Directory already exists or cannot be created; ignore error
  }
}

for (const url of pagesToTest) {
  test(`Accessibility check for ${url}`, async ({ page }) => {
    await ensureDir(reportDir);
    await page.goto(`http://localhost:8002${url}`);
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();
    if (results.violations.length > 0) {
      const safeUrl = url.replace(/\W+/g, '_') || 'root';
      const reportPath = path.join(reportDir, `axe-report${safeUrl}.json`);
      await fs.writeFile(reportPath, JSON.stringify(results, null, 2));
      console.error(`‼️ Accessibility violations on ${url}:`);
      for (const violation of results.violations) {
        console.error(`- ${violation.id}: ${violation.description}`);
        for (const node of violation.nodes) {
          console.error(`  > Affected node: ${node.target.join(', ')}`);
          if (node.failureSummary) {
            console.error(`  >> Failure summary: ${node.failureSummary}`);
          }
          if (node.any.length > 0) {
            console.error(`  >>> Any issues: ${node.any.map(issue => issue.message).join(', ')}`);
          }
        }
      }
      throw new Error(`Accessibility violations found on ${url}. See report: ${reportPath}`);
    }
    expect(results.violations.length).toEqual(0);
  });
}
