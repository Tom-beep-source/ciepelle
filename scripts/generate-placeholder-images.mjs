/**
 * Génère des visuels provisoires (aplats de couleur + motif géométrique
 * discret) pour remplacer les photos tant qu'elles ne sont pas fournies par
 * le commerçant. Les couleurs et le nom/ville du commerce sont lus dans
 * src/config.ts pour rester valables après changement de palette client —
 * aucune donnée métier codée en dur ici.
 *
 * Usage : node scripts/generate-placeholder-images.mjs
 *
 * Régénère TOUTES les images listées dans `business.logo`, `media`,
 * `menu[].image`, `gallery` et `seo.ogImage` — y compris le logo, un
 * monogramme généré à partir des initiales du commerce (jamais de nom en
 * toutes lettres, contrairement à un ancien logo client resté en dur dans
 * public/images/logo.svg). Une image réelle fournie par le commerçant doit
 * être réintégrée après coup : ce script écrase sans confirmation.
 */
import sharp from "sharp";
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, "..");
const PUBLIC_DIR = path.join(ROOT, "public");
const fullConfigSrc = readFileSync(path.join(ROOT, "src/config.ts"), "utf8");
// On ne garde que l'objet `siteConfig` (à partir de sa déclaration) : les
// interfaces TypeScript au-dessus contiennent les mêmes noms de clés
// (ex. "business: {") sans valeurs entre guillemets, ce qui fausserait
// l'extraction si on les incluait.
const configSrc = fullConfigSrc.slice(fullConfigSrc.indexOf("export const siteConfig"));

// ----------------------------------------------------------------------------
// Lecture minimale de config.ts (même approche que scripts/check-contrast.mjs :
// on ne peut pas `import` un .ts depuis un script Node brut sans ajouter un
// loader, donc on extrait par regex plutôt que d'ajouter une dépendance).
// ----------------------------------------------------------------------------

/** Renvoie le contenu d'un bloc `key: { ... }` ou `key: [ ... ]`, bornes incluses. */
function findBlock(src, key) {
  const startMatch = src.match(new RegExp(`\\b${key}:\\s*[{[]`));
  if (!startMatch) throw new Error(`Bloc "${key}" introuvable dans config.ts`);
  const openChar = startMatch[0].endsWith("{") ? "{" : "[";
  const closeChar = openChar === "{" ? "}" : "]";
  const start = startMatch.index + startMatch[0].length - 1;
  let depth = 0;
  for (let i = start; i < src.length; i++) {
    if (src[i] === openChar) depth++;
    else if (src[i] === closeChar) {
      depth--;
      if (depth === 0) return src.slice(start, i + 1);
    }
  }
  throw new Error(`Bloc "${key}" non refermé dans config.ts`);
}

function findString(src, key) {
  const m = src.match(new RegExp(`${key}:\\s*"([^"]*)"`));
  if (!m) throw new Error(`Champ "${key}" introuvable`);
  return m[1];
}

function findAllStrings(src, key) {
  return [...src.matchAll(new RegExp(`${key}:\\s*"([^"]*)"`, "g"))].map((m) => m[1]);
}

const businessBlock = findBlock(configSrc, "business");
const businessName = findString(businessBlock, "name");
// logo est optionnel dans SiteConfig — retombe sur le chemin par défaut du
// template si le champ est absent plutôt que d'échouer comme findString.
const logoMatch = businessBlock.match(/logo:\s*"([^"]*)"/);
const logoPath = logoMatch ? logoMatch[1] : "/images/logo.svg";

const contactBlock = findBlock(configSrc, "contact");
const addressBlock = findBlock(contactBlock, "address");
const city = findString(addressBlock, "city");

const colorsBlock = findBlock(findBlock(configSrc, "theme"), "colors");
const colors = {
  primary: findString(colorsBlock, "primary"),
  secondary: findString(colorsBlock, "secondary"),
  accent: findString(colorsBlock, "accent"),
  background: findString(colorsBlock, "background"),
  text: findString(colorsBlock, "text"),
};

