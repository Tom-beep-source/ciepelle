// Chaque photo de public/images/ existe en deux largeurs : `nom.webp` (1920px max)
// et `nom-960.webp`. On construit le srcset par convention pour que le navigateur
// télécharge la variante adaptée au slot d'affichage (gain Lighthouse).
//
// `extraWidths` permet d'ajouter des paliers ponctuels (ex: `about-1280.webp`)
// pour les images chargées tôt sur mobile, où l'écart entre 960 et 1920 force
// le navigateur à choisir la variante 1920 sur les DPR élevés (>2), au prix du
// score Lighthouse mobile. Le fichier `nom-{largeur}.webp` correspondant doit
// exister.

const RESPONSIVE_WIDTHS = [960, 1920];

/** "/images/gallery-1.webp" -> "/images/gallery-1-960.webp 960w, /images/gallery-1.webp 1920w" */
export function buildSrcSet(src: string, extraWidths: number[] = []): string {
  const ext = src.slice(src.lastIndexOf("."));
  const base = src.slice(0, src.lastIndexOf("."));
  const widths = [...RESPONSIVE_WIDTHS, ...extraWidths].sort((a, b) => a - b);
  const maxW = Math.max(...widths);

  return widths
    .map((w) => (w === maxW ? `${base}${ext} ${w}w` : `${base}-${w}${ext} ${w}w`))
    .join(", ");
}
