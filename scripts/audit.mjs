/**
 * Audit Lighthouse : mobile + desktop, sur le build de production.
 *
 * Usage :
 *   npm run audit            build, puis audite les deux formats
 *   npm run audit -- --fast  réutilise le dist existant (pas de rebuild)
 *
 * Sort en code 1 si une catégorie passe sous le seuil (voir CLAUDE.md : > 90).
 */
import lighthouse from "lighthouse";
import * as chromeLauncher from "chrome-launcher";
import desktopConfig from "lighthouse/core/config/desktop-config.js";
import { chromium } from "playwright";
import { spawn, execSync } from "node:child_process";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, "..");
const PORT = 4330;
const URL = `http://localhost:${PORT}/`;
const THRESHOLD = 90;

const CATEGORIES = [
  ["performance", "Performance"],
  ["accessibility", "Accessibilité"],
  ["best-practices", "Bonnes pratiques"],
  ["seo", "SEO"],
];

function killTree(pid) {
  if (!pid) return;
  try {
    if (process.platform === "win32") {
      execSync(`taskkill /pid ${pid} /T /F`, { stdio: "ignore" });
    } else {
      process.kill(-pid, "SIGKILL");
    }
  } catch {
    /* déjà terminé */
  }
}

function waitForUrl(child, timeoutMs = 60000) {
  return new Promise((resolve, reject) => {
    let buf = "";
    const timer = setTimeout(
      () => reject(new Error("Timeout : le serveur de preview n'a pas démarré")),
      timeoutMs
    );
    const onData = (chunk) => {
      buf += chunk.toString();
      if (/localhost:\d+/.test(buf)) {
        clearTimeout(timer);
        child.stdout.off("data", onData);
        resolve();
      }
    };
    child.stdout.on("data", onData);
  });
}

async function runLighthouse(formFactor, chromePort) {
  const isDesktop = formFactor === "desktop";
  const options = {
    port: chromePort,
    output: "json",
    logLevel: "error",
    onlyCategories: CATEGORIES.map(([id]) => id),
  };
  const result = await lighthouse(URL, options, isDesktop ? desktopConfig : undefined);
  return result.lhr;
}

function formatScore(score) {
  const pct = Math.round(score * 100);
  const mark = pct >= THRESHOLD ? "OK   " : "ECHEC";
  return { pct, mark };
}

async function main() {
  const fast = process.argv.includes("--fast");

  if (!fast || !existsSync(path.join(ROOT, "dist"))) {
    console.log("Build de production...");
    execSync("npm run build", { cwd: ROOT, stdio: "inherit" });
  }

  const npmCmd = process.platform === "win32" ? "npm.cmd" : "npm";
  const preview = spawn(npmCmd, ["run", "preview", "--", "--port", String(PORT)], {
    cwd: ROOT,
    stdio: "pipe",
    shell: true,
  });
  preview.stderr.on("data", (d) => process.stderr.write(`[preview] ${d}`));

  let chrome;
  let failed = 0;

  try {
    await waitForUrl(preview);
    console.log(`Preview prêt sur ${URL}\n`);

    // Lighthouse s'appuie sur chrome-launcher, qui cherche un Chrome système.
    // On lui donne le Chromium déjà installé pour Playwright.
    chrome = await chromeLauncher.launch({
      chromePath: chromium.executablePath(),
      chromeFlags: ["--headless=new", "--no-sandbox"],
    });

    // Chauffe : la toute première navigation d'un Chrome fraîchement lancé vers
    // un serveur qui vient de démarrer est systématiquement plus lente (caches
    // disque/serveur/polices froids), ce qui biaisait la mesure vers le pire
    // score plutôt qu'un chargement représentatif. On fait tourner Lighthouse
    // une première fois à blanc (résultat jeté) pour chauffer ce Chrome.
    console.log("Chauffe...");
    await runLighthouse("mobile", chrome.port);
    console.log("Chauffe effectuée\n");

    const rows = [];
    for (const formFactor of ["mobile", "desktop"]) {
      process.stdout.write(`Audit ${formFactor}... `);
      const lhr = await runLighthouse(formFactor, chrome.port);
      process.stdout.write("terminé\n");
      rows.push({ formFactor, lhr });
    }

    console.log("\n" + "=".repeat(58));
    console.log(`Lighthouse — seuil ${THRESHOLD}`);
    console.log("=".repeat(58));

    for (const { formFactor, lhr } of rows) {
      console.log(`\n${formFactor.toUpperCase()}`);
      for (const [id, label] of CATEGORIES) {
        const category = lhr.categories[id];
        if (!category || category.score === null) {
          console.log(`  ????   ---  ${label} (non évalué)`);
          continue;
        }
        const { pct, mark } = formatScore(category.score);
        if (pct < THRESHOLD) failed++;
        console.log(`  ${mark}  ${String(pct).padStart(3)}  ${label}`);
      }
    }

    console.log("\n" + "=".repeat(58));
    console.log(
      failed === 0
        ? `Les 8 scores atteignent ${THRESHOLD}.`
        : `${failed} score(s) sous ${THRESHOLD}.`
    );
  } finally {
    if (chrome) await chrome.kill();
    killTree(preview.pid);
  }

  process.exit(failed === 0 ? 0 : 1);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