const mediaBlock = findBlock(configSrc, "media");
const heroImage = findString(mediaBlock, "heroImage");
const heroImageMobile = findString(mediaBlock, "heroImageMobile");
const aboutImage = findString(mediaBlock, "aboutImage");

const menuBlock = findBlock(configSrc, "menu");
const menuImages = findAllStrings(menuBlock, "image");

const galleryBlock = findBlock(configSrc, "gallery");
const galleryImages = findAllStrings(galleryBlock, "src");

const seoBlock = findBlock(configSrc, "seo");
const ogImage = findString(seoBlock, "ogImage");

// ----------------------------------------------------------------------------
// Génération SVG -> raster
// ----------------------------------------------------------------------------

function escapeXml(str) {
  return str.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&apos;" }[c]));
}

/** Aplat de couleur + fines diagonales — motif sobre et discret, cohérent d'un visuel à l'autre. */
function patternSvg({ width, height, bg, fg, spacing = 26 }) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    <defs>
      <pattern id="p" width="${spacing}" height="${spacing}" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
        <line x1="0" y1="0" x2="0" y2="${spacing}" stroke="${fg}" stroke-width="1.4" stroke-opacity="0.16" />
      </pattern>
    </defs>
    <rect width="${width}" height="${height}" fill="${bg}" />
    <rect width="${width}" height="${height}" fill="url(#p)" />
  </svg>`;
}

/** Taille de police qui garde `text` dans `maxWidth`, entre `min` et `max` px. */
function fitFontSize(text, maxWidth, max, min) {
  const AVG_CHAR_WIDTH_RATIO = 0.58; // approximation sans-serif gras
  let size = max;
  while (size > min && text.length * size * AVG_CHAR_WIDTH_RATIO > maxWidth) size -= 2;
  return size;
}

/** Image de partage (OG) : fond uni + motif discret + nom et ville du commerce. */
function ogImageSvg({ width, height, bg, fg, textColor, accentColor, name, city }) {
  const padding = 96;
  const contentWidth = width - padding * 2;
  const nameSize = fitFontSize(name, contentWidth, 76, 36);
  const citySize = Math.round(nameSize * 0.42);
  const nameY = height / 2;
  const cityY = nameY + nameSize * 0.75;
  const ruleY = nameY - nameSize * 1.1;

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    <defs>
      <pattern id="p" width="30" height="30" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
        <line x1="0" y1="0" x2="0" y2="30" stroke="${fg}" stroke-width="1.4" stroke-opacity="0.12" />
      </pattern>
    </defs>
    <rect width="${width}" height="${height}" fill="${bg}" />
    <rect width="${width}" height="${height}" fill="url(#p)" />
    <rect x="${padding}" y="${ruleY}" width="64" height="4" fill="${accentColor}" />
    <text x="${padding}" y="${nameY}" font-family="Arial, Helvetica, sans-serif" font-weight="700" font-size="${nameSize}" fill="${textColor}">${escapeXml(name)}</text>
    <text x="${padding}" y="${cityY}" font-family="Arial, Helvetica, sans-serif" font-weight="400" font-size="${citySize}" fill="${textColor}" opacity="0.85">${escapeXml(city)}</text>
  </svg>`;
}

/** Initiales du monogramme : deux premiers mots du nom, ou deux premières lettres s'il est composé d'un seul mot. */
function getInitials(name) {
  const words = name.trim().split(/\s+/).filter(Boolean);
  if (words.length === 1) return words[0].slice(0, 2).toUpperCase();
  return (words[0][0] + words[1][0]).toUpperCase();
}

