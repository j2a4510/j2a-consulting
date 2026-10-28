"""Génère les pages FR et EN du site J2A Consulting à partir d'un seul gabarit.
Usage : python3 build.py
"""
import math, pathlib

ROOT = pathlib.Path(__file__).parent

# Projection équirectangulaire simple (lon, lat) -> (x, y) sur 1000 x 500
def xy(lon, lat):
    return round((lon + 180) / 360 * 1000, 1), round((90 - lat) / 180 * 500, 1)

HUB = ("Lomé", 1.22, 6.13)
CITIES = {
    "fr": [("Dakar", -17.45, 14.69), ("Paris", 2.35, 48.86), ("Montréal", -73.57, 45.50),
           ("Dubaï", 55.30, 25.27), ("Shanghai", 121.47, 31.23)],
    "en": [("Dakar", -17.45, 14.69), ("Paris", 2.35, 48.86), ("Montréal", -73.57, 45.50),
           ("Dubai", 55.30, 25.27), ("Shanghai", 121.47, 31.23)],
}

def corridor_svg(lang, title):
    hx, hy = xy(HUB[1], HUB[2])
    parts = [f'<svg viewBox="240 95 680 160" role="img" aria-label="{title}">']
    # grille de points discrète
    for gx in range(246, 920, 18):
        for gy in range(100, 255, 18):
            parts.append(f'<circle class="grid-dot" cx="{gx}" cy="{gy}" r="1"/>')
    for name, lon, lat in CITIES[lang]:
        x, y = xy(lon, lat)
        mx, my = (hx + x) / 2, (hy + y) / 2
        d = math.hypot(x - hx, y - hy)
        # point de contrôle décalé perpendiculairement, toujours vers le haut
        px, py = -(y - hy) / d, (x - hx) / d
        if py > 0:
            px, py = -px, -py
        cx, cy = mx + px * d * 0.35, my + py * d * 0.35
        parts.append(f'<path class="route draw" d="M{hx},{hy} Q{cx:.1f},{cy:.1f} {x},{y}"/>')
    for name, lon, lat in CITIES[lang]:
        x, y = xy(lon, lat)
        anchor = "end" if x < hx - 20 else "start"
        dx = -8 if anchor == "end" else 8
        parts.append(f'<circle class="dot" cx="{x}" cy="{y}" r="3"/>')
        parts.append(f'<text x="{x+dx}" y="{y-6}" text-anchor="{anchor}">{name}</text>')
    parts.append(f'<circle class="hub-ring" cx="{hx}" cy="{hy}" r="11"/>')
    parts.append(f'<circle class="hub" cx="{hx}" cy="{hy}" r="5"/>')
    parts.append(f'<text class="hub-label" x="{hx+14}" y="{hy+18}">{HUB[0]}</text>')
    parts.append("</svg>")
    return "\n".join(parts)

