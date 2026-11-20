"""
BUAS® Growth Intelligence — Report Generation v2

Generates all 7 deliverables:
  01. Master Database (CSV)
  02. Top 100
  03. Top 30
  04. Top 15
  05. Top 10 (deep analysis dossiers)
  06. Market Intelligence Report
  07. Action Plan (4 weeks)
"""
import os
from datetime import datetime


SIGNAL_TYPES = {
    "NEW_BUSINESS": "Creación de nuevas empresas, nuevos conceptos o negocios",
    "EXPANSION": "Apertura de establecimientos, nuevas sedes, internacionalización",
    "NEW_PRODUCT": "Lanzamiento de productos, líneas, servicios o categorías",
    "FUNDING": "Inversión, financiación, adquisición de capital o entrada de socios",
    "REBRANDING_POTENTIAL": "Marca desactualizada, inconsistente o desalineada con el negocio",
    "DIGITAL_GAP": "Web deficiente, ecommerce inexistente, problemas de comunicación digital",
    "TRANSFORMATION": "Cambio generacional, nueva dirección, fusión, reposicionamiento",
    "NEW_MARKET": "Entrada en nuevos mercados, exportación, expansión comercial",
    "PREMIUMIZATION": "Negocio que sube de nivel pero cuya marca no lo refleja",
    "BRAND_ARCHITECTURE": "Necesidad de estructurar arquitectura de marca por crecimiento",
}

PROJECT_TIERS = {
    "BRAND_FOUNDATION": {"label": "Brand Foundation", "range": "4.000–7.000 €",
                         "desc": "Estrategia, posicionamiento, identidad y sistema de marca"},
    "BRAND_DIGITAL": {"label": "Brand & Digital", "range": "7.000–15.000 €",
                      "desc": "Branding, web, experiencia digital y desarrollo"},
    "BRAND_TRANSFORMATION": {"label": "Brand Transformation", "range": "12.000–25.000 €+",
                             "desc": "Reposicionamiento, arquitectura de marca, identidad, digital"},
    "CREATIVE_PARTNER": {"label": "Creative Partner", "range": "1.000–3.000 €/mes",
                         "desc": "Dirección creativa, evolución de marca, campañas, soporte"},
}


