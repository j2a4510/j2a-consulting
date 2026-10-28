"""Génère les pages FR et EN du site J2A Consulting à partir d'un seul gabarit.
Usage : python3 build.py
"""
import json, math, pathlib

ROOT = pathlib.Path(__file__).parent

def xy(lon, lat):
    """Projection équirectangulaire simple (lon, lat) -> (x, y) sur 1000 x 500."""
    return round((lon + 180) / 360 * 1000, 1), round((90 - lat) / 180 * 500, 1)

HUB = ("Lomé", 1.22, 6.13)
COORDS = [(-17.45, 14.69), (2.35, 48.86), (-73.57, 45.50), (55.30, 25.27), (121.47, 31.23)]

def corridor_svg(t):
    hx, hy = xy(HUB[1], HUB[2])
    out = [f'<svg viewBox="236 92 690 168" role="group" aria-label="{t["map_title"]}">']
    for gx in range(242, 926, 16):
        for gy in range(98, 258, 16):
            out.append(f'<circle class="grid-dot" cx="{gx}" cy="{gy}" r="1"/>')
    pts = []
    for (lon, lat) in COORDS:
        x, y = xy(lon, lat)
        mx, my = (hx + x) / 2, (hy + y) / 2
        d = math.hypot(x - hx, y - hy)
        px, py = -(y - hy) / d, (x - hx) / d
        if py > 0:
            px, py = -px, -py
        cx, cy = mx + px * d * 0.35, my + py * d * 0.35
        out.append(f'<path class="route" id="r{len(pts)}" d="M{hx},{hy} Q{cx:.1f},{cy:.1f} {x},{y}"/>')
        pts.append((x, y))
    # impulsions dorées qui circulent sur les routes
    for k in range(len(pts)):
        out.append(f'<circle class="pulse" r="2.4"><animateMotion dur="{3.2 + k * 0.5}s" repeatCount="indefinite"><mpath href="#r{k}"/></animateMotion></circle>')
    for k, ((x, y), c) in enumerate(zip(pts, t["cities"])):
        left = x < hx - 20
        tx = x - 9 if left else x + 9
        anchor = "end" if left else "start"
        out.append(
            f'<g class="city" tabindex="0" role="button" aria-pressed="false" aria-label="{c["name"]} : {c["region"]}">'
            f'<circle class="halo" cx="{x}" cy="{y}" r="13"/><circle class="pt" cx="{x}" cy="{y}" r="3.6"/>'
            f'<text x="{tx}" y="{y - 7}" text-anchor="{anchor}">{c["name"]}</text></g>')
    out.append(f'<circle class="hub-ring" cx="{hx}" cy="{hy}" r="9"/>')
    out.append(f'<circle class="hub" cx="{hx}" cy="{hy}" r="5"/>')
    out.append(f'<text class="hub-label" x="{hx + 13}" y="{hy + 17}">{HUB[0]}</text>')
    out.append("</svg>")
    return "\n".join(out)

def orbit_svg(t):
    c = 260
    out = ['<svg class="orbit" viewBox="0 0 520 520" role="img" aria-label="' + t["eco_title"] + '">',
           f'<circle class="ring" cx="{c}" cy="{c}" r="200"/>',
           f'<circle class="ring" cx="{c}" cy="{c}" r="120" stroke-dasharray="3 6"/>',
           f'<circle cx="{c}" cy="{c}" r="62" fill="#0a1014"/>',
           f'<image href="{t["base"]}assets/logo-light.svg" x="{c-40}" y="{c-34}" width="80" height="65"/>',
           '<g>']
    n = len(t["eco"])
    for k, (name, _, _) in enumerate(t["eco"]):
        a = -math.pi / 2 + k * 2 * math.pi / n
        x, y = c + 200 * math.cos(a), c + 200 * math.sin(a)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="#d0b983"/>')
    out.append("</g>")
    for k, (name, _, _) in enumerate(t["eco"]):
        a = -math.pi / 2 + k * 2 * math.pi / n
        x, y = c + 200 * math.cos(a), c + 200 * math.sin(a)
        ly = y - 22 if k == 0 else y + 34
        short = t["eco_short"][k]
        out.append(f'<text x="{x:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="16" font-weight="600" fill="#0a1014">{short}</text>')
    out.append("</svg>")
    return "\n".join(out)

