"""
BUAS® Growth Intelligence — Scoring Engine v2

Scoring (total 100):
  A. Encaje creativo con BUAS — 25 pts
  B. Necesidad de branding o digital — 20 pts
  C. Capacidad económica — 20 pts
  D. Momento de oportunidad — 15 pts
  E. Potencial de portfolio y reputación — 10 pts
  F. Accesibilidad comercial — 10 pts
"""


def score_encaje_creativo(p) -> int:
    """0-25: Does BUAS want this brand in its portfolio?"""
    score = 0

    # Positioning quality
    pos = (p.posicionamiento or "").lower()
    if any(w in pos for w in ["premium", "lujo", "boutique", "autor", "gourmet", "high-end"]):
        score += 10
    elif any(w in pos for w in ["medio-alto", "aspiracional", "crecimiento", "emergente"]):
        score += 7
    elif any(w in pos for w in ["medio", "consolidado", "establecido"]):
        score += 4
    elif pos:
        score += 2

    # Sector fit
    sector = (p.sector or "").lower()
    if any(s in sector for s in ["hospitality", "hostelería", "hotel", "restauración", "experience"]):
        score += 8
    elif any(s in sector for s in ["food", "alimentación", "bebida", "f&b", "gourmet", "beverage"]):
        score += 7
    elif any(s in sector for s in ["lifestyle", "beauty", "consumer", "cosmética", "belleza", "moda"]):
        score += 6
    elif any(s in sector for s in ["architecture", "arquitectura", "real estate", "inmobili", "space"]):
        score += 6
    elif any(s in sector for s in ["tech", "tecnología", "b2b", "saas", "fintech"]):
        score += 5
    else:
        score += 2

    # Brand gap = opportunity
    cal = (p.calidad_identidad or "").lower()
    problemas = (p.problemas_marca or "").lower()
    combined = cal + " " + problemas
    if any(w in combined for w in ["pobre", "amateur", "inexistente", "muy básica", "obsoleta"]):
        score += 7
    elif any(w in combined for w in ["mejorable", "básica", "desactualizada", "inconsistente", "genérica"]):
        score += 5
    elif any(w in combined for w in ["correcta", "media", "irregular"]):
        score += 3
    elif combined.strip():
        score += 1

    return min(score, 25)


def score_necesidad(p) -> int:
    """0-20: Identifiable and demonstrable need for branding/digital."""
    score = 0
    brand_text = " ".join(filter(None, [p.problemas_marca, p.necesidad_branding,
                                        p.necesidad_packaging, p.necesidad_estrategica])).lower()
    digital_text = " ".join(filter(None, [p.web_mejoras, p.web_diseno, p.necesidad_digital,
                                          p.web_ux])).lower()

    brand_flags = ["obsoleta", "incoherente", "amateur", "sin identidad", "desactualizada",
                   "genérica", "sin diferenciación", "pobre", "inconsistente", "sin marca",
                   "no profesional", "básica"]
    digital_flags = ["obsoleta", "lenta", "no responsive", "sin ecommerce", "mejorable",
                     "pobre", "básica", "sin web", "wordpress genérico", "template",
                     "no optimizada", "sin estrategia", "deficiente"]

    brand_hits = sum(1 for w in brand_flags if w in brand_text)
    digital_hits = sum(1 for w in digital_flags if w in digital_text)

    score += min(brand_hits * 3, 10)
    score += min(digital_hits * 3, 10)

    return min(score, 20)


def score_capacidad_economica(p) -> int:
    """0-20: Evidence of capacity for 5K-15K+ projects."""
    score = 0
    tamano = (p.tamano_estimado or "").lower()
    cap = (p.capacidad_economica or "").lower()
    combined = tamano + " " + cap

    if any(w in combined for w in ["grande", "multinacional", "cadena", "grupo grande", "cotizada"]):
        score += 12
    elif any(w in combined for w in ["mediana", "consolidada", "grupo", "varias ubicaciones"]):
        score += 9
    elif any(w in combined for w in ["pyme", "en crecimiento", "financiada", "serie a", "serie b"]):
        score += 7
    elif any(w in combined for w in ["pequeña", "startup", "seed", "pre-seed"]):
        score += 4
    elif any(w in combined for w in ["micro", "autónomo", "unipersonal"]):
        score += 2

    # Funding signals boost
    senal = (p.senal_detectada or "").lower()
    if any(w in senal for w in ["inversión", "financiación", "ronda", "funding", "capital"]):
        score += 5

    # Multiple locations = capacity
    ubicaciones = p.num_ubicaciones or ""
    if ubicaciones:
        try:
            n = int("".join(c for c in str(ubicaciones) if c.isdigit()) or "0")
            if n >= 5:
                score += 3
            elif n >= 2:
                score += 2
        except ValueError:
            pass

    return min(score, 20)


def score_momento(p) -> int:
    """0-15: Is the timing right?"""
    score = 0
    senal = (p.senal_detectada or "").lower()
    signal = (p.signal_type or "").upper()

    high_moment = ["nueva apertura", "lanzamiento", "expansión", "nuevo producto",
                   "nueva marca", "rebranding", "nuevo concepto", "inauguración",
                   "NEW_BUSINESS", "EXPANSION", "NEW_PRODUCT"]
    medium_moment = ["inversión", "financiación", "nueva línea", "nueva sede",
                     "crecimiento", "contratación", "adquisición", "fusión",
                     "FUNDING", "TRANSFORMATION", "NEW_MARKET"]
    low_moment = ["web obsoleta", "identidad incoherente", "digital gap",
                  "premiumización", "REBRANDING_POTENTIAL", "DIGITAL_GAP",
                  "PREMIUMIZATION", "BRAND_ARCHITECTURE"]

    combined = senal + " " + signal
    if any(s.lower() in combined.lower() for s in high_moment):
        score += 12
    elif any(s.lower() in combined.lower() for s in medium_moment):
        score += 8
    elif any(s.lower() in combined.lower() for s in low_moment):
        score += 5

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

    if any(w in pos for w in ["premium", "lujo", "boutique", "autor", "gourmet", "high-end"]):
        score += 4
    elif any(w in pos for w in ["medio-alto", "aspiracional", "innovador"]):
        score += 3
    elif any(w in pos for w in ["emergente", "disruptivo"]):
        score += 2

    high_vis = ["hospitality", "hotel", "cosmética", "beauty", "moda", "food", "lifestyle", "consumer"]
    if any(s in sector for s in high_vis):
        score += 3

    presencia = (p.presencia or "").lower()
    if any(w in presencia for w in ["internacional", "global", "exporta"]):
        score += 3
    elif any(w in presencia for w in ["nacional", "varias ciudades"]):
        score += 2
    elif any(w in presencia for w in ["regional", "local fuerte"]):
        score += 1

    return min(score, 10)


def score_accesibilidad(p) -> int:
    """0-10: Can BUAS reach the decision-maker?"""
    score = 0
    if p.nombre_decisor:
        score += 3
    if p.contacto_corporativo:
        score += 3
    if p.via_contacto:
        score += 2
    if p.linkedin:
        score += 1
    if p.instagram:
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


from datetime import datetime
