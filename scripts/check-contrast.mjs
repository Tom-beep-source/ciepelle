/**
 * Vérifie que les couples de couleurs du site atteignent le contraste WCAG AA.
 * Les couleurs sont lues depuis src/config.ts pour rester valables après
 * changement de palette client.
 *
 * Usage : node scripts/check-contrast.mjs
 * Sort en code 1 si un couple échoue.
 */
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const configSrc = readFileSync(path.join(__dirname, "../src/config.ts"), "utf8");

function readColor(key) {
  const m = configSrc.match(new RegExp(`${key}:\\s*"(#[0-9A-Fa-f]{6})"`));
  if (!m) throw new Error(`Couleur introuvable dans config.ts : ${key}`);
  return m[1];
}

const COLORS = {
  background: readColor("background"),
  text: readColor("text"),
  primary: readColor("primary"),
  secondary: readColor("secondary"),
  accent: readColor("accent"),
  white: "#FFFFFF",
};

const toRgb = (hex) => {
  const i = parseInt(hex.slice(1), 16);
  return [(i >> 16) & 255, (i >> 8) & 255, i & 255];
};

/** Aplatit une couleur semi-transparente sur son fond (ce que voit l'œil). */
const composite = (fg, bg, alpha) =>
  fg.map((c, i) => Math.round(c * alpha + bg[i] * (1 - alpha)));

const luminance = (rgb) => {
  const [r, g, b] = rgb.map((c) => {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};

const ratio = (a, b) => {
  const [l1, l2] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (l1 + 0.05) / (l2 + 0.05);
};

// [libellé, couleur de texte, opacité, couleur de fond, seuil]
// Seuil 3.0 pour le "grand texte" (>=24px, ou >=18.66px en gras) — WCAG 1.4.3.
const CHECKS = [
  ["Corps de texte", "text", 1, "background", 4.5],
  ["Description produit (70%)", "text", 0.7, "background", 4.5],
  ["Texte secondaire (75%)", "text", 0.75, "background", 4.5],
  ["Prix (100%)", "text", 1, "background", 4.5],
  ["Libellé colonne (ink/70)", "text", 0.7, "background", 4.5],
  ["Attribution carte (ink/70)", "text", 0.7, "background", 4.5],
  ["Avis (ink/80)", "text", 0.8, "background", 4.5],
  ["Copyright pied de page (white/70)", "white", 0.7, "secondary", 4.5],
  ["Coordonnées pied de page (white/80)", "white", 0.8, "secondary", 4.5],
  ["Lien primaire", "primary", 1, "background", 4.5],
  ["Texte sur bouton primaire", "white", 1, "primary", 4.5],
  ["Texte sur surface sombre", "white", 1, "secondary", 4.5],
  ["Pastille tag (texte secondary)", "secondary", 1, "background", 4.5],
  ["Bandeau horaires (secondary sur accent)", "secondary", 1, "accent", 4.5],
  ["Icône accessibilité (secondary/70)", "secondary", 0.7, "background", 3.0],
];

let failed = 0;
console.log("Contraste WCAG — seuil AA 4.5:1 (texte courant), 3.0:1 (grand texte//UI)\n");

for (const [label, fgKey, alpha, bgKey, threshold] of CHECKS) {
  const bg = toRgb(COLORS[bgKey]);
  const fg = alpha === 1 ? toRgb(COLORS[fgKey]) : composite(toRgb(COLORS[fgKey]), bg, alpha);
  const r = ratio(fg, bg);
  const ok = r >= threshold;
  if (!ok) failed++;
  console.log(
    `${ok ? "OK  " : "ECHEC"} ${r.toFixed(2).padStart(6)}:1  (min ${threshold})  ${label}`
  );
}

console.log(
  failed === 0 ? "\nTous les couples respectent le seuil." : `\n${failed} couple(s) en échec.`
);
process.exit(failed === 0 ? 0 : 1);