T = {
"fr": dict(
    lang="fr", other_href="en/", other_label="English", base="",
    title="J2A Consulting | Structuration et financement de projets en Afrique de l'Ouest",
    desc="J2A Consulting, cabinet basé à Lomé, structure des projets africains pour qu'ils deviennent finançables : étude, structuration, financement, implantation. Afrique de l'Ouest, Golfe, Québec, Asie.",
    nav=[("#approche", "Approche"), ("#expertises", "Expertises"), ("#ecosysteme", "Écosystème"), ("#contact", "Contact")],
    h1='Nous rendons les projets africains <strong>finançables</strong>.',
    lede="Depuis Lomé, J2A Consulting relie les porteurs de projets, les collectivités et les investisseurs. Nous structurons, nous montons les financements et nous accompagnons l'implantation, de l'Afrique de l'Ouest au Golfe, au Québec et à l'Asie.",
    cta1="Parler de votre projet", cta2="Notre approche",
    map_title="Les corridors de J2A Consulting au départ de Lomé",
    map_caption="Nos corridors : Afrique de l'Ouest, Europe, Golfe, Amérique du Nord, Asie.",
    h_approach="Entre un bon projet et son financement, il manque souvent un dossier.",
    approach=["Beaucoup de projets solides ne trouvent pas de financement. Ce n'est pas faute d'argent disponible : il manque un dossier au standard des banques et des fonds, une structure juridique claire, un plan par phases et des partenaires au bon endroit.",
              "C'est ce chaînon que nous construisons. Nous travaillons pour les entreprises, les investisseurs étrangers qui entrent sur le marché, et les collectivités qui doivent transformer leurs besoins en projets finançables."],
    steps_label="Notre démarche, en quatre étapes",
    steps=[("Étudier", "Marché, faisabilité, partenaires locaux. Nous validons le projet avant d'engager des moyens."),
           ("Structurer", "Montage juridique et financier, phasage, modèle financier, gouvernance."),
           ("Financer", "Dossiers au format banque et investisseur, recherche et négociation avec les financeurs."),
           ("Implanter", "Mise en œuvre sur le terrain, partenaires, représentation locale.")],
    h_exp="Nos domaines d'intervention",
    exp=[("Agro-industrie", "Production, transformation et export : structuration de filières, contrats avec les acheteurs, certification, financement des campagnes."),
         ("Immobilier", "Projets résidentiels et mixtes : faisabilité, montage, dossiers bancaires et recherche d'investisseurs."),
         ("Collectivités et institutions", "Accompagnement des communes et des organisations : plans d'investissement, projets prioritaires, partenariats avec les bailleurs."),
         ("Entrée sur le marché", "Pour les entreprises étrangères qui veulent tester l'Afrique de l'Ouest avant de s'y installer : veille, partenaires, prospection, représentation.")],
    h_market="J2A Market Access",
    market=["Une offre pour les entreprises internationales qui veulent se développer en Afrique de l'Ouest sans ouvrir tout de suite une filiale. Présence commerciale, connaissance du marché, opportunités qualifiées et représentation locale, activées par étapes selon les résultats.",
            "Pour les gouvernements, les fonds souverains, les family offices et les groupes internationaux, nous montons aussi des mandats sur mesure : représentation stratégique, relations institutionnelles, appui aux négociations."],
    tiers=["Découvrir", "Connecter", "Développer", "S'implanter"],
    quote="« Entrer sur un nouveau marché ne devrait jamais commencer par l'ouverture d'un bureau. »",
    h_eco="Un écosystème de projets",
    eco=[("Ipomoea Africa", "https://ipomoea.africa", "Production et export agro-industriels au Togo, construits par phases, de la patate douce à la transformation."),
         ("Growing Beyond Vision", None, "Architecture d'investissement pour l'Afrique, depuis Sharjah, entre le Golfe, l'Asie et l'Afrique de l'Ouest."),
         ("Association Togolaise de la Franchise", None, "Promotion de la franchise comme levier de développement des entreprises au Togo.")],
    h_lead="Le dirigeant",
    lead_name="Yaovi Kokodoko", lead_role="Directeur général, J2A Consulting",
    lead=["Yaovi Kokodoko structure des projets et des financements entre l'Afrique de l'Ouest, le Golfe, le Québec et l'Asie. Il travaille avec des entreprises, des investisseurs et des collectivités, en agro-industrie, en immobilier et en développement institutionnel.",
          "Il est cofondateur de Growing Beyond Vision, gérant d'Ipomoea Africa et président de l'Association Togolaise de la Franchise."],
    h_contact="Parlons de votre projet.",
    contact_intro="Un premier échange de trente minutes suffit pour savoir comment nous pouvons vous aider.",
    c_mail="E-mail", c_tel="Téléphone", c_where="Bureau", where="Lomé, Togo",
    rights="J2A Consulting SARL, Lomé, République togolaise",
),
"en": dict(
    lang="en", other_href="../", other_label="Français", base="../",
    title="J2A Consulting | Project structuring and financing in West Africa",
    desc="J2A Consulting, based in Lomé, structures African projects so they become financeable: studies, structuring, financing, implementation. West Africa, the Gulf, Quebec, Asia.",
    nav=[("#approche", "Approach"), ("#expertises", "Expertise"), ("#ecosysteme", "Ecosystem"), ("#contact", "Contact")],
    h1='We make African projects <strong>financeable</strong>.',
    lede="From Lomé, J2A Consulting connects project owners, local governments and investors. We structure projects, raise the financing and support implementation, from West Africa to the Gulf, Quebec and Asia.",
    cta1="Discuss your project", cta2="Our approach",
    map_title="J2A Consulting's corridors from Lomé",
    map_caption="Our corridors: West Africa, Europe, the Gulf, North America, Asia.",
    h_approach="Between a good project and its financing, what is often missing is a file.",
    approach=["Many sound projects never get financed. Money is not the problem: what is missing is a file that meets bank and fund standards, a clear legal structure, a phased plan and the right partners in the right place.",
              "That missing link is what we build. We work for companies, for foreign investors entering the market, and for local governments that need to turn their needs into financeable projects."],
    steps_label="Our approach, in four steps",
    steps=[("Study", "Market, feasibility, local partners. We validate the project before committing resources."),
           ("Structure", "Legal and financial set-up, phasing, financial model, governance."),
           ("Finance", "Bank- and investor-grade files, sourcing and negotiation with financiers."),
           ("Implement", "On-the-ground execution, partners, local representation.")],
    h_exp="What we work on",
    exp=[("Agribusiness", "Production, processing and export: value-chain structuring, buyer contracts, certification, seasonal financing."),
         ("Real estate", "Residential and mixed-use projects: feasibility, structuring, bank files and investor search."),
         ("Local governments and institutions", "Support for municipalities and organisations: investment plans, priority projects, partnerships with donors."),
         ("Market entry", "For foreign companies that want to test West Africa before setting up: market intelligence, partners, business development, representation.")],
    h_market="J2A Market Access",
    market=["An offer for international companies that want to grow in West Africa without opening a subsidiary right away. Commercial presence, market intelligence, qualified opportunities and local representation, activated step by step as results come in.",
            "For governments, sovereign funds, family offices and multinationals, we also structure bespoke mandates: strategic representation, institutional relations, negotiation support."],
    tiers=["Discover", "Connect", "Grow", "Establish"],
    quote="“Entering a new market should never begin with opening an office.”",
    h_eco="An ecosystem of projects",
    eco=[("Ipomoea Africa", "https://ipomoea.africa", "Agro-industrial production and export in Togo, built in phases, from sweet potato to processing."),
         ("Growing Beyond Vision", None, "Investment architecture for Africa, from Sharjah, across the Gulf, Asia and West Africa."),
         ("Togolese Franchise Association", None, "Promoting franchising as a growth lever for businesses in Togo.")],
    h_lead="Leadership",
    lead_name="Yaovi Kokodoko", lead_role="Managing Director, J2A Consulting",
    lead=["Yaovi Kokodoko structures projects and financing across West Africa, the Gulf, Quebec and Asia. He works with companies, investors and local governments in agribusiness, real estate and institutional development.",
          "He is co-founder of Growing Beyond Vision, managing director of Ipomoea Africa and president of the Togolese Franchise Association."],
    h_contact="Let's talk about your project.",
    contact_intro="A first thirty-minute conversation is enough to see how we can help.",
    c_mail="Email", c_tel="Phone", c_where="Office", where="Lomé, Togo",
    rights="J2A Consulting SARL, Lomé, Togolese Republic",
),
}

