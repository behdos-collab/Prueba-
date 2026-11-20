"""
BUAS Prospecting Intelligence System - Scoring Engine

Scoring dimensions (total 100):
  A. Encaje creativo con BUAS — 25 pts
  B. Necesidad de branding o web — 20 pts
  C. Capacidad economica — 20 pts
  D. Momento de oportunidad — 15 pts
  E. Potencial de portfolio — 10 pts
  F. Accesibilidad del decisor — 10 pts
"""


def score_encaje_creativo(prospect) -> int:
    """Score 0-25: creative fit with BUAS."""
    score = 0
    pos = prospect.posicionamiento.lower() if prospect.posicionamiento else ""
    if any(w in pos for w in ["premium", "alto", "lujo", "boutique", "gourmet", "autor"]):
        score += 10
    elif any(w in pos for w in ["medio-alto", "aspiracional", "crecimiento"]):
        score += 7
    elif any(w in pos for w in ["medio", "consolidado"]):
        score += 4

    sector = prospect.sector.lower() if prospect.sector else ""
    priority_1 = ["hospitality", "hostelería", "hotel", "restauración"]
    priority_2 = ["alimentación", "bebidas", "f&b", "gourmet"]
    priority_3 = ["cosmética", "belleza", "wellness"]
    if any(s in sector for s in priority_1):
        score += 8
    elif any(s in sector for s in priority_2):
        score += 7
    elif any(s in sector for s in priority_3):
        score += 6
    elif any(s in sector for s in ["arquitectura", "interiorismo", "real estate"]):
        score += 5
    elif any(s in sector for s in ["moda", "lifestyle", "retail"]):
        score += 5
    elif any(s in sector for s in ["tecnología", "b2b", "saas"]):
        score += 4
    else:
        score += 2

    cal = prospect.calidad_identidad.lower() if prospect.calidad_identidad else ""
    if any(w in cal for w in ["pobre", "baja", "amateur", "desactualizada", "inconsistente"]):
        score += 7
    elif any(w in cal for w in ["mejorable", "básica", "irregular"]):
        score += 5
    elif any(w in cal for w in ["correcta", "media"]):
        score += 3
    elif cal:
        score += 1

    return min(score, 25)


def score_necesidad(prospect) -> int:
    """Score 0-20: need for branding/web services."""
    score = 0
    problemas = (prospect.problemas_marca or "").lower()
    web = (prospect.web_mejoras or "").lower()
    diseno = (prospect.web_diseno or "").lower()

    brand_issues = ["obsoleta", "incoherente", "amateur", "sin identidad", "desactualizada",
                    "genérica", "sin diferenciación", "pobre"]
    web_issues = ["obsoleta", "lenta", "no responsive", "sin ecommerce", "mejorable",
                  "pobre", "básica", "sin web", "wordpress genérico"]

    brand_count = sum(1 for w in brand_issues if w in problemas)
    web_count = sum(1 for w in web_issues if w in web or w in diseno)

    score += min(brand_count * 3, 10)
    score += min(web_count * 3, 10)

    return min(score, 20)


def score_capacidad_economica(prospect) -> int:
    """Score 0-20: economic capacity."""
    score = 0
    tamano = (prospect.tamano_estimado or "").lower()
    rango = (prospect.presupuesto_rango or "").lower()

    if any(w in tamano for w in ["grande", "multinacional", "cadena"]):
        score += 10
    elif any(w in tamano for w in ["mediana", "consolidada", "grupo"]):
        score += 8
    elif any(w in tamano for w in ["pequeña-mediana", "pyme consolidada", "en crecimiento"]):
        score += 6
    elif any(w in tamano for w in ["pequeña", "startup financiada"]):
        score += 4
    elif any(w in tamano for w in ["micro", "autónomo"]):
        score += 2

    if "15.000" in rango or "complejo" in rango or "20.000" in rango:
        score += 10
    elif "10.000" in rango or "8.000" in rango:
        score += 8
    elif "5.000" in rango or "branding + web" in rango:
        score += 6
    elif "3.000" in rango or "branding" in rango:
        score += 4

    return min(score, 20)


def score_momento(prospect) -> int:
    """Score 0-15: timing/opportunity moment."""
    score = 0
    senal = (prospect.senal_detectada or "").lower()

    high_signals = ["nueva apertura", "lanzamiento", "expansión", "nuevo producto",
                    "nueva marca", "rebranding"]
    medium_signals = ["inversión", "financiación", "nueva línea", "nueva sede",
                      "crecimiento", "contratación"]
    low_signals = ["web obsoleta", "identidad incoherente", "actividad digital"]

    if any(s in senal for s in high_signals):
        score += 12
    elif any(s in senal for s in medium_signals):
        score += 8
    elif any(s in senal for s in low_signals):
        score += 5

    if prospect.fecha_senal:
        try:
            from datetime import datetime
            senal_date = datetime.strptime(prospect.fecha_senal, "%Y-%m-%d")
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


def score_portfolio(prospect) -> int:
    """Score 0-10: portfolio and visibility potential."""
    score = 0
    pos = (prospect.posicionamiento or "").lower()
    sector = (prospect.sector or "").lower()

    if any(w in pos for w in ["premium", "lujo", "boutique", "autor", "gourmet"]):
        score += 5
    elif any(w in pos for w in ["medio-alto", "aspiracional"]):
        score += 3

    high_vis_sectors = ["hospitality", "hostelería", "cosmética", "moda", "alimentación"]
    if any(s in sector for s in high_vis_sectors):
        score += 3

    if prospect.presencia and any(w in prospect.presencia.lower() for w in ["nacional", "internacional"]):
        score += 2

    return min(score, 10)


def score_accesibilidad(prospect) -> int:
    """Score 0-10: decision-maker accessibility."""
    score = 0

    if prospect.nombre_decisor:
        score += 3
    if prospect.contacto_corporativo:
        score += 3
    if prospect.via_contacto:
        score += 2
    if prospect.linkedin:
        score += 2

    return min(score, 10)


def score_prospect(prospect) -> int:
    """Calculate and assign all scores for a prospect."""
    prospect.score_encaje_creativo = score_encaje_creativo(prospect)
    prospect.score_necesidad = score_necesidad(prospect)
    prospect.score_capacidad_economica = score_capacidad_economica(prospect)
    prospect.score_momento = score_momento(prospect)
    prospect.score_portfolio = score_portfolio(prospect)
    prospect.score_accesibilidad = score_accesibilidad(prospect)
    return prospect.calculate_score()
