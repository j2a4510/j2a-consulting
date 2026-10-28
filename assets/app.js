(() => {
  const data = JSON.parse(document.getElementById("site-data").textContent);
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // En-tête : fond plein après le haut de page
  const head = document.querySelector(".site-head");
  const onScrollHead = () => head.classList.toggle("solid", window.scrollY > 40);
  onScrollHead();
  window.addEventListener("scroll", onScrollHead, { passive: true });

  // Titre : le mot final change
  const verb = document.querySelector(".verb span");
  if (verb && !reduce) {
    let i = 0;
    setInterval(() => {
      i = (i + 1) % data.verbs.length;
      verb.animate([{ opacity: 1, transform: "none" }, { opacity: 0, transform: "translateY(-12px)" }], { duration: 260, fill: "forwards" })
        .onfinish = () => {
          verb.textContent = data.verbs[i];
          verb.animate([{ opacity: 0, transform: "translateY(12px)" }, { opacity: 1, transform: "none" }], { duration: 320, fill: "forwards" });
        };
    }, 2800);
  }

  // Carte des corridors : clic sur une ville
  const cities = [...document.querySelectorAll(".corridor .city")];
  const routes = [...document.querySelectorAll(".corridor .route")];
  const card = document.querySelector(".corridor-card");
  let auto = true, idx = 0;
  const select = (n) => {
    idx = n;
    cities.forEach((c, k) => { c.classList.toggle("on", k === n); c.setAttribute("aria-pressed", k === n); });
    routes.forEach((r, k) => r.classList.toggle("on", k === n));
    const d = data.cities[n];
    card.innerHTML = `<div class="k">${d.region}</div><p>${d.text}</p>`;
  };
  cities.forEach((c, k) => {
    const go = () => { auto = false; select(k); };
    c.addEventListener("click", go);
    c.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(); } });
  });
  if (cities.length) {
    select(0);
    if (!reduce) setInterval(() => { if (auto) select((idx + 1) % cities.length); }, 4200);
  }

  // Parcours : défilement horizontal piloté par le scroll
  const pin = document.querySelector(".journey-pin");
  const panels = document.querySelector(".panels");
  const fill = document.querySelector(".track-line i");
  const items = [...document.querySelectorAll(".panel")];
  const horizontal = () => window.matchMedia("(min-width: 900px)").matches && !reduce;
  const onJourney = () => {
    if (!pin) return;
    const r = pin.getBoundingClientRect();
    const total = pin.offsetHeight - window.innerHeight;
    const p = Math.min(1, Math.max(0, -r.top / Math.max(1, total)));
    fill.style.width = (p * 100) + "%";
    if (horizontal()) {
      const max = panels.scrollWidth - panels.parentElement.clientWidth;
      panels.style.transform = `translateX(${-p * Math.max(0, max)}px)`;
      const active = Math.min(items.length - 1, Math.floor(p * items.length));
      items.forEach((el, k) => el.classList.toggle("on", k === active));
    } else {
      panels.style.transform = "";
      items.forEach((el) => el.classList.add("on"));
    }
  };
  onJourney();
  window.addEventListener("scroll", onJourney, { passive: true });
  window.addEventListener("resize", onJourney);

  // Expertises : onglets accessibles
  const tabs = [...document.querySelectorAll(".tab")];
  const tps = [...document.querySelectorAll(".tabpanel")];
  const openTab = (n, focus) => {
    tabs.forEach((t, k) => { t.setAttribute("aria-selected", k === n); t.tabIndex = k === n ? 0 : -1; });
    tps.forEach((p, k) => {
      p.hidden = k !== n;
      if (k === n) { p.classList.remove("enter"); void p.offsetWidth; p.classList.add("enter"); }
    });
    if (focus) tabs[n].focus();
  };
  tabs.forEach((t, k) => {
    t.addEventListener("click", () => openTab(k));
    t.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown" || e.key === "ArrowRight") { e.preventDefault(); openTab((k + 1) % tabs.length, true); }
      if (e.key === "ArrowUp" || e.key === "ArrowLeft") { e.preventDefault(); openTab((k - 1 + tabs.length) % tabs.length, true); }
    });
  });

  // Market Access : échelle des formules
  const rungs = [...document.querySelectorAll(".rung")];
  const lc = document.querySelector(".ladder-copy");
  const climb = (n) => {
    rungs.forEach((r, k) => { r.setAttribute("aria-pressed", k === n); r.classList.toggle("lit", k <= n); });
    const t = data.tiers[n];
    lc.innerHTML = `<h3>${t.name}</h3><p>${t.text}</p>`;
  };
  rungs.forEach((r, k) => r.addEventListener("click", () => climb(k)));
  if (rungs.length) climb(0);
})();