T = {
"fr": dict(
    lang="fr", path="", locale="fr_FR", other_href="en/", other_label="English", base="",
    title="J2A Consulting | Structuration de projets, préparation au financement et accès au marché en Afrique de l'Ouest",
    desc="J2A Consulting, cabinet basé à Lomé, structure les projets, prépare les dossiers de financement et facilite l'accès aux marchés en Afrique de l'Ouest, en lien avec l'Europe, le Golfe, le Québec et l'Asie.",
    nav=[("#parcours", "Parcours"), ("#expertises", "Expertises"), ("#dirigeant", "Dirigeant"), ("#contact", "Contact")],
    h1_a="Nous préparons les projets africains", verbs=["au financement.", "à l'exécution.", "au marché."],
    lede="Depuis Lomé, J2A Consulting relie porteurs de projets, collectivités et investisseurs, et accompagne chaque projet de l'étude jusqu'à l'implantation.",
    cta1="Parler de votre projet", cta2="Voir le parcours",
    map_title="Les corridors de J2A Consulting au départ de Lomé",
    map_hint="Choisissez une ville pour voir ce que nous y faisons.",
    cities=[
        dict(name="Dakar", region="Afrique de l'Ouest et centrale", text="Notre terrain. Un réseau opérationnel dans une dizaine de pays, du Sénégal au Cameroun, pour étudier, prospecter et implanter."),
        dict(name="Paris", region="Europe", text="Acheteurs, importateurs, financeurs d'impact et diaspora : nous ouvrons les débouchés et les sources de financement."),
        dict(name="Montréal", region="Québec et Canada", text="Partenariats entre le Canada et l'Afrique de l'Ouest, missions d'entreprises et liens avec la diaspora."),
        dict(name="Dubaï", region="Golfe", text="Avec Growing Beyond Vision, basée à Sharjah, nous connectons les investisseurs du Golfe aux projets africains."),
        dict(name="Shanghai", region="Asie", text="Industriels, équipementiers et partenaires asiatiques qui veulent entrer sur le marché ouest-africain."),
    ],
    big="Un bon projet ne suffit pas. <b>Entre l'idée et le financement, il manque presque toujours un dossier.</b>",
    cols=["Le dossier au standard des banques et des fonds, la structure juridique claire, le plan par phases, les partenaires au bon endroit : c'est ce qui sépare un projet solide d'un projet financé.",
          "C'est ce chaînon que nous construisons, pour les entreprises, pour les investisseurs étrangers qui entrent sur le marché et pour les collectivités qui doivent transformer leurs besoins en projets finançables."],
    j_title="Le parcours d'un projet", j_intro="Quatre étapes, un seul interlocuteur, du premier diagnostic à l'installation sur le terrain.",
    steps=[("Étudier", "Nous validons le projet avant d'engager des moyens.", ["Étude de marché et faisabilité", "Identification des partenaires locaux", "Diagnostic go / no-go"]),
           ("Structurer", "Nous donnons au projet la forme qu'attendent les financeurs.", ["Montage juridique et gouvernance", "Phasage et modèle financier", "Contrats avec les acheteurs"]),
           ("Financer", "Nous préparons les dossiers et accompagnons la recherche de financement. La décision reste celle des financeurs.", ["Dossiers banque et investisseurs", "Banques locales, fonds, bailleurs", "Accompagnement des négociations"]),
           ("Implanter", "Nous restons aux côtés du projet sur le terrain.", ["Mise en œuvre et suivi", "Recrutement et partenaires", "Représentation locale"])],
    exp_title="Ce que nous faisons",
    exp=[("Agro-industrie", "De la parcelle au conteneur : nous structurons des filières complètes, de la production à l'export.", ["Contrats avec les acheteurs", "Certification et qualité", "Financement des campagnes", "Unités de transformation"]),
         ("Immobilier", "Projets résidentiels et mixtes, de la faisabilité au dossier bancaire.", ["Études de faisabilité", "Montage financier", "Dossiers bancaires", "Recherche d'investisseurs"]),
         ("Collectivités", "Nous aidons les communes à transformer leurs besoins en projets que les bailleurs peuvent financer.", ["Plans d'investissement", "Projets prioritaires", "Partenariats avec les bailleurs", "Visibilité internationale"]),
         ("Entrée sur le marché", "Pour les entreprises étrangères qui veulent tester l'Afrique de l'Ouest avant de s'y installer.", ["Veille et données de marché", "Partenaires et distributeurs", "Prospection active", "Représentation locale"])],
    m_title="J2A Market Access",
    m_text=["Se développer en Afrique de l'Ouest sans ouvrir tout de suite une filiale. Présence commerciale, connaissance du marché, opportunités qualifiées et représentation locale, activées par étapes selon les résultats.",
            "Pour les gouvernements, fonds souverains, family offices et groupes internationaux, nous montons aussi des mandats sur mesure."],
    ladder_label="Les quatre formules",
    tiers=[dict(name="Découvrir", short="Tester", text="Tester le marché : présence, premières données et premiers contacts, sans engagement lourd."),
           dict(name="Connecter", short="Réseau", text="Construire un réseau qualifié de partenaires, de distributeurs et de prescripteurs."),
           dict(name="Développer", short="Ventes", text="Accélérer les ventes avec une prospection active et un suivi des opportunités."),
           dict(name="S'implanter", short="Présence", text="Installer une présence durable, avec une représentation locale quand les résultats le justifient.")],
    quote="« Entrer sur un nouveau marché ne devrait jamais commencer par l'ouverture d'un bureau. »",
    lead_title="Le dirigeant", lead_name="Yaovi Kokodoko", lead_role="Directeur général, J2A Consulting",
    lead=["Yaovi Kokodoko structure des projets et des financements entre l'Afrique de l'Ouest, l'Europe, le Golfe, le Québec et l'Asie. Il travaille avec des entreprises, des investisseurs et des collectivités, en agro-industrie, en immobilier et en développement institutionnel.",
          "Il est cofondateur de Growing Beyond Vision, gérant d'Ipomoea Africa et président de l'Association Togolaise de la Franchise."],
    lead_quote="« Mon métier, c'est de rendre un projet lisible pour ceux qui doivent le financer, sans lui faire perdre ce qui le rend juste pour le terrain. »",
    photo_alt="Portrait de Yaovi Kokodoko",
    eco_title="L'écosystème J2A", eco_short=["Ipomoea Africa", "GBV", "Franchise Togo"],
    eco_intro="J2A est au centre d'un ensemble de projets et de partenaires qui se renforcent les uns les autres.",
    eco=[("Ipomoea Africa", "https://ipomoea.africa", "Production et export agro-industriels au Togo, construits par phases."),
         ("Growing Beyond Vision", None, "Architecture d'investissement pour l'Afrique, depuis Sharjah."),
         ("Association Togolaise de la Franchise", None, "La franchise comme levier de développement des entreprises au Togo.")],
    say="Parlons de votre projet.", c_intro="Un premier échange de trente minutes suffit pour savoir comment nous pouvons vous aider.",
    c_tel="Téléphone", c_where="Bureau", where="Lomé, Togo", c_li="LinkedIn",
    rights="J2A Consulting SARL, Lomé, République togolaise",
),
"en": dict(
    lang="en", path="en/", locale="en_GB", other_href="../", other_label="Français", base="../",
    title="J2A Consulting | Project structuring, financing readiness and market access in West Africa",
    desc="J2A Consulting, based in Lomé, structures projects, prepares financing files and facilitates market access in West Africa, with links to Europe, the Gulf, Quebec and Asia.",
    nav=[("#parcours", "Journey"), ("#expertises", "Expertise"), ("#dirigeant", "Leadership"), ("#contact", "Contact")],
    h1_a="We get African projects ready", verbs=["for financing.", "for execution.", "for market."],
    lede="From Lomé, J2A Consulting connects project owners, local governments and investors, and stays with each project from first study to implementation.",
    cta1="Discuss your project", cta2="See the journey",
    map_title="J2A Consulting's corridors from Lomé",
    map_hint="Pick a city to see what we do there.",
    cities=[
        dict(name="Dakar", region="West and Central Africa", text="Our home ground. An operational network across some ten countries, from Senegal to Cameroon, to study, prospect and set up."),
        dict(name="Paris", region="Europe", text="Buyers, importers, impact investors and the diaspora: we open markets and sources of financing."),
        dict(name="Montréal", region="Quebec and Canada", text="Canada–West Africa partnerships, business missions and diaspora links."),
        dict(name="Dubai", region="The Gulf", text="With Growing Beyond Vision, based in Sharjah, we connect Gulf investors with African projects."),
        dict(name="Shanghai", region="Asia", text="Manufacturers, equipment suppliers and Asian partners entering the West African market."),
    ],
    big="A good project is not enough. <b>Between the idea and the financing, what is missing is almost always a file.</b>",
    cols=["A file that meets bank and fund standards, a clear legal structure, a phased plan, the right partners in the right place: that is what separates a sound project from a financed one.",
          "That missing link is what we build, for companies, for foreign investors entering the market, and for local governments that need to turn their needs into financeable projects."],
    j_title="A project's journey", j_intro="Four steps, one partner, from the first diagnosis to operations on the ground.",
    steps=[("Study", "We validate the project before committing resources.", ["Market and feasibility study", "Local partner identification", "Go / no-go diagnosis"]),
           ("Structure", "We shape the project the way financiers expect it.", ["Legal set-up and governance", "Phasing and financial model", "Buyer contracts"]),
           ("Finance", "We prepare the files and support the search for financing. The decision remains with the financiers.", ["Bank and investor files", "Local banks, funds, donors", "Negotiation support"]),
           ("Implement", "We stay with the project on the ground.", ["Execution and monitoring", "Hiring and partners", "Local representation"])],
    exp_title="What we do",
    exp=[("Agribusiness", "From the field to the container: we structure complete value chains, from production to export.", ["Buyer contracts", "Certification and quality", "Seasonal financing", "Processing units"]),
         ("Real estate", "Residential and mixed-use projects, from feasibility to the bank file.", ["Feasibility studies", "Financial structuring", "Bank files", "Investor search"]),
         ("Local governments", "We help municipalities turn their needs into projects that donors can finance.", ["Investment plans", "Priority projects", "Donor partnerships", "International visibility"]),
         ("Market entry", "For foreign companies that want to test West Africa before setting up.", ["Market intelligence", "Partners and distributors", "Active business development", "Local representation"])],
    m_title="J2A Market Access",
    m_text=["Grow in West Africa without opening a subsidiary right away. Commercial presence, market intelligence, qualified opportunities and local representation, activated step by step as results come in.",
            "For governments, sovereign funds, family offices and multinationals, we also structure bespoke mandates."],
    ladder_label="The four tiers",
    tiers=[dict(name="Discover", short="Test", text="Test the market: presence, first data and first contacts, with no heavy commitment."),
           dict(name="Connect", short="Network", text="Build a qualified network of partners, distributors and influencers."),
           dict(name="Grow", short="Sales", text="Accelerate sales with active business development and opportunity tracking."),
           dict(name="Establish", short="Presence", text="Set up a lasting presence, with local representation once results justify it.")],
    quote="“Entering a new market should never begin with opening an office.”",
    lead_title="Leadership", lead_name="Yaovi Kokodoko", lead_role="Managing Director, J2A Consulting",
    lead=["Yaovi Kokodoko structures projects and financing across West Africa, Europe, the Gulf, Quebec and Asia. He works with companies, investors and local governments in agribusiness, real estate and institutional development.",
          "He is co-founder of Growing Beyond Vision, managing director of Ipomoea Africa and president of the Togolese Franchise Association."],
    lead_quote="“My job is to make a project readable for those who have to finance it, without losing what makes it right for the ground.”",
    photo_alt="Portrait of Yaovi Kokodoko",
    eco_title="The J2A ecosystem", eco_short=["Ipomoea Africa", "GBV", "Franchise Togo"],
    eco_intro="J2A sits at the centre of a set of projects and partners that strengthen one another.",
    eco=[("Ipomoea Africa", "https://ipomoea.africa", "Agro-industrial production and export in Togo, built in phases."),
         ("Growing Beyond Vision", None, "Investment architecture for Africa, from Sharjah."),
         ("Togolese Franchise Association", None, "Franchising as a growth lever for businesses in Togo.")],
    say="Let's talk about your project.", c_intro="A first thirty-minute conversation is enough to see how we can help.",
    c_tel="Phone", c_where="Office", where="Lomé, Togo", c_li="LinkedIn",
    rights="J2A Consulting SARL, Lomé, Togolese Republic",
),
}

