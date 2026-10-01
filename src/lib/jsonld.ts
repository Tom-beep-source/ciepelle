import {
  siteConfig,
  isOpenEveryDay,
  type SiteConfig,
  type WeeklyHours,
} from "../config";

const SCHEMA_DAY: Record<keyof WeeklyHours, string> = {
  monday: "https://schema.org/Monday",
  tuesday: "https://schema.org/Tuesday",
  wednesday: "https://schema.org/Wednesday",
  thursday: "https://schema.org/Thursday",
  friday: "https://schema.org/Friday",
  saturday: "https://schema.org/Saturday",
  sunday: "https://schema.org/Sunday",
};

const BUSINESS_SCHEMA_TYPE: Record<SiteConfig["business"]["type"], string> = {
  bakery: "Bakery",
  restaurant: "Restaurant",
  florist: "Florist",
};

/**
 * Horaires au format schema.org. Quand le commerce ouvre tous les jours aux
 * mêmes heures, on émet une seule entrée listant les 7 jours plutôt que 7
 * entrées redondantes.
 */
function buildOpeningHours(config: SiteConfig) {
  const days = Object.keys(config.hours) as (keyof WeeklyHours)[];

  if (isOpenEveryDay(config)) {
    const hours = config.hours.monday;
    if (hours !== "closed") {
      return [
        {
          "@type": "OpeningHoursSpecification",
          dayOfWeek: days.map((d) => SCHEMA_DAY[d]),
          opens: hours.open,
          closes: hours.close,
        },
      ];
    }
  }

  return days
    .filter((day) => config.hours[day] !== "closed")
    .map((day) => {
      const hours = config.hours[day];
      if (hours === "closed") return null;
      return {
        "@type": "OpeningHoursSpecification",
        dayOfWeek: SCHEMA_DAY[day],
        opens: hours.open,
        closes: hours.close,
      };
    })
    .filter(Boolean);
}

function buildAmenityFeatures(config: SiteConfig) {
  const features: Array<{ name: string; value: boolean }> = [
    {
      name: "wheelchairAccessibleEntrance",
      value: config.structured.wheelchairAccessibleEntrance,
    },
    {
      name: "wheelchairAccessibleParking",
      value: config.structured.wheelchairAccessibleParking,
    },
  ];

  return features.map((f) => ({
    "@type": "LocationFeatureSpecification",
    name: f.name,
    value: f.value,
  }));
}

export function buildLocalBusinessJsonLd(
  config: SiteConfig = siteConfig,
  siteUrl = ""
) {
  const sameAs = Object.values(config.social).filter(Boolean);

  return {
    "@context": "https://schema.org",
    "@type": BUSINESS_SCHEMA_TYPE[config.business.type],
    name: config.business.name,
    description: config.business.description,
    image: siteUrl ? `${siteUrl}${config.seo.ogImage}` : config.seo.ogImage,
    url: siteUrl || undefined,
    telephone: config.contact.phoneHref,
    priceRange: config.business.priceRange,
    ...(config.business.cuisine ? { servesCuisine: config.business.cuisine } : {}),
    paymentAccepted: config.structured.paymentAccepted,
    currenciesAccepted: config.structured.currenciesAccepted,
    address: {
      "@type": "PostalAddress",
      streetAddress: config.contact.address.street,
      addressLocality: config.contact.address.city,
      postalCode: config.contact.address.zip,
      addressCountry: config.contact.address.country,
    },
    geo: {
      "@type": "GeoCoordinates",
      latitude: config.contact.address.lat,
      longitude: config.contact.address.lng,
    },
    openingHoursSpecification: buildOpeningHours(config),
    amenityFeature: buildAmenityFeatures(config),
    hasMenu: siteUrl ? `${siteUrl}/#menu` : "#menu",
    ...(sameAs.length ? { sameAs } : {}),
  };
}
