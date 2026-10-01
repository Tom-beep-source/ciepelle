// ============================================================================
// FICHIER UNIQUE DE CONFIGURATION DU COMMERCE
// ----------------------------------------------------------------------------
// Pour dupliquer ce template pour un nouveau client : ne modifiez QUE ce
// fichier. Aucune donnée métier (nom, textes, prix, photos...) ne doit être
// codée en dur ailleurs dans src/components ou src/pages.
// ============================================================================

export type BusinessType = "bakery" | "restaurant" | "florist";

/**
 * Les 14 allergènes à déclaration obligatoire (règlement UE n°1169/2011,
 * annexe II). Toujours afficher le nom exact ci-dessous — jamais résumé en
 * « contient des allergènes », qui ne suffit pas réglementairement.
 */
export type Allergene =
  | "Céréales contenant du gluten"
  | "Crustacés"
  | "Œufs"
  | "Poissons"
  | "Arachides"
  | "Soja"
  | "Lait"
  | "Fruits à coque"
  | "Céleri"
  | "Moutarde"
  | "Graines de sésame"
  | "Anhydride sulfureux et sulfites"
  | "Lupin"
  | "Mollusques";

/** Une paire libellé/valeur libre affichée sous un produit (voir MenuItem.details). */
export interface MenuItemDetail {
  label: string;
  value: string;
}

export interface MenuItem {
  name: string;
  description?: string;
  /** Absent tant que le prix n'a pas été communiqué par le commerçant — ne jamais inventer une valeur ni reprendre celle d'un concurrent. */
  price?: string;
  tags?: Array<"vegan" | "sans-gluten" | "fait-maison" | "bio" | "nouveau">;
  /** Liste courte, dans l'ordre de la recette. */
  ingredients?: string[];
  /** Sous-ensemble des 14 allergènes ci-dessus présents dans ce produit ([] si aucun). */
  allergenes?: Allergene[];
  /**
   * Paires libellé/valeur libres, affichées dans l'ordre donné sous le
   * produit (ex. boucherie : `{ label: "Origine", value: "Bœuf — France,
   * Aveyron" }`, `{ label: "Cuisson", value: "12 min par kilo à 220 °C" }` ;
   * fleuriste : `{ label: "Composition", value: "..." }`, `{ label: "Durée
   * de vie", value: "..." }`). Aucun libellé n'est prédéfini par le
   * template : chaque métier choisit les siens — voir NOUVEAU-CLIENT.md §4 bis.
   */
  details?: MenuItemDetail[];
}

export interface MenuCategory {
  category: string;
  /** Vignette affichée à gauche du titre de catégorie. */
  image?: string;
  items: MenuItem[];
}

export interface GalleryImage {
  src: string;
  alt: string;
}

export interface Testimonial {
  name: string;
  text: string;
  date?: string;
}

export type DayHours = { open: string; close: string } | "closed";

export interface WeeklyHours {
  monday: DayHours;
  tuesday: DayHours;
  wednesday: DayHours;
  thursday: DayHours;
  friday: DayHours;
  saturday: DayHours;
  sunday: DayHours;
}

/** Une ligne de la section « Infos pratiques ». `icon` référence un pictogramme line-art. */
export interface PracticalItem {
  label: string;
  icon:
    | "bag"
    | "coffee"
    | "sunrise"
    | "clock"
    | "wheelchair"
    | "parking"
    | "card"
    | "nfc"
    | "ticket";
  /** Met la ligne en évidence (ex. argument commercial fort). */
  highlight?: boolean;
}

export interface SiteConfig {
  business: {
    name: string;
    type: BusinessType;
    tagline: string;
    description: string;
    logo?: string;
    priceRange: string; // ex: "€€" — utilisé aussi dans le JSON-LD
    /**
     * Types de produits, pour servesCuisine dans le JSON-LD. Propriété
     * schema.org propre aux commerces alimentaires (boulangerie, restaurant) :
     * absente pour les autres métiers (ex. fleuriste), où elle n'est alors pas
     * émise — voir buildLocalBusinessJsonLd dans lib/jsonld.ts.
     */
    cuisine?: string;
  };