SITE = "https://j2a4510.github.io/j2a-consulting/"  # à remplacer par le nom de domaine définitif

def page(t):
    b = t["base"]
    nav = "".join(f'<a href="{h}">{l}</a>' for h, l in t["nav"])
    cols = "".join(f"<p>{p}</p>" for p in t["cols"])
    panels = "".join(
        f'<article class="panel"><div class="n" aria-hidden="true">{i}</div><h3>{h}</h3><p>{p}</p>'
        + "<ul>" + "".join(f"<li>{x}</li>" for x in li) + "</ul></article>"
        for i, (h, p, li) in enumerate(t["steps"], 1))
    tabs = "".join(
        f'<button class="tab" role="tab" id="tab{k}" aria-controls="tp{k}" aria-selected="{"true" if k == 0 else "false"}" tabindex="{0 if k == 0 else -1}">{h}</button>'
        for k, (h, _, _) in enumerate(t["exp"]))
    tps = "".join(
        f'<div class="tabpanel" role="tabpanel" id="tp{k}" aria-labelledby="tab{k}"{"" if k == 0 else " hidden"}>'
        f'<p class="lead-in">{p}</p><ul>' + "".join(f"<li>{x}</li>" for x in li) + "</ul></div>"
        for k, (_, p, li) in enumerate(t["exp"]))
    rungs = "".join(f'<button class="rung" aria-pressed="false">{x["name"]}<small>{x["short"]}</small></button>' for x in t["tiers"])
    mtext = "".join(f"<p>{p}</p>" for p in t["m_text"])
    lead = "".join(f"<p>{p}</p>" for p in t["lead"])
    eco = "".join(
        '<div class="eco-item"><h3>' + (f'<a href="{u}" rel="noopener">{n}</a>' if u else n) + f'</h3><p>{p}</p></div>'
        for n, u, p in t["eco"])
    data = json.dumps(dict(verbs=t["verbs"], cities=t["cities"], tiers=t["tiers"]), ensure_ascii=False)
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<link rel="canonical" href="{SITE}{t['path']}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{t['path']}">
<meta property="og:locale" content="{t['locale']}">
<meta property="og:site_name" content="J2A Consulting">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:title" content="{t['title']}">
<meta property="og:description" content="{t['desc']}">
<meta property="og:image" content="{SITE}assets/share.jpg">
<link rel="alternate" hreflang="fr" href="{SITE}">
<link rel="alternate" hreflang="en" href="{SITE}en/">
<link rel="alternate" hreflang="x-default" href="{SITE}">
<link rel="icon" href="{b}assets/logo.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@200;300;400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{b}assets/style.css">
</head>
<body>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="{b if b else './'}"><img src="{b}assets/logo-light.svg" alt="J2A Consulting"></a>
    <button class="menu-btn" aria-expanded="false" aria-controls="mainnav"><span class="sr">Menu</span><i></i><i></i></button>
    <nav class="nav" id="mainnav" aria-label="Navigation">{nav}<a class="lang" href="{t['other_href']}" lang="{'en' if t['lang'] == 'fr' else 'fr'}">{t['other_label']}</a></nav>
  </div>
