/**
 * Génère un QR code imprimable (SVG + PNG haute résolution) à partir d'une
 * URL, sans dépendre d'un service tiers : génération locale (bibliothèque
 * `qrcode`), aucune redirection, aucun compte — le QR encode directement
 * l'URL finale.
 *
 * Usage : npm run qr -- <url> <fichier-de-sortie-sans-extension>
 * Exemple : npm run qr -- https://exemple.fr/allergenes/ public/images/qr-allergenes
 *
 * Écrit <fichier-de-sortie>.svg (vectoriel, net à toute taille d'impression)
 * et <fichier-de-sortie>.png (2000px, haute résolution pour impression).
 */
import QRCode from "qrcode";
import path from "node:path";
import { mkdirSync } from "node:fs";

const [, , url, outFile] = process.argv;

if (!url || !outFile) {
  console.error("Usage : npm run qr -- <url> <fichier-de-sortie-sans-extension>");
  console.error("Exemple : npm run qr -- https://exemple.fr/allergenes/ public/images/qr-allergenes");
  process.exit(1);
}

// Niveau H (~30% de correction d'erreur) : le QR reste scannable même
// partiellement abîmé, sali ou recouvert (usage comptoir/boutique).
// margin: 4 modules blancs = zone de silence minimale recommandée par la
// norme ISO/IEC 18004, nécessaire pour que les lecteurs détectent le code.
const options = {
  errorCorrectionLevel: "H",
  margin: 4,
  color: { dark: "#000000", light: "#FFFFFF" },
};

const base = outFile.replace(/\.(svg|png)$/i, "");
const svgPath = `${base}.svg`;
const pngPath = `${base}.png`;

const dir = path.dirname(base);
if (dir && dir !== ".") mkdirSync(dir, { recursive: true });

await QRCode.toFile(svgPath, url, { ...options, type: "svg" });
await QRCode.toFile(pngPath, url, { ...options, type: "png", width: 2000 });

console.log(`QR code généré pour : ${url}`);
console.log(`  ${svgPath}`);
console.log(`  ${pngPath}`);
