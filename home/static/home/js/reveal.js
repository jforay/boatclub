document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".home-card");
  if (!cards.length) return;

  // Add base class + stagger delays
  cards.forEach((card, i) => {
    card.classList.add("reveal-up");
    card.style.setProperty("--reveal-delay", `${i * 70}ms`);
  });

  // Reveal when in view
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target); // reveal once
        }
      });
    },
    { threshold: 0.15, rootMargin: "0px 0px -10% 0px" }
  );

  cards.forEach((card) => io.observe(card));
});
