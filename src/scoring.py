"""
BUAS® Growth Intelligence — Scoring Engine v2.1

Scoring (total 100):
  A. Encaje creativo con BUAS — 25 pts
  B. Necesidad de branding o digital — 20 pts
  C. Capacidad económica — 20 pts
  D. Momento de oportunidad — 15 pts
  E. Potencial de portfolio y reputación — 10 pts
  F. Accesibilidad comercial — 10 pts
"""
from datetime import datetime


def _text(*fields) -> str:
    return " ".join(filter(None, fields)).lower()


def _count_hits(text: str, flags: list[str]) -> int:
    return sum(1 for w in flags if w in text)


def score_encaje_creativo(p) -> int:
    """0-25: Does BUAS want this brand in its portfolio?"""
    score = 0

    # Positioning quality (0-10)
    pos = (p.posicionamiento or "").lower()
    desc = (p.descripcion_negocio or "").lower()
    combined_pos = pos + " " + desc
    if any(w in combined_pos for w in [
        "lujo", "gran lujo", "5 estrellas", "high-end", "luxury"
    ]):
        score += 10
    elif any(w in combined_pos for w in [
        "premium", "boutique", "autor", "gourmet", "artesanal",
        "exclusivo", "selecto", "haute", "craft"
    ]):
        score += 9
    elif any(w in combined_pos for w in [
        "medio-alto", "aspiracional", "innovador", "disruptivo",
        "emergente premium", "streetwear", "digital-first", "hype"
    ]):
        score += 7
    elif any(w in combined_pos for w in [
        "crecimiento", "emergente", "consolidado", "establecido",
        "medio", "sostenible", "eco", "zero waste"
    ]):
        score += 5
    elif pos:
        score += 3

    # Sector fit (0-8)
    sector = (p.sector or "").lower()
    subsector = (p.subsector or "").lower()
    sector_all = sector + " " + subsector
    if any(s in sector_all for s in [
        "hospitality", "hostelería", "hotel", "restauración", "experience",
        "restaurante", "beach club", "resort"
    ]):
        score += 8
    elif any(s in sector_all for s in [
        "food", "alimentación", "bebida", "f&b", "gourmet", "beverage",
        "vino", "bodega", "conserva", "chocolate", "aceite", "gastro"
    ]):
        score += 7
    elif any(s in sector_all for s in [
        "lifestyle", "beauty", "consumer", "cosmética", "belleza", "moda",
        "fashion", "skincare", "wellness", "perfum", "joyería"
    ]):
        score += 7
    elif any(s in sector_all for s in [
        "architecture", "arquitectura", "real estate", "inmobili", "space",
        "interiorismo", "promotora", "residencial"
    ]):
        score += 6
    elif any(s in sector_all for s in [
        "tech", "tecnología", "b2b", "saas", "fintech", "healthtech",
        "startup", "software", "app"
    ]):
        score += 5
    else:
        score += 3

    # Brand gap = opportunity (0-7)
    cal = (p.calidad_identidad or "").lower()
    problemas = (p.problemas_marca or "").lower()
    web_design = (p.web_diseno or "").lower()
    combined = cal + " " + problemas + " " + web_design
    if any(w in combined for w in [
        "pobre", "amateur", "inexistente", "muy básica", "obsoleta",
        "sin identidad", "sin marca", "sin web", "no tiene", "no profesional"
    ]):
        score += 7
    elif any(w in combined for w in [
        "mejorable", "básica", "desactualizada", "inconsistente", "genérica",
        "heterogénea", "poco diferencia", "sin diferenciación", "irregular",
        "incoherente", "no comunica", "necesita", "transición"
    ]):
        score += 6
    elif any(w in combined for w in [
        "correcta pero", "margen de mejora", "funcional pero", "estándar",
        "correcta", "media", "podría modernizarse", "podría mejorar"
    ]):
        score += 4
    elif combined.strip():
        score += 2

    return min(score, 25)