  theme: {
    colors: {
      // Couleurs relevées sur la devanture réelle.
      // Attention au rôle de chaque clé dans les composants :
      //  - secondary = surface sombre (hero, pied de page) et texte foncé
      //  - primary   = appels à l'action (boutons, liens)
      //  - accent    = pastilles, mises en évidence
      primary: string;
      secondary: string;
      accent: string;
      background: string;
      text: string;
    };
    fonts: {
      heading: string;
      body: string;
      /**
       * Origines à préconnecter avant le chargement des polices (gain de
       * latence). `crossOrigin: true` pour toute origine qui sert les fichiers
       * de police eux-mêmes (et pas seulement le CSS @font-face) — nécessaire
       * même quand elle est différente de l'origine des feuilles ci-dessous
       * (ex. Google Fonts sert son CSS depuis fonts.googleapis.com mais les
       * fichiers depuis fonts.gstatic.com).
       */
      preconnect: Array<{ href: string; crossOrigin?: boolean }>;
      /**
       * Feuilles de style @font-face à charger (Google Fonts, Fontshare,
       * auto-hébergement...). BaseLayout.astro les charge en non-bloquant
       * (preload -> stylesheet) : voir le commentaire sur le LCP dans ce fichier.
       */
      stylesheets: string[];
    };
  };

  contact: {
    phone: string; // format affiché
    phoneHref: string; // format tel:
    email: string;
    address: {
      street: string;
      city: string;
      zip: string;
      country: string;
      lat: number;
      lng: number;
    };
  };

  hours: WeeklyHours;
  /** Accroche horaires affichée en évidence (argument commercial). */
  hoursHighlight?: string;

  media: {
    heroImage: string;
    /** Recadrage portrait servi en dessous de 768px. */
    heroImageMobile: string;
    aboutImage: string;
  };

  menu: MenuCategory[];
  /**
   * Passe à `true` uniquement une fois que le commerçant a relu et validé
   * `menu[].items[].ingredients`/`allergenes`/`details`. Tant que c'est
   * `false`, la page d'infos produits et la section produits affichent un
   * bandeau d'avertissement (données de démonstration) au lieu d'affirmer
   * que les informations sont validées — voir NOUVEAU-CLIENT.md §4 bis.
   */
  allergenesValides: boolean;

  /**
   * Page dédiée au détail des produits (ingrédients, allergènes, et les
   * paires libellé/valeur de `menu[].items[].details`), pensée pour être
   * ouverte par QR code au comptoir. Le nom du champ historique (`infoPage`,
   * ex-page "allergènes") reste générique : chaque métier y met ce qui le
   * concerne (voir NOUVEAU-CLIENT.md §4 bis).
   */
  infoPage: {
    /** Chemin d'URL, sans slashes (ex. "allergenes", "origine-viandes"). Défaut du template : "allergenes" — ne pas changer une fois le QR code imprimé (voir NOUVEAU-CLIENT.md §9). */
    slug: string;
    /** Titre affiché en haut de la page (ex. "Allergènes", "Origine & cuisson", "Entretien"). */
    title: string;
    /** Paragraphe d'introduction, sous le titre. */
    intro: string;
    /** Libellé du lien vers cette page, utilisé à la fois dans la section produits et dans le pied de page. */
    linkLabel: string;
  };