/** Monogramme générique (initiales du commerce) — jamais de nom en toutes lettres, pour rester valable client après client. */
function logoSvg({ name, bg, fg }) {
  const initials = getInitials(name);
  const fontSize = initials.length > 1 ? 20 : 26;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">
    <rect width="48" height="48" rx="8" fill="${bg}"/>
    <text x="24" y="31" text-anchor="middle" font-family="serif" font-size="${fontSize}" fill="${fg}">${escapeXml(initials)}</text>
  </svg>`;
}

function variantPath(basePath, suffix) {
  const ext = basePath.slice(basePath.lastIndexOf("."));
  const base = basePath.slice(0, basePath.lastIndexOf("."));
  return `${base}-${suffix}${ext}`;
}

async function writeWebp(relPath, svg) {
  const outPath = path.join(PUBLIC_DIR, relPath.replace(/^\//, ""));
  mkdirSync(path.dirname(outPath), { recursive: true });
  await sharp(Buffer.from(svg)).webp({ quality: 85 }).toFile(outPath);
  console.log(`  ${relPath}`);
}

async function writeJpeg(relPath, svg) {
  const outPath = path.join(PUBLIC_DIR, relPath.replace(/^\//, ""));
  mkdirSync(path.dirname(outPath), { recursive: true });
  await sharp(Buffer.from(svg)).jpeg({ quality: 88 }).toFile(outPath);
  console.log(`  ${relPath}`);
}

function writeSvg(relPath, svg) {
  const outPath = path.join(PUBLIC_DIR, relPath.replace(/^\//, ""));
  mkdirSync(path.dirname(outPath), { recursive: true });
  writeFileSync(outPath, svg, "utf8");
  console.log(`  ${relPath}`);
}

// Rotation de couples (fond, motif) puisés dans la palette du client — la
// galerie et les vignettes menu utilisent tour à tour ces combinaisons pour
// que les tuiles se distinguent sans jamais sortir de la palette.
const PAIRS = [
  [colors.secondary, colors.accent],
  [colors.primary, colors.background],
  [colors.accent, colors.secondary],
  [colors.text, colors.accent],
];

async function main() {
  console.log("Génération des visuels provisoires (aplats + motif géométrique)...\n");

  console.log("Logo :");
  writeSvg(logoPath, logoSvg({ name: businessName, bg: colors.primary, fg: colors.background }));

  console.log("Hero :");
  await writeWebp(heroImage, patternSvg({ width: 1920, height: 1080, bg: colors.secondary, fg: colors.accent }));
  await writeWebp(
    variantPath(heroImage, 960),
    patternSvg({ width: 960, height: 540, bg: colors.secondary, fg: colors.accent })
  );
  await writeWebp(
    heroImageMobile,
    patternSvg({ width: 1080, height: 1440, bg: colors.secondary, fg: colors.accent })
  );

  console.log("À propos :");
  await writeWebp(aboutImage, patternSvg({ width: 1920, height: 1440, bg: colors.primary, fg: colors.background }));
  await writeWebp(
    variantPath(aboutImage, 960),
    patternSvg({ width: 960, height: 720, bg: colors.primary, fg: colors.background })
  );
  await writeWebp(
    variantPath(aboutImage, 1280),
    patternSvg({ width: 1280, height: 960, bg: colors.primary, fg: colors.background })
  );

  console.log("Galerie :");
  for (const [i, image] of galleryImages.entries()) {
    const [bg, fg] = PAIRS[i % PAIRS.length];
    await writeWebp(image, patternSvg({ width: 1920, height: 1440, bg, fg }));
    await writeWebp(variantPath(image, 960), patternSvg({ width: 960, height: 720, bg, fg }));
  }

  console.log("Vignettes produits :");
  for (const [i, image] of menuImages.entries()) {
    const [bg, fg] = PAIRS[(i + 1) % PAIRS.length]; // décalage pour ne pas répéter l'ordre de la galerie
    await writeWebp(image, patternSvg({ width: 320, height: 320, bg, fg, spacing: 18 }));
  }

  console.log("Image de partage (OG) :");
  await writeJpeg(
    ogImage,
    ogImageSvg({
      width: 1200,
      height: 630,
      bg: colors.secondary,
      fg: colors.accent,
      textColor: colors.background,
      accentColor: colors.accent,
      name: businessName,
      city,
    })
  );

  console.log("\nTerminé. Ces visuels sont provisoires : à remplacer par les photos réelles du commerce.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