def page(t):
    b = t["base"]
    nav = "".join(f'<a href="{h}">{l}</a>' for h, l in t["nav"])
    steps = "".join(f'<li><span class="n" aria-hidden="true">{i}</span><h3>{h}</h3><p>{p}</p></li>'
                    for i, (h, p) in enumerate(t["steps"], 1))
    exp = "".join(f'<div class="exp"><h3>{h}</h3><p>{p}</p></div>' for h, p in t["exp"])
    eco = "".join(
        f'<div class="eco"><h3>' + (f'<a href="{u}" rel="noopener">{n}</a>' if u else n) + f'</h3><p>{p}</p></div>'
        for n, u, p in t["eco"])
    tiers = "".join(f"<li>{x}</li>" for x in t["tiers"])
    approach = "".join(f"<p>{p}</p>" for p in t["approach"])
    market = "".join(f"<p>{p}</p>" for p in t["market"])
    lead = "".join(f"<p>{p}</p>" for p in t["lead"])
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<meta property="og:title" content="{t['title']}">
<meta property="og:description" content="{t['desc']}">
<link rel="alternate" hreflang="fr" href="{b}">
<link rel="alternate" hreflang="en" href="{b}en/">
<link rel="icon" href="{b}assets/logo.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{b}assets/style.css">
</head>
<body>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="{b if b else './'}"><img src="{b}assets/logo-light.svg" alt="J2A Consulting"></a>
    <nav class="nav" aria-label="Navigation">{nav}<a class="lang" href="{t['other_href']}" lang="{'en' if t['lang']=='fr' else 'fr'}">{t['other_label']}</a></nav>
  </div>