  /**
   * Section "Commandes" optionnelle sur la page d'accueil : entièrement
   * statique, aucune base de données, aucun suivi, aucun stock. Le bouton
   * « Appeler » et le formulaire (même clé Web3Forms que `forms`) ne font
   * qu'envoyer une demande par e-mail au commerçant, qui rappelle pour
   * confirmer — voir NOUVEAU-CLIENT.md §4 ter. Absent => la section ne
   * s'affiche pas du tout.
   */
  commandes?: {
    title: string;
    intro: string;
    /** Ce qui peut être commandé, dans l'ordre d'affichage. */
    items: Array<{
      label: string;
      /** Délai minimum de commande (ex. "48h", "15 jours"). */
      delaiMinimum: string;
      /** Quantité minimale, si applicable (ex. "6 personnes"). */
      quantiteMinimum?: string;
    }>;
    /** Note sur les périodes de forte demande (ex. fêtes de fin d'année). */
    noteForteDemande?: string;
  };

  gallery: GalleryImage[];

  testimonials: Testimonial[];
  /** Lien vers la fiche Google du commerce (avis réels). */
  googleReviewsUrl?: string;

  practical: {
    services: PracticalItem[];
    accessibility: PracticalItem[];
    payments: PracticalItem[];
  };

  /** Valeurs normalisées schema.org, consommées uniquement par le JSON-LD. */
  structured: {
    paymentAccepted: string;
    currenciesAccepted: string;
    wheelchairAccessibleEntrance: boolean;
    wheelchairAccessibleParking: boolean;
  };

  social: {
    instagram?: string;
    facebook?: string;
    tiktok?: string;
  };

  map: {
    // Carte statique locale : pas d'iframe, aucun script tiers (score Lighthouse).
    staticImage: string;
    staticImageAlt: string;
    /** Mention légale obligatoire pour les tuiles OpenStreetMap. */
    attribution: string;
  };

  forms: {
    web3formsAccessKey: string;
  };

  /**
   * Identité légale de l'ÉDITEUR du site (l'agence/l'auto-entrepreneur qui
   * conçoit et publie le site), PAS celle du commerçant client — ne pas
   * confondre avec `business` ni `contact`, qui décrivent le commerce.
   * Consommé uniquement par /mentions-legales/ et /politique-confidentialite/.
   *
   * Ce bloc entier reste IDENTIQUE pour tous les clients : l'éditeur ne
   * change pas d'un site à l'autre. Ne pas le remplir par client — voir
   * NOUVEAU-CLIENT.md §9.
   */
  legal: {
    /** Raison sociale telle qu'immatriculée. */
    companyName: string;
    /** Forme juridique : "EI", "SARL", "SAS"... */
    legalForm: string;
    siren: string;
    siret: string;
    /** Adresse de l'éditeur (et non celle du commerce, voir contact.address). */
    companyAddress: string;
    /** Ville du greffe d'immatriculation (RCS) — absent pour un auto-entrepreneur non commerçant, non immatriculé au RCS. */
    rcsCity?: string;
    /** Capital social — sociétés uniquement (SARL, SAS...). Laisser undefined pour une entreprise individuelle. */
    shareCapital?: string;
    /** Personne physique responsable de la publication (le plus souvent le dirigeant). */
    publicationDirector: string;
    /** Téléphone et e-mail de l'éditeur (et non ceux du commerce, voir contact.phone/email). */
    phone: string; // format affiché
    phoneHref: string; // format tel:
    email: string;
    /**
     * Hébergeur du site. Identique pour tous les clients tant que le stack
     * (Cloudflare Pages/Workers, voir wrangler.jsonc) ne change pas — à ne
     * modifier que si l'hébergement change.
     */
    host: {
      name: string;
      address: string;
    };
    /** Durée de conservation des données du formulaire de contact. */
    dataRetentionDuration: string;
  };

  seo: {
    title: string;
    description: string;
    ogImage: string;
  };
}