def score_necesidad(p) -> int:
    """0-20: Identifiable and demonstrable need for branding/digital."""
    score = 0

    brand_text = _text(
        p.problemas_marca, p.necesidad_branding, p.necesidad_packaging,
        p.necesidad_estrategica, p.calidad_identidad, p.coherencia_marca,
        p.diferenciacion, p.encaje_creativo, p.problema_branding
    )

    digital_text = _text(
        p.web_mejoras, p.web_diseno, p.necesidad_digital, p.web_ux,
        p.web_arquitectura, p.web_movil, p.web_copywriting, p.web_conversion,
        p.problema_digital
    )

    brand_flags = [
        "obsoleta", "incoherente", "amateur", "sin identidad", "desactualizada",
        "genérica", "sin diferenciación", "pobre", "inconsistente", "sin marca",
        "no profesional", "básica", "mejorable", "heterogénea", "poco diferencia",
        "necesita nueva imagen", "transición", "no comunica", "modernizar",
        "desalineada", "sin coherencia", "falta coherencia", "sin personalidad",
        "indefinida", "desfasada", "anticuada", "necesita rebranding",
        "marca industrial", "imagen que no", "marca que no"
    ]

    digital_flags = [
        "obsoleta", "lenta", "no responsive", "sin ecommerce", "mejorable",
        "pobre", "básica", "sin web", "wordpress genérico", "template",
        "no optimizada", "sin estrategia", "deficiente", "funcional pero",
        "rediseño", "necesita web", "web necesita", "sin storytelling",
        "experiencia de marca", "mejora", "actualización", "profesionalización",
        "sin diferenciación", "estándar", "web completa", "web y comunicación"
    ]

    brand_hits = _count_hits(brand_text, brand_flags)
    digital_hits = _count_hits(digital_text, digital_flags)

    opp_text = _text(
        p.descripcion_oportunidad, p.servicio_potencial,
        p.potencial_transformacion, p.argumento_comercial
    )
    extra_brand = _count_hits(opp_text, [
        "branding", "identidad", "packaging", "marca", "reposicionamiento",
        "arquitectura de marca", "naming", "unificación", "coherencia"
    ])
    extra_digital = _count_hits(opp_text, [
        "web", "digital", "ecommerce", "comunicación", "online",
        "rediseño", "dirección de arte"
    ])

    brand_score = min((brand_hits + extra_brand) * 2, 10)
    digital_score = min((digital_hits + extra_digital) * 2, 10)

    score = brand_score + digital_score
    return min(score, 20)


def score_capacidad_economica(p) -> int:
    """0-20: Evidence of capacity for 5K-15K+ projects."""
    score = 0
    tamano = (p.tamano_estimado or "").lower()
    cap = (p.capacidad_economica or "").lower()
    ticket = (p.ticket_potencial or "").lower()
    combined = tamano + " " + cap

    if any(w in combined for w in [
        "grande", "multinacional", "cotizada", "grupo grande",
        ">70", ">50", "más de 50", "más de 70"
    ]):
        score += 12
    elif any(w in combined for w in [
        "mediana-grande", "cadena", "grupo", "más de 20", "más de 15",
        ">20", ">15", "15+", "20+", "16+", "red de"
    ]):
        score += 10
    elif any(w in combined for w in [
        "mediana", "consolidada", "varias ubicaciones", "establecida",
        "familiar consolidada", "bodega familiar consolidada"
    ]):
        score += 8
    elif any(w in combined for w in [
        "pequeña-mediana", "pyme en crecimiento", "financiada",
        "serie a", "serie b", "en crecimiento", "pyme"
    ]):
        score += 6
    elif any(w in combined for w in [
        "pequeña", "startup", "seed", "pre-seed", "joven"
    ]):
        score += 4
    elif any(w in combined for w in ["micro", "autónomo", "unipersonal"]):
        score += 2
    elif combined.strip():
        score += 3

    # Ticket potential boost (0-5)
    if any(w in ticket for w in ["25.000", "25k", ">25", "30.000"]):
        score += 5
    elif any(w in ticket for w in ["15.000", "15k", ">15", "20.000"]):
        score += 4
    elif any(w in ticket for w in ["10.000", "10k", ">10"]):
        score += 3
    elif any(w in ticket for w in ["5.000", "5k", ">5", "7.000"]):
        score += 2

    # Funding signals boost
    senal = (p.senal_detectada or "").lower()
    if any(w in senal for w in [
        "inversión", "financiación", "ronda", "funding", "capital",
        "adquisición", "compra", "fusión"
    ]):
        score += 4

    # Multiple locations = capacity
    ubicaciones = p.num_ubicaciones or ""
    if ubicaciones:
        try:
            text = str(ubicaciones).lower()
            if "varias" in text or "múltiples" in text:
                score += 2
            else:
                n = int("".join(c for c in text if c.isdigit()) or "0")
                if n >= 10:
                    score += 3
                elif n >= 3:
                    score += 2
                elif n >= 2:
                    score += 1
        except ValueError:
            pass

    return min(score, 20)


