import gsap from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";

let registered = false;

function ensureRegistered() {
  if (!registered) {
    gsap.registerPlugin(ScrollTrigger);
    registered = true;
  }
}

/** Anime l'entrée du hero au chargement de la page (pas de scroll requis). */
export function heroEnter(root: ParentNode = document) {
  ensureRegistered();
  const targets = root.querySelectorAll<HTMLElement>("[data-hero-in]");
  if (!targets.length) return;

  gsap.from(targets, {
    y: 32,
    opacity: 0,
    duration: 1,
    ease: "power3.out",
    stagger: 0.12,
    delay: 0.15,
  });
}

/** Révèle en fondu/translation les éléments marqués [data-reveal] au scroll. */
export function revealOnScroll(root: ParentNode = document) {
  ensureRegistered();
  const targets = root.querySelectorAll<HTMLElement>("[data-reveal]");

  targets.forEach((el) => {
    gsap.from(el, {
      y: 24,
      opacity: 0,
      duration: 0.8,
      ease: "power2.out",
      scrollTrigger: {
        trigger: el,
        start: "top 85%",
        toggleActions: "play none none none",
      },
    });
  });
}

/** Anime en stagger les enfants directs d'un conteneur [data-reveal-group]. */
export function revealGroupsOnScroll(root: ParentNode = document) {
  ensureRegistered();
  const groups = root.querySelectorAll<HTMLElement>("[data-reveal-group]");

  groups.forEach((group) => {
    const children = Array.from(group.children) as HTMLElement[];
    if (!children.length) return;

    gsap.from(children, {
      y: 24,
      opacity: 0,
      duration: 0.7,
      ease: "power2.out",
      stagger: 0.08,
      scrollTrigger: {
        trigger: group,
        start: "top 85%",
        toggleActions: "play none none none",
      },
    });
  });
}

export function initScrollAnimations(root: ParentNode = document) {
  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  if (prefersReducedMotion) return;

  heroEnter(root);
  revealOnScroll(root);
  revealGroupsOnScroll(root);
}
