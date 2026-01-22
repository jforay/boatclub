(() => {
  const header = document.getElementById("siteHeader");
  if (!header) return;

  const hero = document.querySelector("[data-hero]");
  if (!hero) return; // only run on pages that have a hero

  header.classList.add("is-transparent");
  header.classList.remove("is-scrolled");

  const update = () => {
    const threshold = hero.offsetHeight - 60; // tweak if you want sooner/later
    if (window.scrollY > threshold) {
      header.classList.add("is-scrolled");
      header.classList.remove("is-transparent");
    } else {
      header.classList.add("is-transparent");
      header.classList.remove("is-scrolled");
    }
  };

  window.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
  update();
})();