</header>

<main>
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>{t['h1_a']} <span class="verb"><span>{t['verbs'][0]}</span></span></h1>
      <p class="lede">{t['lede']}</p>
      <div class="cta-row">
        <a class="btn btn-gold" href="#contact">{t['cta1']}</a>
        <a class="btn btn-ghost" href="#parcours">{t['cta2']}</a>
      </div>
    </div>
    <div class="corridor">
      {corridor_svg(t)}
      <div class="corridor-card" aria-live="polite"></div>
      <div class="corridor-hint">{t['map_hint']}</div>
    </div>
  </div>
  <div class="scroll-cue" aria-hidden="true"></div>
</section>

<section class="manifesto">
  <div class="wrap">
    <p class="big">{t['big']}</p>
    <div class="cols">{cols}</div>
  </div>
</section>

<section class="journey" id="parcours">
  <div class="wrap journey-head">
    <h2>{t['j_title']}</h2>
    <p>{t['j_intro']}</p>
  </div>
  <div class="journey-pin">
    <div class="journey-stage">
      <div class="wrap">
        <div class="track-line" aria-hidden="true"><i></i></div>
        <div class="panels">{panels}</div>
      </div>
    </div>
  </div>
</section>

<section class="expertise" id="expertises">
  <div class="wrap">
    <h2>{t['exp_title']}</h2>
    <div class="switcher">
      <div class="tabs" role="tablist" aria-label="{t['exp_title']}">{tabs}</div>
      <div>{tps}</div>
    </div>
  </div>