</header>

<main>
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>{t['h1']}</h1>
      <p class="lede">{t['lede']}</p>
      <div class="cta-row">
        <a class="btn btn-gold" href="#contact">{t['cta1']}</a>
        <a class="btn btn-ghost" href="#approche">{t['cta2']}</a>
      </div>
    </div>
    <figure class="corridor" style="margin:0">
      {corridor_svg(t['lang'], t['map_title'])}
      <figcaption class="corridor-caption">{t['map_caption']}</figcaption>
    </figure>
  </div>
</section>

<section class="block" id="approche">
  <div class="wrap">
    <div class="intro">
      <h2>{t['h_approach']}</h2>
      <div>{approach}</div>
    </div>
    <ol class="steps" aria-label="{t['steps_label']}">{steps}</ol>
  </div>
</section>

<section class="block expertise" id="expertises">
  <div class="wrap">
    <h2>{t['h_exp']}</h2>
    <div class="exp-list">{exp}</div>
  </div>
</section>

<section class="block market">
  <div class="wrap">
    <div>
      <h2>{t['h_market']}</h2>
      <div style="margin-top:24px">{market}</div>
      <ul class="tiers">{tiers}</ul>
    </div>
    <blockquote>{t['quote']}</blockquote>
  </div>
</section>

<section class="block" id="ecosysteme">
  <div class="wrap">
    <h2>{t['h_eco']}</h2>
    <div class="eco-list">{eco}</div>
  </div>
</section>

<section class="block lead">
  <div class="wrap">
    <div>
      <h2>{t['h_lead']}</h2>
      <p class="role"><strong>{t['lead_name']}</strong><br>{t['lead_role']}</p>
    </div>
    <div>{lead}</div>
  </div>
</section>
</main>

<footer class="contact" id="contact">
  <div class="wrap">
    <h2>{t['h_contact']}</h2>
    <p style="color:#b9c6cb;margin-top:16px">{t['contact_intro']}</p>
    <div class="contact-grid">
      <a href="mailto:ykstrategic@proton.me"><span>{t['c_mail']}</span>ykstrategic@proton.me</a>
      <a href="tel:+22871527976"><span>{t['c_tel']}</span>+228 71 52 79 76</a>
      <div><span>{t['c_where']}</span>{t['where']}</div>
    </div>
    <div class="foot">
      <img src="{b}assets/logo-light.svg" alt="">
      <div>© 2026 {t['rights']}</div>
    </div>
  </div>
</footer>
</body>
</html>
"""

(ROOT / "index.html").write_text(page(T["fr"]), encoding="utf-8")
(ROOT / "en" / "index.html").write_text(page(T["en"]), encoding="utf-8")
print("ok")