export const siteConfig: SiteConfig = {
  business: {
    name: "BOULANGERIE EXEMPLE",
    type: "bakery",
    tagline: "[À PERSONNALISER] Votre accroche courte et chaleureuse",
    description:
      "[À PERSONNALISER] Décrivez le commerce en une ou deux phrases : univers, spécialités, ambiance.",
    logo: "/images/logo.svg",
    priceRange: "€",
    cuisine: "Boulangerie, Pâtisserie",
  },

  theme: {
    colors: {
      secondary: "#14395F", // bleu profond de l'enseigne — surfaces sombres, texte foncé
      primary: "#A6472F", // brique rouge — boutons et liens
      accent: "#E3B23C", // jaune doré du lettrage — pastilles, mises en évidence
      background: "#FAF6EE", // crème clair — fond de page
      text: "#1B2430",
    },
    // Fraunces en variable (SOFT/WONK épinglés dans l'URL, opsz suit la taille
    // de rendu via global.css), Satoshi via Fontshare. Changer de police pour un
    // nouveau client : mettre à jour heading/body ET preconnect/stylesheets.
    fonts: {
      heading: "Fraunces",
      body: "Satoshi",
      preconnect: [
        { href: "https://fonts.googleapis.com" },
        { href: "https://fonts.gstatic.com", crossOrigin: true },
        { href: "https://api.fontshare.com", crossOrigin: true },
      ],
      stylesheets: [
        "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT,WONK@9..144,400..700,50,1&display=swap",
        // 400 (corps), 500 (font-medium) et 700 (le seul disponible >500, utilisé
        // pour approcher font-semibold/600 en l'absence de variable font Satoshi).
        // 900 n'est demandé par aucune classe du template — inutile à charger.
        "https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&display=swap",
      ],
    },
  },

  contact: {
    phone: "00 00 00 00 00",
    phoneHref: "+330000000000",
    email: "contact@exemple.fr",
    address: {
      street: "[ADRESSE À REMPLIR]",
      city: "[VILLE]",
      zip: "00000",
      country: "FR",
      // À REMPLACER — coordonnées provisoires (mairie de Marseille), pour que
      // la carte et l'itinéraire ne soient jamais vides ni faux par défaut.
      lat: 43.2966,
      lng: 5.3698,
    },
  },

  hours: {
    monday: { open: "[À REMPLIR]", close: "[À REMPLIR]" },
    tuesday: { open: "[À REMPLIR]", close: "[À REMPLIR]" },
    wednesday: { open: "[À REMPLIR]", close: "[À REMPLIR]" },
    thursday: { open: "[À REMPLIR]", close: "[À REMPLIR]" },
    friday: { open: "[À REMPLIR]", close: "[À REMPLIR]" },
    saturday: { open: "[À REMPLIR]", close: "[À REMPLIR]" },
    sunday: { open: "[À REMPLIR]", close: "[À REMPLIR]" },
  },
  hoursHighlight: "[À REMPLIR]",

  // PHOTOS PROVISOIRES - à remplacer par les photos réelles du commerce
  media: {
    heroImage: "/images/hero.webp",
    heroImageMobile: "/images/hero-mobile.webp",
    aboutImage: "/images/about.webp",
  },

  // PHOTOS PROVISOIRES - à remplacer par les photos réelles du commerce
  // PRIX VOLONTAIREMENT ABSENTS : à demander au commerçant pour chaque client,
  // jamais inventés ni repris d'un concurrent (voir NOUVEAU-CLIENT.md §3).
  // ingredients/allergenes : valeurs plausibles à faire valider par le commerçant
  // (voir chaque entrée) — ce sont des affirmations réglementées, jamais à deviner.
  menu: [
    {
      category: "Pains",
      image: "/images/menu-pains.webp",
      items: [
        {
          name: "Baguette tradition",
          description: "Farine locale, levain naturel, cuisson au feu de bois",
          tags: ["fait-maison"],
          ingredients: ["Farine de blé", "Eau", "Levain", "Sel"], // À CONFIRMER avec le commerçant
          allergenes: ["Céréales contenant du gluten"], // À CONFIRMER avec le commerçant
        },
        {
          name: "Pain de campagne",
          description: "Miche de 500g, croûte épaisse, mie alvéolée",
          tags: ["fait-maison", "bio"],
          ingredients: ["Farine de blé", "Farine de seigle", "Eau", "Levain", "Sel"], // À CONFIRMER avec le commerçant
          allergenes: ["Céréales contenant du gluten"], // À CONFIRMER avec le commerçant
        },
        {
          name: "Pain sans gluten",
          description: "Farine de riz et sarrasin",
          tags: ["sans-gluten"],
          ingredients: ["Farine de riz", "Farine de sarrasin", "Eau", "Levure", "Sel"], // À CONFIRMER avec le commerçant
          allergenes: [], // À CONFIRMER avec le commerçant
        },
      ],
    },
    {
      category: "Viennoiseries",
      image: "/images/menu-viennoiseries.webp",
      items: [
        {
          name: "Croissant au beurre",
          tags: ["fait-maison"],
          ingredients: ["Farine de blé", "Beurre", "Lait", "Sucre", "Levure", "Sel"], // À CONFIRMER avec le commerçant
          allergenes: ["Céréales contenant du gluten", "Lait"], // À CONFIRMER avec le commerçant
        },
        {
          name: "Pain au chocolat",
          tags: ["fait-maison"],
          ingredients: ["Farine de blé", "Beurre", "Chocolat", "Lait", "Sucre", "Levure", "Sel"], // À CONFIRMER avec le commerçant
          allergenes: ["Céréales contenant du gluten", "Lait", "Soja"], // À CONFIRMER avec le commerçant
        },
        {
          name: "Chausson aux pommes",
          tags: ["nouveau"],
          ingredients: ["Pâte feuilletée (farine de blé, beurre)", "Pommes", "Sucre"], // À CONFIRMER avec le commerçant
          allergenes: ["Céréales contenant du gluten", "Lait"], // À CONFIRMER avec le commerçant
        },
      ],
    },
    {
      category: "Pâtisseries",
      image: "/images/menu-patisseries.webp",
      items: [
        {
          name: "Tarte au citron meringuée",
          tags: ["fait-maison"],
          ingredients: ["Pâte sablée (farine de blé, beurre)", "Citron", "Œufs", "Sucre"], // À CONFIRMER avec le commerçant
          allergenes: ["Céréales contenant du gluten", "Lait", "Œufs"], // À CONFIRMER avec le commerçant
        },
        {
          name: "Éclair vanille",
          ingredients: ["Pâte à choux (farine de blé, œufs, beurre)", "Crème pâtissière vanille", "Lait", "Sucre"], // À CONFIRMER avec le commerçant
          allergenes: ["Céréales contenant du gluten", "Œufs", "Lait"], // À CONFIRMER avec le commerçant
        },
        {
          name: "Tartelette aux fruits (vegan)",
          tags: ["vegan"],
          ingredients: ["Pâte sablée sans beurre (farine de blé, huile)", "Fruits frais", "Crème végétale", "Sucre"], // À CONFIRMER avec le commerçant
          allergenes: ["Céréales contenant du gluten"], // À CONFIRMER avec le commerçant
        },
      ],
    },
  ],

  // false tant que le commerçant n'a pas relu/validé ingredients/allergenes
  // ci-dessus (actuellement des valeurs plausibles // À CONFIRMER) — passer à
  // true seulement après validation explicite du commerçant.
  allergenesValides: false,

  infoPage: {
    slug: "allergenes",
    title: "Allergènes",
    intro:
      "Ces informations sont fournies par BOULANGERIE EXEMPLE. Elles complètent l'affichage obligatoire disponible en boutique, sans le remplacer : en cas de doute ou d'allergie sévère, demandez confirmation à l'équipe avant de commander.",
    linkLabel: "Allergènes",
  },

  // EXEMPLE — section optionnelle (voir NOUVEAU-CLIENT.md §4 ter). Mettre
  // `commandes` à `undefined` (supprimer le bloc entier) pour désactiver la
  // section si le commerce ne prend pas de commandes à l'avance.
  commandes: {
    title: "Commandes",
    intro:
      "[À PERSONNALISER] Certaines pièces se préparent sur commande. Appelez-nous ou envoyez votre demande ci-dessous : nous vous recontactons pour confirmer le délai et les modalités de retrait.",
    items: [
      { label: "Bûche de Noël", delaiMinimum: "48h", quantiteMinimum: "6 personnes" }, // À CONFIRMER avec le commerçant
      { label: "Pièce montée / gâteau d'événement", delaiMinimum: "15 jours", quantiteMinimum: "10 personnes" }, // À CONFIRMER avec le commerçant
    ],
    noteForteDemande:
      "Délais rallongés autour des fêtes de fin d'année et de Pâques : anticipez votre commande.",
  },

  // PHOTOS PROVISOIRES - aplats générés (voir scripts/generate-placeholder-images.mjs),
  // à remplacer par les photos réelles du commerce. L'alt reflète le contenu
  // actuel (un aplat, pas encore la scène finale) : à réécrire en même temps
  // que chaque photo, pour décrire ce qui sera réellement visible.
  gallery: [
    { src: "/images/gallery-1.webp", alt: "Aplat décoratif provisoire — photo du commerce à venir" },
    { src: "/images/gallery-2.webp", alt: "Aplat décoratif provisoire — photo du commerce à venir" },
    { src: "/images/gallery-3.webp", alt: "Aplat décoratif provisoire — photo du commerce à venir" },
    { src: "/images/gallery-4.webp", alt: "Aplat décoratif provisoire — photo du commerce à venir" },
    { src: "/images/gallery-5.webp", alt: "Aplat décoratif provisoire — photo du commerce à venir" },
    { src: "/images/gallery-6.webp", alt: "Aplat décoratif provisoire — photo du commerce à venir" },
  ],

  // FICTIF - À REMPLACER par de vrais avis autorisés
  testimonials: [
    {
      name: "[À PERSONNALISER] Prénom N.",
      text: "[À PERSONNALISER] Exemple d'avis — à remplacer par un vrai avis client autorisé.",
    },
  ],
  // À REMPLACER par le lien de la fiche Google du commerce réel
  googleReviewsUrl: "https://www.google.com/maps/search/?api=1&query=BOULANGERIE+EXEMPLE",

  practical: {
    // Pas de livraison : ne rien ajouter ici qui la suggère.
    services: [
      { label: "Vente à emporter", icon: "bag" },
      { label: "Café sur place", icon: "coffee" },
      { label: "Petit déjeuner", icon: "sunrise" },
      { label: "Passage rapide", icon: "clock" },
    ],
    accessibility: [
      { label: "Entrée accessible en fauteuil roulant", icon: "wheelchair" },
      { label: "Parking accessible en fauteuil roulant", icon: "parking" },
    ],
    payments: [
      { label: "Cartes de crédit et de débit", icon: "card" },
      { label: "Paiement mobile sans contact", icon: "nfc" },
      { label: "Titres restaurant Pluxee acceptés", icon: "ticket", highlight: true },
    ],
  },

  structured: {
    paymentAccepted: "Cash, Credit Card, Debit Card, NFC Mobile Payments, Pluxee",
    currenciesAccepted: "EUR",
    wheelchairAccessibleEntrance: true,
    wheelchairAccessibleParking: true,
  },

  social: {},

  map: {
    staticImage: "/images/map.webp",
    staticImageAlt: "[À PERSONNALISER] Plan du commerce, avec son emplacement",
    attribution: "© les contributeurs OpenStreetMap",
  },

  forms: {
    web3formsAccessKey: "", // CRÉER UNE CLÉ PAR CLIENT sur web3forms.com
  },

  // Identité de l'éditeur (Tom Canal) — fixe pour tous les clients, voir
  // NOUVEAU-CLIENT.md §9. Ne pas remplacer par les informations du commerçant.
  legal: {
    companyName: "Tom Canal",
    legalForm: "EI",
    siren: "107623431",
    siret: "10762343100015",
    companyAddress: "68 avenue des Pyrénées 31600 Muret",
    // Pas de rcsCity : auto-entrepreneur non commerçant, non immatriculé au RCS.
    // Pas de shareCapital : pas de capital social en EI.
    publicationDirector: "Tom Canal",
    phone: "06 65 29 59 01",
    phoneHref: "+33665295901",
    email: "tommuret.canal@gmail.com",
    host: {
      name: "Cloudflare, Inc.",
      address: "101 Townsend Street, San Francisco, CA 94107, États-Unis",
    },
    dataRetentionDuration: "3 ans à compter du dernier contact",
  },

  seo: {
    title: "[À PERSONNALISER] Nom du commerce — Ville | Accroche courte",
    description:
      "[À PERSONNALISER] Décrivez le commerce, sa ville et ses spécialités pour les moteurs de recherche.",
    // PHOTO PROVISOIRE - aplat généré avec nom + ville (voir
    // scripts/generate-placeholder-images.mjs), à remplacer par une vraie photo.
    ogImage: "/images/og-image.jpg",
  },
};

