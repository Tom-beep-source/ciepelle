# Images

## Visuels provisoires

Les photos de produits, la vitrine, l'intérieur, la galerie, l'image de
partage (OG) et le logo sont **provisoires** : ce sont des aplats de couleur
(motif géométrique discret) ou, pour le logo, un monogramme fait des
initiales du commerce, générés dans la palette du client (voir
`scripts/generate-placeholder-images.mjs`, `npm run placeholders`). Elles
doivent être remplacées par les photos réelles (et, si le commerçant en a un,
un vrai logo) avant livraison — voir `CLAUDE.md` § *Photos* pour les règles à
respecter (aucune enseigne ni texte de tiers visible, recadrage portrait
vérifié, lumière cohérente) ; un logo générique évite le même risque de fuite
qu'une photo de banque d'images (nom d'un client précédent laissé en dur).
**Ne jamais utiliser de banque d'images (Unsplash ou autre) comme visuel
provisoire** : le risque d'y laisser une enseigne ou un prix concurrent
visible est trop élevé, voir `NOUVEAU-CLIENT.md` §4.

Pour régénérer ces aplats après un changement de palette dans `config.ts`
(avant d'avoir les vraies photos) :

```bash
npm run placeholders
```

Le script lit `theme.colors`, `business.name` et `contact.address.city` dans
`src/config.ts` et écrase tous les fichiers listés dans `business.logo`,
`media`, `menu[].image`, `gallery` et `seo.ogImage`. Une fois une vraie photo
(ou un vrai logo) intégré manuellement, ne plus relancer le script sur ce
fichier précis (il écrase sans confirmation).

## Convention à respecter

Chaque photo existe en **deux largeurs** :

- `nom.webp` — 1920px maximum sur le plus grand côté
- `nom-960.webp` — variante 960px

`buildSrcSet()` (`src/lib/images.ts`) construit le `srcset` à partir de cette
convention. **Si vous ajoutez une photo, générez les deux fichiers**, sinon le
navigateur demandera une variante inexistante (404).

Exceptions volontaires :

- `logo.svg` — vectoriel, taille fixe 48×48
- `hero-mobile.webp` — recadrage portrait servi en dessous de 768px via `<picture>`
- `menu-*.webp` — vignettes de catégorie 320×320, affichées trop petit pour
  justifier une variante
- `map.webp` — carte statique, taille fixe
- `og-image.jpg` — **doit rester en JPEG** : les aperçus de partage
  (Facebook, WhatsApp, LinkedIn) gèrent mal le WebP et pas du tout le SVG
- `about-1280.webp` — palier intermédiaire supplémentaire. C'est la première
  image chargée sous le hero ; sur les DPR mobiles élevés (~2.6), l'écart entre
  960 et 1920 forçait le navigateur à télécharger la variante 1920 en entier,
  ce qui faisait échouer le score Lighthouse mobile. Passé via le deuxième
  argument de `buildSrcSet(src, extraWidths)`. À reproduire pour toute autre
  image chargée immédiatement (pas `loading="lazy"` proche du haut de page).

## Carte

`map.webp` est un assemblage de tuiles OpenStreetMap (zoom 17) centré sur
l'adresse du commerce, avec marqueur aux couleurs de l'enseigne. Aucune
iframe ni script tiers, pour préserver le score Lighthouse. **Provisoire sur
ce template** : centrée sur l'adresse placeholder (mairie de Marseille), à
régénérer pour l'adresse de chaque nouveau client, voir `NOUVEAU-CLIENT.md` §5.

**L'attribution « © les contributeurs OpenStreetMap » est obligatoire** et
affichée sous la carte (`map.attribution` dans `src/config.ts`). Ne la retirez pas.

Pour régénérer la carte à une autre adresse, adaptez les constantes `LAT`/`LON`
et relancez le script d'assemblage des tuiles.
