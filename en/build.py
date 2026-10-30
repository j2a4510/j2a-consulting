"""Génère les pages FR et EN du site J2A Consulting à partir d'un seul gabarit.
Usage : python3 build.py
"""
import json, math, pathlib, hashlib

ROOT = pathlib.Path(__file__).parent
VER = hashlib.md5((ROOT / "assets/style.css").read_bytes() + (ROOT / "assets/app.js").read_bytes()).hexdigest()[:8]

def xy(lon, lat):
    """Projection équirectangulaire simple (lon, lat) -> (x, y) sur 1000 x 500."""
    return round((lon + 180) / 360 * 1000, 1), round((90 - lat) / 180 * 500, 1)

HUB = ("Lomé", 1.22, 6.13)
# Dakar, Conakry, Casablanca, Paris, Londres, Montréal, Dubaï, Shanghai, Bangkok, Singapour, Sydney
COORDS = [(-17.45, 14.69), (-13.71, 9.51), (-7.59, 33.57), (2.35, 48.86), (-0.13, 51.51), (-73.57, 45.50),
          (55.30, 25.27), (121.47, 31.23), (100.50, 13.75), (103.82, 1.35), (151.21, -33.87)]
# Position de l'étiquette de chaque ville : côté ("l" gauche, "r" droite) et décalage vertical
LABELS = [("l", -7), ("l", 16), ("l", -7), ("r", -7), ("l", -7), ("l", -7),
          ("r", -7), ("r", -7), ("r", -7), ("r", 16), ("l", -7)]