// ----------------------------------------------------------------------------
// Helpers dérivés de la config — utilisés par les composants, ne pas dupliquer
// la logique métier ailleurs.
// ----------------------------------------------------------------------------

const DAY_ORDER: (keyof WeeklyHours)[] = [
  "monday",
  "tuesday",
  "wednesday",
  "thursday",
  "friday",
  "saturday",
  "sunday",
];

const DAY_LABELS: Record<keyof WeeklyHours, string> = {
  monday: "Lundi",
  tuesday: "Mardi",
  wednesday: "Mercredi",
  thursday: "Jeudi",
  friday: "Vendredi",
  saturday: "Samedi",
  sunday: "Dimanche",
};

export function getOrderedHours(config: SiteConfig = siteConfig) {
  return DAY_ORDER.map((day) => ({
    day,
    label: DAY_LABELS[day],
    hours: config.hours[day],
  }));
}

export function formatDayHours(hours: DayHours): string {
  if (hours === "closed") return "Fermé";
  return `${hours.open} – ${hours.close}`;
}

export function getFullAddress(config: SiteConfig = siteConfig): string {
  const { street, zip, city } = config.contact.address;
  return `${street}, ${zip} ${city}`;
}

export function getDirectionsUrl(config: SiteConfig = siteConfig): string {
  const { lat, lng } = config.contact.address;
  return `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`;
}

