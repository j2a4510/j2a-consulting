(() => {
  document.documentElement.classList.add("js");
  const data = JSON.parse(document.getElementById("site-data").textContent);
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // En-tête : fond plein après le haut de page
  const head = document.querySelector(".site-head");
  const onScrollHead = () => head.classList.toggle("solid", window.scrollY > 40);
  onScrollHead();
  window.addEventListener("scroll", onScrollHead, { passive: true });

  // Menu mobile
  const mb = document.querySelector(".menu-btn"), nav = document.getElementById("mainnav");
  if (mb) {
    const close = () => { mb.setAttribute("aria-expanded", "false"); nav.classList.remove("open"); };
    mb.addEventListener("click", () => {
      const open = mb.getAttribute("aria-expanded") !== "true";
      mb.setAttribute("aria-expanded", open); nav.classList.toggle("open", open);
    });
    nav.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));
    document.addEventListener("keydown", (e) => { if (e.key === "Escape" && mb.getAttribute("aria-expanded") === "true") { close(); mb.focus(); } });
  }

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
  let idx = 0;
  const select = (n) => {
    idx = n;
    cities.forEach((c, k) => { c.classList.toggle("on", k === n); c.setAttribute("aria-pressed", k === n); });
    routes.forEach((r, k) => r.classList.toggle("on", k === n));
    const d = data.cities[n];
    const heading = document.createElement("div");
    heading.className = "k";
    heading.textContent = d.region;
    const copy = document.createElement("p");
    copy.textContent = d.text;
    card.replaceChildren(heading, copy);
  };
  cities.forEach((c, k) => {
    const go = () => select(k);
    c.addEventListener("click", go);
    c.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(); } });
  });
  if (cities.length) {
    select(0);
  }

  // Parcours : la ligne dorée se remplit au fil de la lecture
  const vw = document.querySelector(".vwrap");
  const railFill = document.querySelector(".rail i");
  const vItems = [...document.querySelectorAll(".vsteps > li")];
  const onJourney = () => {
    if (!vw) return;
    const r = vw.getBoundingClientRect();
    const mid = window.innerHeight * 0.6;
    const p = Math.min(1, Math.max(0, (mid - r.top) / r.height));
    railFill.style.height = (p * 100) + "%";
    vItems.forEach((li) => li.classList.toggle("on", li.getBoundingClientRect().top < mid));
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
    const heading = document.createElement("h3");
    heading.textContent = t.name;
    const copy = document.createElement("p");
    copy.textContent = t.text;
    lc.replaceChildren(heading, copy);
  };
  rungs.forEach((r, k) => r.addEventListener("click", () => climb(k)));
  if (rungs.length) climb(0);
})();
