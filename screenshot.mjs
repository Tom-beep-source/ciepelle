import { chromium } from "playwright";
import { AxeBuilder } from "@axe-core/playwright";
import { spawn, execSync } from "node:child_process";
import { mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT_DIR = path.join(__dirname, ".screenshots");

const VIEWPORTS = [
  { name: "desktop", width: 1440, height: 900 },
  { name: "mobile", width: 390, height: 844 },
];

mkdirSync(OUT_DIR, { recursive: true });

function killProcessTree(pid) {
  if (!pid) return;
  try {
    if (process.platform === "win32") {
      execSync(`taskkill /pid ${pid} /T /F`, { stdio: "ignore" });
    } else {
      process.kill(-pid, "SIGKILL");
    }
  } catch {
    // process may already be gone
  }
}

/**
 * Force le déclenchement des images en loading="lazy" avant capture.
 * Sans ça, une capture fullPage photographie des emplacements vides : le
 * défilement déclenche bien le chargement, mais la capture n'attend pas la fin.
 * (Lenis n'intercepte pas scrollTo ici : le contexte est en reducedMotion.)
 */
async function loadLazyImages(page) {
  await page.evaluate(async () => {
    await new Promise((resolve) => {
      let y = 0;
      const step = () => {
        window.scrollTo(0, y);
        y += window.innerHeight;
        if (y < document.body.scrollHeight) {
          setTimeout(step, 100);
        } else {
          window.scrollTo(0, 0);
          resolve();
        }
      };
      step();
    });
  });

  // On ignore les <img> sans source (ex. la cible vide de la lightbox), qui
  // n'atteignent jamais naturalWidth > 0.
  await page.waitForFunction(
    () =>
      Array.from(document.images)
        .filter((i) => i.getAttribute("src"))
        .every((i) => i.complete && i.naturalWidth > 0),
    null,
    { timeout: 15000 }
  );
}

/**
 * Audit d'accessibilité axe-core sur la page telle qu'elle est rendue.
 * Renvoie le nombre de violations, et les détaille sur la sortie standard.
 */
async function runAxeAudit(page, label) {
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "best-practice"])
    .analyze();

  const violations = results.violations;

  if (violations.length === 0) {
    console.log(`  axe-core (${label}) : aucune violation`);
    return 0;
  }

  console.log(`  axe-core (${label}) : ${violations.length} type(s) de violation`);
  for (const v of violations) {
    console.log(`    [${v.impact ?? "n/a"}] ${v.id} — ${v.help}`);
    console.log(`      ${v.helpUrl}`);
    for (const node of v.nodes.slice(0, 3)) {
      console.log(`      · ${node.target.join(" ")}`);
      // Le message de axe précise la valeur fautive (ratio de contraste, etc.)
      const detail = [...node.any, ...node.all, ...node.none][0];
      if (detail?.message) console.log(`        ${detail.message}`);
    }
    if (v.nodes.length > 3) {
      console.log(`      · … et ${v.nodes.length - 3} autre(s) occurrence(s)`);
    }
  }
  return violations.length;
}

/** Résout dès que l'URL du serveur dev apparaît dans stdout, ex: "Local  http://localhost:4321/" */
function waitForServerUrl(devServer, timeoutMs = 30000) {
  return new Promise((resolve, reject) => {
    let buffer = "";
    const timer = setTimeout(() => {
      reject(new Error("Timed out waiting for dev server URL"));
    }, timeoutMs);

    const onData = (chunk) => {
      buffer += chunk.toString();
      const match = buffer.match(/http:\/\/localhost:(\d+)\//);
      if (match) {
        clearTimeout(timer);
        devServer.stdout.off("data", onData);
        resolve(`http://localhost:${match[1]}/`);
      }
    };

    devServer.stdout.on("data", onData);
  });
}

async function main() {
  const npmCmd = process.platform === "win32" ? "npm.cmd" : "npm";
  const devServer = spawn(npmCmd, ["run", "dev"], {
    cwd: __dirname,
    stdio: "pipe",
    shell: true,
  });

  devServer.stdout.on("data", (d) => process.stdout.write(`[dev] ${d}`));
  devServer.stderr.on("data", (d) => process.stderr.write(`[dev] ${d}`));

  let totalViolations = 0;

  try {
    const url = await waitForServerUrl(devServer);
    console.log(`Dev server ready at ${url}, launching browser...`);

    const browser = await chromium.launch();

    for (const viewport of VIEWPORTS) {
      // Contexte explicite : @axe-core/playwright refuse une page issue de
      // browser.newPage(), il lui faut un contexte propre.
      const context = await browser.newContext({
        viewport: { width: viewport.width, height: viewport.height },
        reducedMotion: "reduce", // évite de capturer les animations GSAP en plein vol
      });
      const page = await context.newPage();
      await page.goto(url, { waitUntil: "networkidle" });
      await loadLazyImages(page);
      await page.waitForTimeout(500); // laisse le rendu se stabiliser après le retour en haut

      const fullPagePath = path.join(OUT_DIR, `${viewport.name}-full.png`);
      await page.screenshot({ path: fullPagePath, fullPage: true });
      console.log(`Saved ${fullPagePath}`);

      const viewportPath = path.join(OUT_DIR, `${viewport.name}-viewport.png`);
      await page.screenshot({ path: viewportPath, fullPage: false });
      console.log(`Saved ${viewportPath}`);

      totalViolations += await runAxeAudit(page, viewport.name);

      await page.close();
      await context.close();
    }

    await browser.close();
  } finally {
    killProcessTree(devServer.pid);
  }

  if (totalViolations > 0) {
    console.log(
      `\n${totalViolations} violation(s) d'accessibilité au total — voir le détail ci-dessus.`
    );
    process.exitCode = 1;
  } else {
    console.log("\nAccessibilité : aucune violation sur les deux formats.");
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