/** Vrai si le commerce ouvre tous les jours aux mêmes heures. */
export function isOpenEveryDay(config: SiteConfig = siteConfig): boolean {
  const values = DAY_ORDER.map((d) => config.hours[d]);
  const first = values[0];
  if (first === "closed") return false;
  return values.every(
    (h) => h !== "closed" && h.open === first.open && h.close === first.close
  );
}

export function isBakery(config: SiteConfig = siteConfig): boolean {
  return config.business.type === "bakery";
}

export function isRestaurant(config: SiteConfig = siteConfig): boolean {
  return config.business.type === "restaurant";
}

export function isFlorist(config: SiteConfig = siteConfig): boolean {
  return config.business.type === "florist";
}

/**
 * Libellés de la section produits, adaptés au métier : nav du header (forme
 * nominale) et bouton d'appel à l'action du hero (forme impérative). Ajouter
 * une entrée ici pour tout nouveau `BusinessType`.
 */
const MENU_SECTION_LABELS: Record<BusinessType, { nav: string; cta: string }> = {
  bakery: { nav: "Nos produits", cta: "Voir nos produits" },
  restaurant: { nav: "Notre carte", cta: "Voir notre carte" },
  florist: { nav: "Nos compositions", cta: "Voir nos compositions" },
};

export function getMenuSectionLabels(config: SiteConfig = siteConfig) {
  return MENU_SECTION_LABELS[config.business.type];
}