def _header(f, title, subtitle=""):
    f.write(f"# BUAS® — {title}\n\n")
    if subtitle:
        f.write(f"*{subtitle}*\n\n")
    f.write(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y')}\n\n")
    f.write("---\n\n")


def generate_top100_report(prospects, filepath="output/02_top_100.md"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        _header(f, "TOP 100 EMPRESAS POTENCIALES",
                "Empresas con mayor encaje con BUAS ordenadas por score")
        f.write("| # | Empresa | Sector | Ciudad | Score | Prioridad |\n")
        f.write("|---|---------|--------|--------|-------|----------|\n")
        for i, p in enumerate(prospects[:100], 1):
            name = p.nombre_comercial or p.nombre_empresa
            f.write(f"| {i} | {name} | {p.sector} | {p.ciudad} | {p.score_total} | {p.prioridad} |\n")
    return filepath


def generate_top30_report(prospects, filepath="output/03_top_30.md"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        _header(f, "TOP 30 — ANÁLISIS DE OPORTUNIDADES",
                "30 empresas investigadas con señales de oportunidad")
        for i, p in enumerate(prospects[:30], 1):
            name = p.nombre_comercial or p.nombre_empresa
            f.write(f"## {i}. {name}\n\n")
            f.write(f"**Sector**: {p.sector} — {p.subsector}  \n")
            f.write(f"**Ciudad**: {p.ciudad}  \n")
            f.write(f"**Score**: {p.score_total}/100 — Prioridad **{p.prioridad}**  \n")
            f.write(f"**Web**: {p.url}  \n\n")
            f.write(f"**Negocio**: {p.descripcion_negocio or getattr(p, 'productos_servicios', '')}  \n")
            f.write(f"**Posicionamiento**: {p.posicionamiento}  \n")
            f.write(f"**Tamaño**: {p.tamano_estimado}  \n\n")
            f.write(f"**Señal detectada**: {p.senal_detectada}  \n")
            sig_label = SIGNAL_TYPES.get(getattr(p, 'signal_type', ''), getattr(p, 'signal_type', ''))
            if sig_label:
                f.write(f"**Tipo de señal**: {sig_label}  \n")
            f.write(f"**Problemas de marca**: {p.problemas_marca}  \n")
            f.write(f"**Mejoras digitales**: {p.web_mejoras}  \n\n")
            f.write(f"**Servicio potencial BUAS**: {p.servicio_potencial}  \n")
            ticket = getattr(p, 'ticket_potencial', '') or getattr(p, 'presupuesto_rango', '')
            f.write(f"**Ticket potencial**: {ticket}  \n")
            oportunidad = getattr(p, 'descripcion_oportunidad', '') or getattr(p, 'motivo_oportunidad', '')
            f.write(f"**Oportunidad**: {oportunidad}  \n\n")

            f.write("**Desglose scoring**:\n\n")
            f.write(f"| Dimensión | Pts | Max |\n|---|---|---|\n")
            f.write(f"| Encaje creativo | {p.score_encaje_creativo} | 25 |\n")
            f.write(f"| Necesidad branding/digital | {p.score_necesidad} | 20 |\n")
            f.write(f"| Capacidad económica | {p.score_capacidad_economica} | 20 |\n")
            f.write(f"| Momento oportunidad | {p.score_momento} | 15 |\n")
            f.write(f"| Potencial portfolio | {p.score_portfolio} | 10 |\n")
            f.write(f"| Accesibilidad comercial | {p.score_accesibilidad} | 10 |\n")
            f.write(f"| **TOTAL** | **{p.score_total}** | **100** |\n\n")
            f.write("---\n\n")
    return filepath


def generate_top15_report(prospects, filepath="output/04_top_15.md"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        _header(f, "TOP 15 — OPORTUNIDADES PRIORITARIAS",
                "Las 15 mejores oportunidades comerciales para BUAS")
        for i, p in enumerate(prospects[:15], 1):
            name = p.nombre_comercial or p.nombre_empresa
            f.write(f"## {i}. {name}\n\n")
            f.write(f"**{p.sector}** | {p.ciudad} | Score: **{p.score_total}/100** | Prioridad **{p.prioridad}**\n\n")
            f.write(f"**Qué hace**: {p.descripcion_negocio}  \n")
            f.write(f"**Posicionamiento**: {p.posicionamiento}  \n")
            f.write(f"**Web**: {p.url}  \n\n")
            f.write(f"**Señal**: {p.senal_detectada}  \n")
            oportunidad = getattr(p, 'descripcion_oportunidad', '') or p.problemas_marca
            f.write(f"**Por qué BUAS**: {oportunidad}  \n")
            f.write(f"**Servicio**: {p.servicio_potencial}  \n")
            ticket = getattr(p, 'ticket_potencial', '') or ''
            f.write(f"**Ticket**: {ticket}  \n\n")
            if p.argumento_comercial:
                f.write(f"**Argumento comercial**: {p.argumento_comercial}  \n\n")
            f.write("---\n\n")
    return filepath


def generate_top10_dossiers(prospects, dirpath="output/dossiers"):
    """RESULTADO 05: Top 10 deep-analysis dossiers."""
    os.makedirs(dirpath, exist_ok=True)
    for i, p in enumerate(prospects[:10], 1):
        name = p.nombre_comercial or p.nombre_empresa
        safe = name.replace(" ", "_").replace("/", "_")[:40]
        fp = os.path.join(dirpath, f"{i:02d}_{safe}.md")
        with open(fp, "w", encoding="utf-8") as f:
            f.write(f"# {name}\n\n")
            f.write(f"**Score**: {p.score_total}/100 — **Prioridad {p.prioridad}**\n\n")

            f.write("## Identificación\n\n")
            f.write(f"| Campo | Valor |\n|---|---|\n")
            f.write(f"| Empresa | {p.nombre_empresa} |\n")
            f.write(f"| Nombre comercial | {p.nombre_comercial} |\n")
            f.write(f"| Sector | {p.sector} — {p.subsector} |\n")
            f.write(f"| Ciudad | {p.ciudad} |\n")
            f.write(f"| Web | {p.url} |\n")
            f.write(f"| Instagram | {p.instagram} |\n")
            f.write(f"| LinkedIn | {p.linkedin} |\n\n")

            f.write("## Negocio\n\n")
            f.write(f"- **Descripción**: {p.descripcion_negocio}\n")
            f.write(f"- **Modelo**: {p.modelo_negocio}\n")
            f.write(f"- **Público**: {p.publico_objetivo}\n")
            f.write(f"- **Posicionamiento**: {p.posicionamiento}\n")
            f.write(f"- **Tamaño**: {p.tamano_estimado}\n")
            cap = getattr(p, 'capacidad_economica', '')
            f.write(f"- **Capacidad económica**: {cap}\n")
            f.write(f"- **Competidores**: {p.competidores}\n\n")

            f.write("## Análisis de marca\n\n")
            f.write(f"- **Calidad identidad**: {p.calidad_identidad}\n")
            f.write(f"- **Coherencia**: {p.coherencia_marca}\n")
            f.write(f"- **Diferenciación**: {p.diferenciacion}\n")
            f.write(f"- **Problemas**: {p.problemas_marca}\n\n")

            f.write("## Análisis digital\n\n")
            f.write(f"- **Diseño web**: {p.web_diseno}\n")
            f.write(f"- **UX/UI**: {p.web_ux}\n")
            f.write(f"- **Mejoras**: {p.web_mejoras}\n\n")

            f.write("## Oportunidad\n\n")
            f.write(f"- **Señal**: {p.senal_detectada}\n")
            f.write(f"- **Fecha señal**: {p.fecha_senal}\n")
            f.write(f"- **Fuente**: {p.fuente_senal}\n")
            oportunidad = getattr(p, 'descripcion_oportunidad', '')
            f.write(f"- **Descripción oportunidad**: {oportunidad}\n\n")

            f.write("## BUAS Fit\n\n")
            f.write(f"- **Servicio recomendado**: {p.servicio_potencial}\n")
            ticket = getattr(p, 'ticket_potencial', '')
            f.write(f"- **Ticket potencial**: {ticket}\n\n")

            f.write("## Scoring\n\n")
            f.write(f"| Dimensión | Pts | Max |\n|---|---|---|\n")
            f.write(f"| Encaje creativo | {p.score_encaje_creativo} | 25 |\n")
            f.write(f"| Necesidad branding/digital | {p.score_necesidad} | 20 |\n")
            f.write(f"| Capacidad económica | {p.score_capacidad_economica} | 20 |\n")
            f.write(f"| Momento oportunidad | {p.score_momento} | 15 |\n")
            f.write(f"| Potencial portfolio | {p.score_portfolio} | 10 |\n")
            f.write(f"| Accesibilidad comercial | {p.score_accesibilidad} | 10 |\n")
            f.write(f"| **TOTAL** | **{p.score_total}** | **100** |\n\n")

            if p.argumento_comercial:
                f.write("## Argumento comercial\n\n")
                f.write(f"{p.argumento_comercial}\n\n")

            if p.via_contacto or p.contacto_corporativo:
                f.write("## Contacto\n\n")
                f.write(f"- **Contacto corporativo**: {p.contacto_corporativo}\n")
                if p.nombre_decisor:
                    f.write(f"- **Decisor**: {p.nombre_decisor} ({p.cargo_decisor})\n")
                f.write(f"- **Vía de contacto**: {p.via_contacto}\n\n")

            f.write(f"---\n*Fuente: {p.fuente_origen} | Consulta: {getattr(p, 'fecha_consulta', p.fecha_deteccion)} | ")
            f.write(f"Verificado: {'Sí' if p.verificado else 'Pendiente'}*\n")
    return dirpath


def generate_market_report(db, filepath="output/06_informe_mercado.md"):
    """RESULTADO 06: Market Intelligence Report."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    stats = db.stats()
    scored = db.get_scored()

    sector_scores = {}
    for p in scored:
        s = p.sector or "Otros"
        sector_scores.setdefault(s, []).append(p.score_total)

    signal_counts = {}
    for p in scored:
        sig = getattr(p, 'signal_type', '') or ''
        if sig:
            signal_counts[sig] = signal_counts.get(sig, 0) + 1
        elif p.senal_detectada:
            key = p.senal_detectada[:50]
            signal_counts[key] = signal_counts.get(key, 0) + 1

    problems = {}
    for p in scored:
        for field in [p.problemas_marca, p.web_mejoras]:
            if field:
                for item in field.split(","):
                    item = item.strip()
                    if item:
                        problems[item] = problems.get(item, 0) + 1

    with open(filepath, "w", encoding="utf-8") as f:
        _header(f, "INFORME DE INTELIGENCIA DE MERCADO",
                "Growth Intelligence & Opportunity Detection System")

        f.write("## Resumen ejecutivo\n\n")
        f.write(f"- **Empresas descubiertas**: {stats['total']}\n")
        f.write(f"- **Empresas puntuadas**: {stats['scored']}\n")
        for pri in ["A", "B", "C", "DESCARTAR"]:
            count = stats["by_priority"].get(pri, 0)
            if count:
                f.write(f"- **Prioridad {pri}**: {count}\n")
        f.write("\n")

        f.write("## Sectores con mayor potencial\n\n")
        for sector in sorted(sector_scores.keys(),
                           key=lambda s: sum(sector_scores[s]) / max(len(sector_scores[s]), 1),
                           reverse=True):
            scores = sector_scores[sector]
            avg = sum(scores) / len(scores)
            top_score = max(scores)
            f.write(f"### {sector}\n\n")
            f.write(f"- Empresas: {len(scores)}\n")
            f.write(f"- Score medio: {avg:.0f}/100\n")
            f.write(f"- Score máximo: {top_score}/100\n\n")

        f.write("## Territorios con mejores oportunidades\n\n")
        regions = stats.get("by_region", {})
        for loc in sorted(regions.keys(), key=lambda k: regions[k], reverse=True)[:15]:
            f.write(f"- **{loc}**: {regions[loc]} empresas\n")
        f.write("\n")

        f.write("## Señales de oportunidad más frecuentes\n\n")
        for sig in sorted(signal_counts.keys(), key=lambda k: signal_counts[k], reverse=True)[:10]:
            label = SIGNAL_TYPES.get(sig, sig)
            f.write(f"- **{label}**: {signal_counts[sig]} empresas\n")
        f.write("\n")

        f.write("## Problemas de marca y digitales más recurrentes\n\n")
        for prob in sorted(problems.keys(), key=lambda k: problems[k], reverse=True)[:15]:
            f.write(f"- {prob}: {problems[prob]} empresas\n")
        f.write("\n")

        f.write("## Recomendaciones para BUAS\n\n")
        f.write("1. **Foco en Hospitality y F&B**: Mayor concentración de oportunidades premium con necesidad de branding integral.\n")
        f.write("2. **Territorio clave**: Expandir presencia comercial más allá de Murcia hacia Valencia, Madrid y Barcelona.\n")
        f.write("3. **Señales prioritarias**: Nuevas aperturas y lanzamientos son el mejor momento de entrada.\n")
        f.write("4. **Proyecto tipo**: Brand & Digital (7K-15K) es el rango con más oportunidades.\n")
        f.write("5. **Premiumización**: Muchas empresas están subiendo de nivel pero su marca no lo refleja — gran oportunidad de posicionamiento.\n\n")

    return filepath


def generate_action_plan(prospects, filepath="output/07_plan_accion.md"):
    """RESULTADO 07: 4-week commercial action plan for top 10."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        _header(f, "PLAN DE ACCIÓN COMERCIAL — 4 SEMANAS",
                "Estrategia de aproximación para las 10 mejores oportunidades")

        f.write("## Metodología\n\n")
        f.write("Para cada empresa se define: por qué interesa, qué necesita, qué ofrecer, ")
        f.write("cómo contactar y cuándo actuar.\n\n---\n\n")

        for i, p in enumerate(prospects[:10], 1):
            name = p.nombre_comercial or p.nombre_empresa
            week = min((i - 1) // 3 + 1, 4)

            f.write(f"## {i}. {name} — Semana {week}\n\n")
            f.write(f"**Sector**: {p.sector} | **Ciudad**: {p.ciudad} | **Score**: {p.score_total}/100\n\n")

            oportunidad = getattr(p, 'descripcion_oportunidad', '') or p.problemas_marca
            f.write(f"**Por qué nos interesa**: {oportunidad}\n\n")
            f.write(f"**Momento de oportunidad**: {p.senal_detectada}\n\n")
            f.write(f"**Qué podría necesitar**: {p.servicio_potencial}\n\n")

            ticket = getattr(p, 'ticket_potencial', '')
            f.write(f"**Ticket potencial**: {ticket}\n\n")
            f.write(f"**Canal de contacto**: {p.via_contacto or 'Web corporativa / LinkedIn'}\n\n")

            f.write("**Preparación previa**:\n")
            f.write("- Análisis visual de marca actual y puntos de mejora\n")
            f.write("- Estudio de competidores directos\n")
            f.write("- Preparar presentación personalizada con diagnóstico y propuesta de valor\n\n")

            proxima = getattr(p, 'proxima_accion', '') or 'Preparar aproximación personalizada y contactar por vía corporativa'
            f.write(f"**Siguiente acción**: {proxima}\n\n")
            f.write("---\n\n")

        f.write("## Calendario resumen\n\n")
        f.write("| Semana | Empresas | Acciones |\n")
        f.write("|--------|----------|----------|\n")
        names = [p.nombre_comercial or p.nombre_empresa for p in prospects[:10]]
        f.write(f"| 1 | {', '.join(names[:3])} | Investigación + contacto inicial |\n")
        f.write(f"| 2 | {', '.join(names[3:6])} | Investigación + contacto inicial |\n")
        f.write(f"| 3 | {', '.join(names[6:9])} | Investigación + contacto inicial |\n")
        rest = names[9:10] if len(names) > 9 else []
        f.write(f"| 4 | {', '.join(rest)} + seguimiento | Follow-up semanas 1-3 |\n\n")

    return filepath