def corridor_svg(t):
    hx, hy = xy(HUB[1], HUB[2])
    out = [f'<svg viewBox="236 84 690 278" role="group" aria-label="{t["map_title"]}">']
    for gx in range(242, 926, 16):
        for gy in range(90, 362, 16):
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
        side, dy = LABELS[k]
        left = side == "l"
        tx = round(x - 9 if left else x + 9, 1)
        anchor = "end" if left else "start"
        out.append(
            f'<g class="city" tabindex="0" role="button" aria-pressed="false" aria-label="{c["name"]} : {c["region"]}">'
            f'<circle class="halo" cx="{x}" cy="{y}" r="13"/><circle class="pt" cx="{x}" cy="{y}" r="3.6"/>'
            f'<text x="{tx}" y="{round(y + dy, 1)}" text-anchor="{anchor}">{c["name"]}</text></g>')
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
    skip="Aller au contenu",
    title="J2A Consulting | Structuration de projets, préparation au financement et accès au marché en Afrique de l'Ouest",
    desc="J2A Consulting, cabinet basé à Lomé, structure les projets, prépare les dossiers de financement et facilite l'accès aux marchés en Afrique de l'Ouest, en lien avec l'Europe, le Golfe, le Québec et l'Asie.",
    nav=[("#parcours", "Parcours"), ("#expertises", "Expertises"), ("#filieres", "Filières"), ("#dirigeant", "Dirigeant"), ("#contact", "Contact")],
    h1='Nous préparons les projets africains <span class="g">au financement, à l\'exécution et au marché.</span>',
    proof=[("Structuration", "Projets phasés, montages juridiques et financiers, modèles au standard des financeurs."), ("Partenariats", "Acheteurs, investisseurs, bailleurs et partenaires locaux, réunis autour d\'un même projet."), ("Accès au marché", "Un réseau opérationnel en Afrique de l\'Ouest, relié à l\'Europe, au Maghreb, au Golfe, au Canada, à l\'Asie et à l\'Australie.")],
    eco_roles=["Exécution opérationnelle", "Industrialisation et partenariats internationaux", "Réseau institutionnel"],
    h1_a="Nous préparons les projets africains", verbs=["au financement.", "à l'exécution.", "au marché."],
    lede="Depuis Lomé, J2A Consulting relie porteurs de projets, collectivités et investisseurs, et accompagne chaque projet de l'étude jusqu'à l'implantation.",
    cta1="Parler de votre projet", cta2="Voir le parcours",
    figs_label="J2A en chiffres",
    figs=[("11", "corridors internationaux, de Dakar à Sydney"),
          ("4", "domaines d'expertise : agro-industrie, immobilier, collectivités, entrée sur le marché"),
          ("300 ha", "de filière d'export bio en structuration au Togo"),
          ("48 h", "pour une première réponse à votre projet")],
    map_title="Les corridors de J2A Consulting au départ de Lomé",
    map_hint="Choisissez une ville pour voir ce que nous y faisons.",
    port_alt="Porte-conteneurs et grues au port de Lomé, vus depuis la plage", port_cap="Le port de Lomé, point de départ de nos corridors.", port_credit="Photo :",
    consult_kicker="Premier échange offert", consult_title="30 minutes pour faire le point sur votre projet",
    consult_lede="Un premier échange en visioconférence ou à Lomé, sans engagement. Décrivez votre projet en deux minutes : nous revenons vers vous sous 48 heures ouvrées pour fixer le rendez-vous.",
    consult_cta="Réserver mon premier échange",
    consult_get_title="Ce que vous en retirez",
    consult_get=["Un regard extérieur sur votre projet, ses atouts et ses points de vigilance", "Les prochaines étapes concrètes, dans le bon ordre", "Une indication claire de ce que J2A peut faire pour vous, ou non"],
    consult_note="Pour bien préparer l'échange, nous vous demandons le type de projet, le pays et son stade d'avancement : idée, étude ou recherche de financement.",
    corr_title="Nos corridors", corr_intro="Lomé au centre, onze destinations. Chacune correspond à un type de partenaires que nous mobilisons pour vos projets.",
    cities=[
        dict(name="Dakar", region="Afrique de l'Ouest francophone", text="Notre terrain. Un réseau opérationnel dans une dizaine de pays, du Sénégal au Cameroun, pour étudier, prospecter et implanter."),
        dict(name="Conakry", region="Guinée", text="Un marché en forte croissance, où nous accompagnons des projets et des partenaires locaux."),
        dict(name="Casablanca", region="Maroc", text="Ingénierie et études avec nos partenaires marocains, et passerelle vers les investisseurs et les industriels du Royaume."),
        dict(name="Paris", region="France", text="Acheteurs, importateurs, financeurs d'impact et diaspora : nous ouvrons les débouchés et les sources de financement."),
        dict(name="Londres", region="Royaume-Uni", text="Investisseurs, fonds d'impact et institutions financières, et liens avec la diaspora."),
        dict(name="Montréal", region="Canada et Québec", text="Partenariats entre le Canada et l'Afrique de l'Ouest, missions d'entreprises et liens avec la diaspora."),
        dict(name="Dubaï", region="Golfe", text="Investisseurs et fonds du Golfe intéressés par les projets africains."),
        dict(name="Shanghai", region="Chine", text="Industriels, équipementiers et partenaires chinois qui veulent entrer sur le marché ouest-africain."),
        dict(name="Bangkok", region="Thaïlande", text="Fournisseurs, technologies agro-industrielles et partenaires commerciaux pour les filières africaines."),
        dict(name="Singapour", region="Singapour", text="Avec Lean Hub Asia et Growing Beyond Vision, nous portons des projets de transformation locale des ressources africaines."),
        dict(name="Sydney", region="Australie", text="Investisseurs et entreprises australiens intéressés par l'Afrique de l'Ouest, notamment dans l'agriculture et les ressources."),
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
         ("Entrée sur le marché", "Pour les entreprises étrangères qui veulent tester l'Afrique de l'Ouest avant de s'y installer.", ["Veille et données de marché", "Partenaires et distributeurs", "Prospection active", "Représentation locale"]),
         ("IA et entrepreneuriat", "Nous appliquons l'intelligence artificielle et les méthodes d'entrepreneuriat aux projets, avec des partenaires spécialisés.", ["Planification et simulation par l'IA", "Programmes d'incubation", "Mentorat assisté par l'IA", "Formation des équipes"])],
    agro_kicker="Coopératives et filières agricoles",
    agro_title="Des coopératives prêtes à vendre et à être financées",
    agro_lede="Les coopératives et les associations villageoises ont la terre et le savoir-faire. Il leur manque souvent un acheteur sous contrat, une organisation reconnue et un accès au financement. Nous faisons le lien, du diagnostic au suivi des campagnes.",
    agro_photo_alt="Réunion d'échange avec des producteurs sous une paillote, au Togo", agro_photo_cap="Échange avec des producteurs, au Togo.",
    band_alt="Parcelles en végétation naturelle sous un ciel lumineux, au Togo", band_cap="Sur le terrain, au Togo.",
    agro=[("Diagnostic et notation", "Statut, foncier, gouvernance, volumes, comptes. Chaque coopérative reçoit une note A, B ou C : ce qui est finançable aujourd'hui, et ce qui reste à construire."),
          ("Structuration", "Mise en conformité avec l'Acte uniforme OHADA, gouvernance, comptabilité simple et formation des gérants."),
          ("Certification et contrôle interne", "Préparation à la certification bio de groupe et tenue du système de contrôle interne exigé par les organismes certificateurs."),
          ("Mise en marché", "Recherche d'acheteurs et contrats d'achat : volumes, qualité, prix plancher et primes."),
          ("Financement des campagnes", "Crédit de campagne adossé aux contrats, warrantage, garanties et subventions. Les fonds sont versés directement aux coopératives."),
          ("Suivi pour les financeurs", "Des rapports réguliers sur les livraisons, les stocks et les remboursements, pour que chacun sache où en est la campagne.")],
    agro_who_title="Avec qui nous travaillons",
    agro_who=[("Coopératives et unions", "Un débouché sûr et un accès au crédit."),
              ("Acheteurs et exportateurs", "Des volumes réguliers, traçables et certifiés."),
              ("Bailleurs et fonds d'impact", "Des dossiers solides et un relais sur le terrain."),
              ("Communes", "Des pôles agricoles qui créent des emplois pour les jeunes.")],
    agro_rule="<b>Notre règle :</b> nous ne gérons jamais les fonds. Les financements vont aux coopératives, les contrats sont signés entre les parties, et notre rémunération est connue de tous.",
    agro_cta="Présenter une coopérative ou une filière", agro_subject="Coopérative ou filière à accompagner",
    case_title="Sur notre table en ce moment",
    case_name="Une filière agro-industrielle d'export, au Togo",
    case_lede="Du foncier et un acheteur européen intéressé, mais ni plan de financement, ni certification, ni organisation de production. Voici où en est le dossier.",
    case_steps=[("Fait", "Projet découpé en phases, de l'export du frais à la transformation"), ("Fait", "Dossiers distincts pour les banques locales et pour les fonds"), ("En cours", "Programme d'expéditions et contrat cadre avec l'importateur"), ("En cours", "Certification bio par un organisme reconnu par l'UE")],
    case_more="D'autres dossiers en immobilier, auprès de collectivités et en entrée sur le marché sont présentés sur demande, sous accord de confidentialité.",
    case_cta="Recevoir une présentation détaillée", case_subject="Demande de présentation détaillée",
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
    partners_title="Nos partenaires", partners_link="Voir le site",
    partners=[("Lean Hub Asia", "https://www.leanhubasia.com/", "Singapour", "Cabinet de transformation B2B, du lean au numérique, pour l'industrie, les infrastructures et la chaîne logistique."),
              ("InnovNation", "https://innovnation.ai/", "IA et entrepreneuriat", "Plateforme d'entrepreneuriat fondée sur l'IA pour les universités, les gouvernements et les incubateurs. Avec Lean Hub Asia, J2A en porte un projet de déploiement en Afrique de l'Ouest francophone."),
              ("SIMCEL", "https://www.simcel.io/", "IA et planification", "Plateforme de planification intégrée par l'IA et les jumeaux numériques. J2A accompagne son développement en Afrique de l'Ouest."),
              ("CEFAAT-SFER", None, "Togo", "Centrale entrepreneuriale et des filières agricoles : foncier agricole et programmes de production au Togo.")],
    eco=[("Ipomoea Africa", "https://ipomoea.africa", "Production et export agro-industriels au Togo, construits par phases."),
         ("Growing Beyond Vision", "https://www.growingbeyondvision.com/", "Transformer les ressources africaines en Afrique, avec Lean Hub Asia (Singapour)."),
         ("Association Togolaise de la Franchise", None, "La franchise comme levier de développement des entreprises au Togo.")],
    form_cta="Présenter mon projet", or_mail="Ou écrivez-nous directement :",
    say="Parlons de votre projet.", c_intro="Décrivez votre projet en deux minutes. Nous revenons vers vous sous 48 heures ouvrées pour convenir d'un premier échange.",
    c_tel="Téléphone", c_where="Bureau", where="Lomé, Togo", c_li="LinkedIn",
    rights="J2A Consulting SARL, Lomé, République togolaise",
),
 "en": dict(
    lang="en", path="en/", locale="en_GB", other_href="../", other_label="Français", base="../",
    skip="Skip to content",
    title="J2A Consulting | Project structuring, financing readiness and market access in West Africa",
    desc="J2A Consulting, based in Lomé, structures projects, prepares financing files and facilitates market access in West Africa, with links to Europe, the Gulf, Quebec and Asia.",
    nav=[("#parcours", "Journey"), ("#expertises", "Expertise"), ("#filieres", "Value chains"), ("#dirigeant", "Leadership"), ("#contact", "Contact")],
    h1='We get African projects <span class="g">ready for financing, execution and market.</span>',
    proof=[("Structuring", "Phased projects, legal and financial set-ups, models built to financier standards."), ("Partnerships", "Buyers, investors, donors and local partners, brought together around one project."), ("Market access", "An operational network in West Africa, connected to Europe, North Africa, the Gulf, Canada, Asia and Australia.")],
    eco_roles=["Operational execution", "Industrialisation and international partnerships", "Institutional network"],
    h1_a="We get African projects ready", verbs=["for financing.", "for execution.", "for market."],
    lede="From Lomé, J2A Consulting connects project owners, local governments and investors, and stays with each project from first study to implementation.",
    cta1="Discuss your project", cta2="See the journey",
    figs_label="J2A in figures",
    figs=[("11", "international corridors, from Dakar to Sydney"),
          ("4", "areas of expertise: agribusiness, real estate, local governments, market entry"),
          ("300 ha", "organic export value chain being structured in Togo"),
          ("48 h", "for a first answer on your project")],
    map_title="J2A Consulting's corridors from Lomé",
    map_hint="Pick a city to see what we do there.",
    port_alt="Container ships and cranes at the port of Lomé, seen from the beach", port_cap="The port of Lomé, where our corridors begin.", port_credit="Photo:",
    consult_kicker="First conversation, on us", consult_title="30 minutes to take stock of your project",
    consult_lede="A first conversation by video call or in Lomé, with no commitment. Describe your project in two minutes: we get back to you within two working days to set the appointment.",
    consult_cta="Book my first conversation",
    consult_get_title="What you take away",
    consult_get=["An outside view of your project, its strengths and the points to watch", "The next concrete steps, in the right order", "A clear sense of what J2A can do for you, or not"],
    consult_note="To prepare the conversation well, we ask for the type of project, the country and its stage: idea, study or financing search.",
    corr_title="Our corridors", corr_intro="Lomé at the centre, eleven destinations. Each one stands for a type of partner we bring to your projects.",
    cities=[
        dict(name="Dakar", region="French-speaking West Africa", text="Our home ground. An operational network across some ten countries, from Senegal to Cameroon, to study, prospect and set up."),
        dict(name="Conakry", region="Guinea", text="A fast-growing market where we support projects and local partners."),
        dict(name="Casablanca", region="Morocco", text="Engineering and studies with our Moroccan partners, and a bridge to the Kingdom's investors and manufacturers."),
        dict(name="Paris", region="France", text="Buyers, importers, impact investors and the diaspora: we open markets and sources of financing."),
        dict(name="London", region="United Kingdom", text="Investors, impact funds and financial institutions, and links with the diaspora."),
        dict(name="Montréal", region="Canada and Quebec", text="Canada–West Africa partnerships, business missions and diaspora links."),
        dict(name="Dubai", region="The Gulf", text="Gulf investors and funds interested in African projects."),
        dict(name="Shanghai", region="China", text="Manufacturers, equipment suppliers and Chinese partners entering the West African market."),
        dict(name="Bangkok", region="Thailand", text="Suppliers, agro-processing technology and trading partners for African value chains."),
        dict(name="Singapore", region="Singapore", text="With Lean Hub Asia and Growing Beyond Vision, we develop projects that process African resources locally."),
        dict(name="Sydney", region="Australia", text="Australian investors and companies interested in West Africa, notably in agriculture and natural resources."),
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
         ("Market entry", "For foreign companies that want to test West Africa before setting up.", ["Market intelligence", "Partners and distributors", "Active business development", "Local representation"]),
         ("AI and entrepreneurship", "We apply artificial intelligence and entrepreneurship methods to projects, with specialised partners.", ["AI planning and simulation", "Incubation programmes", "AI-assisted mentoring", "Team training"])],
    agro_kicker="Cooperatives and agricultural value chains",
    agro_title="Cooperatives ready to sell and to be financed",
    agro_lede="Cooperatives and village associations have the land and the know-how. What they usually lack is a buyer under contract, a recognised organisation and access to finance. We make the link, from the first diagnosis to monitoring each season.",
    agro_photo_alt="Meeting with farmers under a thatched shelter, Togo", agro_photo_cap="Meeting with farmers in Togo.",
    band_alt="Land under natural vegetation beneath a bright sky, Togo", band_cap="In the field, Togo.",
    agro=[("Diagnosis and rating", "Legal status, land, governance, volumes, accounts. Each cooperative gets an A, B or C rating: what can be financed today, and what still needs to be built."),
          ("Structuring", "Compliance with the OHADA Uniform Act on cooperatives, governance, simple bookkeeping and manager training."),
          ("Certification and internal control", "Preparation for group organic certification and running the internal control system that certification bodies require."),
          ("Market access", "Finding buyers and drafting purchase contracts: volumes, quality, floor prices and premiums."),
          ("Seasonal financing", "Crop finance backed by purchase contracts, warehouse receipts, guarantees and grants. Funds go directly to the cooperatives."),
          ("Reporting to financiers", "Regular reports on deliveries, stocks and repayments, so everyone knows where the season stands.")],
    agro_who_title="Who we work with",
    agro_who=[("Cooperatives and unions", "A secure market and access to credit."),
              ("Buyers and exporters", "Regular, traceable and certified volumes."),
              ("Donors and impact funds", "Sound files and a partner on the ground."),
              ("Municipalities", "Agricultural hubs that create jobs for young people.")],
    agro_rule="<b>Our rule:</b> we never handle the funds. Financing goes to the cooperatives, contracts are signed between the parties, and our fees are disclosed to everyone.",
    agro_cta="Present a cooperative or a value chain", agro_subject="Cooperative or value chain to support",
    case_title="On our desk right now",
    case_name="An agro-industrial export value chain in Togo",
    case_lede="Land and an interested European buyer, but no financing plan, no certification and no production organisation. Here is where the file stands.",
    case_steps=[("Done", "Project broken into phases, from fresh export to processing"), ("Done", "Separate files for local banks and for investment funds"), ("In progress", "Shipping programme and framework contract with the importer"), ("In progress", "Organic certification by an EU-recognised body")],
    case_more="Other files in real estate, with local governments and in market entry are presented on request, under a confidentiality agreement.",
    case_cta="Request a detailed presentation", case_subject="Request for a detailed presentation",
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
    partners_title="Our partners", partners_link="Visit website",
    partners=[("Lean Hub Asia", "https://www.leanhubasia.com/", "Singapore", "B2B transformation consultancy, from lean to digital, for industry, infrastructure and supply chains."),
              ("InnovNation", "https://innovnation.ai/", "AI and entrepreneurship", "An AI-native entrepreneurship platform for universities, governments and incubators. With Lean Hub Asia, J2A is leading a plan to roll it out across French-speaking West Africa."),
              ("SIMCEL", "https://www.simcel.io/", "AI and planning", "An integrated business planning platform built on AI and digital twins. J2A supports its development in West Africa."),
              ("CEFAAT-SFER", None, "Togo", "An agricultural business and value-chain hub: farmland and production programmes in Togo.")],
    eco=[("Ipomoea Africa", "https://ipomoea.africa", "Agro-industrial production and export in Togo, built in phases."),
         ("Growing Beyond Vision", "https://www.growingbeyondvision.com/", "Processing African resources in Africa, with Lean Hub Asia (Singapore)."),
         ("Togolese Franchise Association", None, "Franchising as a growth lever for businesses in Togo.")],
    form_cta="Present my project", or_mail="Or write to us directly:",
    say="Let's talk about your project.", c_intro="Describe your project in two minutes. We get back to you within two working days to arrange a first conversation.",
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
    csteps = "".join(f'<li><span class="st{" st-on" if k < 2 else ""}">{a}</span>{b}</li>' for k, (a, b) in enumerate(t["case_steps"]))
    mtext = "".join(f"<p>{p}</p>" for p in t["m_text"])
    lead = "".join(f"<p>{p}</p>" for p in t["lead"])
    eco = "".join(
        '<div class="eco-item"><h3>' + (f'<a href="{u}" rel="noopener">{n}</a>' if u else n) + f'</h3><p>{p}</p></div>'
        for n, u, p in t["eco"])
    proof = "".join(f'<div class="proof-item"><h3>{h}</h3><p>{p}</p></div>' for h, p in t["proof"])
    vsteps = "".join(
        f'<li><span class="n" aria-hidden="true">{i}</span><div><h3>{h}</h3><p>{p}</p><ul>' + "".join(f"<li>{x}</li>" for x in li) + "</ul></div></li>"
        for i, (h, p, li) in enumerate(t["steps"], 1))
    expg = "".join(
        f'<article class="exp-card"><h3>{h}</h3><p>{p}</p><ul>' + "".join(f"<li>{x}</li>" for x in li) + "</ul></article>"
        for h, p, li in t["exp"])
    agro = "".join(
        f'<li><span class="n" aria-hidden="true">{i:02d}</span><h3>{h}</h3><p>{p}</p></li>'
        for i, (h, p) in enumerate(t["agro"], 1))
    consult_get = "".join(f"<li>{x}</li>" for x in t["consult_get"])
    partners = "".join(
        f'<article class="partner"><span class="role">{r}</span><h4>{n}</h4><p>{p}</p>'
        + (f'<a class="partner-link" href="{u}" target="_blank" rel="noopener">{t["partners_link"]} <span aria-hidden="true">↗</span></a>' if u else "")
        + "</article>"
        for n, u, r, p in t["partners"])
    figs = "".join(f"<div><dt>{n}</dt><dd>{d}</dd></div>" for n, d in t["figs"])
    agro_who = "".join(f"<div><h3>{h}</h3><p>{p}</p></div>" for h, p in t["agro_who"])
    eco3 = "".join(
        f'<div class="eco-col"><span class="role">{r}</span><h3>' + (f'<a href="{u}" rel="noopener">{n}</a>' if u else n) + f'</h3><p>{p}</p></div>'
        for (n, u, p), r in zip(t["eco"], t["eco_roles"]))
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
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,300;1,9..144,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{b}assets/style.css?v={VER}">
</head>
<body>
<a class="skip-link" href="#main">{t['skip']}</a>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="{b if b else './'}"><img src="{b}assets/logo.svg" alt="J2A Consulting"></a>
    <button class="menu-btn" aria-expanded="false" aria-controls="mainnav"><span class="sr">Menu</span><i></i><i></i></button>
    <nav class="nav" id="mainnav" aria-label="Navigation">{nav}<a class="nav-cta" href="https://tally.so/r/rDD17N" data-tally-open="rDD17N" data-tally-layout="modal" data-tally-width="640" data-tally-emoji-animation="none">{t['form_cta']}</a><a class="lang" href="{t['other_href']}" lang="{'en' if t['lang'] == 'fr' else 'fr'}">{t['other_label']}</a></nav>
  </div>
</header>

<main id="main">
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1 class="reveal">{t['h1']}</h1>
      <p class="lede reveal d2">{t['lede']}</p>
      <div class="cta-row reveal d3">
        <a class="btn btn-gold" href="https://tally.so/r/rDD17N" data-tally-open="rDD17N" data-tally-layout="modal" data-tally-width="640" data-tally-emoji-animation="none">{t['cta1']}</a>
        <a class="btn btn-ghost" href="#parcours">{t['cta2']}</a>
      </div>
    </div>
    <aside class="hero-figs reveal d4" aria-label="{t['figs_label']}"><dl>{figs}</dl></aside>
  </div>
</section>

<section class="proof" aria-label="J2A">
  <div class="wrap proof-grid">{proof}</div>
</section>

<section class="corridors">
  <div class="wrap corridors-grid">
    <div>
      <h2>{t['corr_title']}</h2>
      <p class="corr-intro">{t['corr_intro']}</p>
      <div class="corridor-card" aria-live="polite"></div>
      <div class="corridor-hint">{t['map_hint']}</div>
      <figure class="port-photo"><img src="{b}assets/port-lome.jpg" alt="{t['port_alt']}" width="1400" height="788" loading="lazy"><figcaption>{t['port_cap']} <span class="credit">{t['port_credit']} <a href="https://commons.wikimedia.org/wiki/File:Container_ships_at_Lome_port.jpg" target="_blank" rel="noopener">Brendertogo</a>, <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener">CC BY-SA 4.0</a></span></figcaption></figure>
    </div>
    <div class="corridor">{corridor_svg(t)}</div>
  </div>
</section>

<section class="manifesto">
  <div class="wrap">
    <p class="big">{t['big']}</p>
    <div class="cols">{cols}</div>
  </div>
</section>

<figure class="photo-band"><img src="{b}assets/terrain.jpg" alt="{t['band_alt']}" width="1080" height="810" loading="lazy"><figcaption class="wrap">{t['band_cap']}</figcaption></figure>

<section class="journey" id="parcours">
  <div class="wrap journey-grid">
    <div class="journey-head">
      <h2>{t['j_title']}</h2>
      <p>{t['j_intro']}</p>
    </div>
    <div class="vwrap">
      <span class="rail" aria-hidden="true"><i></i></span>
      <ol class="vsteps">{vsteps}</ol>
    </div>
  </div>
</section>

<section class="expertise" id="expertises">
  <div class="wrap">
    <h2>{t['exp_title']}</h2>
    <div class="exp-grid">{expg}</div>
  </div>
</section>

<section class="agro" id="filieres">
  <div class="wrap">
    <div class="agro-top">
      <div class="agro-head">
        <p class="kicker">{t['agro_kicker']}</p>
        <h2>{t['agro_title']}</h2>
        <p class="agro-lede">{t['agro_lede']}</p>
      </div>
      <figure class="agro-photo"><img src="{b}assets/producteurs.jpg" alt="{t['agro_photo_alt']}" width="1080" height="810" loading="lazy"><figcaption>{t['agro_photo_cap']}</figcaption></figure>
    </div>
    <ol class="agro-grid">{agro}</ol>
    <h3 class="agro-who-title">{t['agro_who_title']}</h3>
    <div class="agro-who">{agro_who}</div>
    <div class="agro-rule">
      <p>{t['agro_rule']}</p>
      <a class="btn btn-gold" href="mailto:ykstrategic@proton.me?subject={t['agro_subject']}">{t['agro_cta']}</a>
    </div>
  </div>
</section>

<section class="case">
  <div class="wrap case-grid">
    <div>
      <h2>{t['case_title']}</h2>
      <p class="case-name">{t['case_name']}</p>
      <p>{t['case_lede']}</p>
    </div>
    <div>
      <ul class="case-steps">{csteps}</ul>
      <p class="case-more">{t['case_more']}</p>
      <a class="btn btn-ink" href="mailto:ykstrategic@proton.me?subject={t['case_subject']}">{t['case_cta']}</a>
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
  <div class="wrap leader-grid">
    <div class="leader-photo"><img src="{b}assets/yaovi.jpg" alt="{t['photo_alt']}" width="900" height="1125" loading="lazy"></div>
    <div class="leader-text">
      <h2 class="sr">{t['lead_title']}</h2>
      <div class="name">{t['lead_name']}</div>
      <div class="role">{t['lead_role']}</div>
      {lead}
      <blockquote>{t['lead_quote']}</blockquote>
    </div>
  </div>
</section>

<section class="eco" id="partenaires">
  <div class="wrap">
    <h2>{t['eco_title']}</h2>
    <p class="eco-intro">{t['eco_intro']}</p>
    <div class="eco-cols">{eco3}</div>
    <h3 class="partners-title">{t['partners_title']}</h3>
    <div class="partners">{partners}</div>
  </div>
</section>

<section class="consult" id="premier-echange">
  <div class="wrap consult-grid">
    <div>
      <p class="kicker">{t['consult_kicker']}</p>
      <h2>{t['consult_title']}</h2>
      <p class="consult-lede">{t['consult_lede']}</p>
      <a class="btn btn-gold" href="https://tally.so/r/rDD17N" data-tally-open="rDD17N" data-tally-layout="modal" data-tally-width="640" data-tally-emoji-animation="none">{t['consult_cta']}</a>
    </div>
    <div class="consult-box">
      <h3>{t['consult_get_title']}</h3>
      <ul>{consult_get}</ul>
      <p class="consult-note">{t['consult_note']}</p>
    </div>
  </div>
</section>
</main>

<footer class="contact" id="contact">
  <div class="wrap">
    <div class="say">{t['say']}</div>
    <p style="color:#b9c6cb;margin-top:22px">{t['c_intro']}</p>
    <div class="cta-row"><a class="btn btn-gold" href="https://tally.so/r/rDD17N" data-tally-open="rDD17N" data-tally-layout="modal" data-tally-width="640" data-tally-emoji-animation="none">{t['form_cta']}</a></div>
    <p class="or">{t['or_mail']}</p>
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
<script src="{b}assets/app.js?v={VER}" defer></script>
<script src="https://tally.so/widgets/embed.js" async></script>
</body>
</html>
"""

(ROOT / "index.html").write_text(page(T["fr"]), encoding="utf-8")
(ROOT / "en" / "index.html").write_text(page(T["en"]), encoding="utf-8")
print("ok")