</section>

<section class="market">
  <div class="wrap market-grid">
    <div>
      <h2>{t['m_title']}</h2>
      <div style="margin-top:24px">{mtext}</div>
      <p class="quote">{t['quote']}</p>
    </div>
    <div class="ladder">
      <div class="ladder-steps" role="group" aria-label="{t['ladder_label']}">{rungs}</div>
      <div class="ladder-copy" aria-live="polite"></div>
    </div>
  </div>
</section>

<section class="leader" id="dirigeant">
  <div class="leader-grid">
    <div class="portrait"><img src="{b}assets/yaovi.jpg" alt="{t['photo_alt']}" loading="lazy" width="900" height="1125"></div>
    <div class="leader-text">
      <h2 class="sr">{t['lead_title']}</h2>
      <div class="name">{t['lead_name']}</div>
      <div class="role">{t['lead_role']}</div>
      {lead}
      <blockquote>{t['lead_quote']}</blockquote>
    </div>
  </div>
</section>

<section class="eco">
  <div class="wrap">
    <h2>{t['eco_title']}</h2>
    <div class="eco-grid">
      {orbit_svg(t)}
      <div>
        <p>{t['eco_intro']}</p>
        <div class="eco-list">{eco}</div>
      </div>
    </div>
  </div>
</section>
</main>

<footer class="contact" id="contact">
  <div class="wrap">
    <div class="say">{t['say']}</div>
    <p style="color:#b9c6cb;margin-top:22px">{t['c_intro']}</p>
    <a class="mail" href="mailto:ykstrategic@proton.me">ykstrategic@proton.me</a>
    <div class="contact-meta">
      <div><span>{t['c_tel']}</span><a href="tel:+22871527976">+228 71 52 79 76</a></div>
      <div><span>{t['c_where']}</span>{t['where']}</div>
    </div>
    <div class="foot">
      <img src="{b}assets/logo-light.svg" alt="">
      <div>© 2026 {t['rights']}</div>
    </div>
  </div>
</footer>
<script type="application/json" id="site-data">{data}</script>
<script src="{b}assets/app.js" defer></script>
</body>
</html>
"""

(ROOT / "index.html").write_text(page(T["fr"]), encoding="utf-8")
(ROOT / "en" / "index.html").write_text(page(T["en"]), encoding="utf-8")
print("ok")
