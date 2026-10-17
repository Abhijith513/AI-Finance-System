import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";

const root = process.env.DEMO_URL || "http://127.0.0.1:5173";
const password = process.env.DEMO_PRESENTER_PASSWORD;
if (!password) throw new Error("DEMO_PRESENTER_PASSWORD is required");
const evidenceDir = path.resolve(process.env.DEMO_EVIDENCE_DIR || "evidence/browser");
fs.mkdirSync(evidenceDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
const log = { started: new Date().toISOString(), steps: [], url: root, pass: false };
try {
  await page.goto(root, { waitUntil: "domcontentloaded", timeout: 30000 });
  await page.getByRole("heading", { name: "AI Finance System" }).waitFor({ timeout: 30000 });
  await page.screenshot({ path: path.join(evidenceDir, "01-login.png"), fullPage: true });
  await page.getByLabel("Username").fill("demo_presenter");
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await page.getByRole("heading", { name: "One transaction. Eight verified steps." }).waitFor({ timeout: 30000 });
  await page.screenshot({ path: path.join(evidenceDir, "02-presenter-ready.png"), fullPage: true });
  await page.getByRole("button", { name: "Start timed demonstration" }).click();
  // Both model evaluations run against the *real* 50k synthetic records.
  await page.getByRole("status").filter({ hasText: "Demo complete — 8/8" }).waitFor({ timeout: 1200000 });
  const stepRows = await page.locator(".demo-step").all();
  for (const row of stepRows) {
    const title = await row.locator("h2").innerText();
    const detail = await row.locator("p").innerText();
    const status = await row.locator("strong").innerText();
    if (!status.startsWith("pass")) throw new Error("Failed step " + title + ": " + status);
    log.steps.push({ title, detail, status });
  }
  if (stepRows.length !== 8) throw new Error("Expected exactly eight verified steps");
  const runtime = await page.locator(".demo-timer strong").innerText();
  log.elapsed_time = runtime;
  await page.screenshot({ path: path.join(evidenceDir, "03-live-end-to-end-success.png"), fullPage: true });
  await page.getByRole("button", { name: "Analytics dashboard" }).click();
  await page.getByRole("heading", { name: "Banking analytics dashboard" }).waitFor({ timeout: 1200000 });
  await page.screenshot({ path: path.join(evidenceDir, "04-analytics-dashboard.png"), fullPage: true });
  await page.getByRole("button", { name: "Guided demo" }).click();
  await page.getByText("Verified transaction evidence").waitFor({ timeout: 30000 });
  await page.getByText("Show management report").click();
  await page.screenshot({ path: path.join(evidenceDir, "05-management-report.png"), fullPage: true });
  await page.getByRole("button", { name: "Sign out" }).click();
  await page.getByRole("button", { name: "Sign in", exact: true }).waitFor({ timeout: 30000 });
  await page.screenshot({ path: path.join(evidenceDir, "06-signed-out.png"), fullPage: true });
  log.pass = true;
  console.log("BROWSER DEMO PASS: 8/8 steps; " + runtime);
} catch (error) {
  log.error = String(error);
  await page.screenshot({ path: path.join(evidenceDir, "failure.png"), fullPage: true }).catch(() => {});
  throw error;
} finally {
  log.finished = new Date().toISOString();
  fs.writeFileSync(path.join(evidenceDir, "demo-log.json"), JSON.stringify(log, null, 2));
  await browser.close();
}