def score_momento(p) -> int:
    """0-15: Is the timing right?"""
    score = 0
    senal = (p.senal_detectada or "").lower()
    signal = (p.signal_type or "").lower()
    opp = (p.descripcion_oportunidad or "").lower()
    combined = senal + " " + signal + " " + opp

    high_moment = [
        "nueva apertura", "lanzamiento", "expansión", "nuevo producto",
        "nueva marca", "rebranding", "nuevo concepto", "inauguración",
        "aperturas", "abre", "abrirá", "apertura", "crecimiento explosivo",
        "flagship", "nueva gama", "nueva línea", "nuevas aperturas",
        "new_business", "expansion", "new_product"
    ]
    medium_moment = [
        "inversión", "financiación", "nueva sede", "nueva categoría",
        "crecimiento", "contratación", "adquisición", "fusión",
        "expansión fuera", "exportación", "internacionalización",
        "funding", "transformation", "new_market",
        "cambio generacional", "nueva dirección", "tendencia"
    ]
    low_moment = [
        "web obsoleta", "identidad incoherente", "digital gap",
        "premiumización", "rebranding_potential", "digital_gap",
        "premiumization", "brand_architecture", "modernizar",
        "podría mejorar", "necesitan actualización"
    ]

    if any(s in combined for s in high_moment):
        score += 12
    elif any(s in combined for s in medium_moment):
        score += 8
    elif any(s in combined for s in low_moment):
        score += 5
    elif combined.strip():
        score += 3

    # Recency bonus
    if p.fecha_senal:
        try:
            senal_date = datetime.strptime(p.fecha_senal, "%Y-%m-%d")
            days_ago = (datetime.now() - senal_date).days
            if days_ago < 90:
                score += 3
            elif days_ago < 180:
                score += 2
            elif days_ago < 365:
                score += 1
        except (ValueError, TypeError):
            pass

    return min(score, 15)


def score_portfolio(p) -> int:
    """0-10: Would this project elevate BUAS's reputation?"""
    score = 0
    pos = (p.posicionamiento or "").lower()
    sector = (p.sector or "").lower()
    desc = (p.descripcion_negocio or "").lower()
    combined_pos = pos + " " + desc

    if any(w in combined_pos for w in [
        "lujo", "gran lujo", "5 estrellas", "luxury"
    ]):
        score += 4
    elif any(w in combined_pos for w in [
        "premium", "boutique", "autor", "gourmet", "high-end",
        "artesanal", "exclusivo", "craft"
    ]):
        score += 4
    elif any(w in combined_pos for w in [
        "medio-alto", "aspiracional", "innovador", "streetwear",
        "digital-first", "disruptivo"
    ]):
        score += 3
    elif any(w in combined_pos for w in [
        "emergente", "sostenible", "zero waste", "eco"
    ]):
        score += 2

    high_vis = [
        "hospitality", "hotel", "cosmética", "beauty", "moda", "food",
        "lifestyle", "consumer", "fashion", "restaurante", "beach",
        "vino", "gourmet", "chocolate", "wellness"
    ]
    if any(s in sector for s in high_vis):
        score += 3
    elif sector.strip():
        score += 1

    presencia = (p.presencia or "").lower()
    if any(w in presencia for w in ["internacional", "global", "exporta"]):
        score += 3
    elif any(w in presencia for w in [
        "nacional", "varias ciudades", "varias provincias",
        "expansión fuera", "buscando expansión"
    ]):
        score += 2
    elif any(w in presencia for w in ["regional", "local fuerte", "local"]):
        score += 1

    return min(score, 10)


def score_accesibilidad(p) -> int:
    """0-10: Can BUAS reach the decision-maker?"""
    score = 0
    if p.nombre_decisor:
        score += 3
    if p.contacto_corporativo:
        score += 2
    if p.via_contacto:
        score += 2
    if p.linkedin:
        score += 1
    if p.instagram:
        score += 1
    contacto = (p.contacto_corporativo or "").lower()
    if "@" in contacto or ".com" in contacto or ".es" in contacto:
        score += 1
    return min(score, 10)


def score_prospect(p) -> int:
    """Calculate and assign all dimension scores."""
    p.score_encaje_creativo = score_encaje_creativo(p)
    p.score_necesidad = score_necesidad(p)
    p.score_capacidad_economica = score_capacidad_economica(p)
    p.score_momento = score_momento(p)
    p.score_portfolio = score_portfolio(p)
    p.score_accesibilidad = score_accesibilidad(p)
    return p.calculate_score()
