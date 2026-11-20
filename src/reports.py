"""
BUAS Prospecting Intelligence System - Report Generation
"""
import os
from datetime import datetime


def generate_market_report(db, filepath="output/05_informe_mercado.md"):
    """Generate ENTREGABLE 5: Market Report."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    stats = db.stats()
    scored = db.get_scored()

    sector_scores = {}
    sector_counts = {}
    for p in scored:
        s = p.sector or "Otros"
        sector_scores.setdefault(s, []).append(p.score_total)
        sector_counts[s] = sector_counts.get(s, 0) + 1

    region_counts = {}
    for p in scored:
        loc = p.ciudad or p.provincia or "Desconocida"
        region_counts[loc] = region_counts.get(loc, 0) + 1

    problems = {}
    for p in scored:
        if p.problemas_marca:
            for prob in p.problemas_marca.split(","):
                prob = prob.strip()
                if prob:
                    problems[prob] = problems.get(prob, 0) + 1

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# BUAS® — INFORME DE MERCADO\n\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}\n\n")
        f.write("---\n\n")

        f.write("## Resumen ejecutivo\n\n")
        f.write(f"- **Empresas descubiertas**: {stats['total']}\n")
        f.write(f"- **Empresas puntuadas**: {stats['scored']}\n")
        for pri, count in sorted(stats["by_priority"].items()):
            f.write(f"- **Prioridad {pri}**: {count}\n")
        f.write("\n")

        f.write("## Sectores con mayor potencial\n\n")
        for sector in sorted(sector_scores.keys(),
                           key=lambda s: sum(sector_scores[s]) / len(sector_scores[s]),
                           reverse=True):
            avg = sum(sector_scores[sector]) / len(sector_scores[sector])
            f.write(f"- **{sector}**: {sector_counts[sector]} empresas, score medio {avg:.0f}/100\n")
        f.write("\n")

        f.write("## Territorios con mejores oportunidades\n\n")
        for loc in sorted(region_counts.keys(), key=lambda k: region_counts[k], reverse=True):
            f.write(f"- **{loc}**: {region_counts[loc]} empresas\n")
        f.write("\n")

        f.write("## Problemas de branding más recurrentes\n\n")
        for prob in sorted(problems.keys(), key=lambda k: problems[k], reverse=True)[:10]:
            f.write(f"- {prob}: {problems[prob]} empresas\n")
        f.write("\n")

    return filepath


def generate_action_plan(prospects, filepath="output/06_plan_accion.md"):
    """Generate ENTREGABLE 6: Action Plan for top 10-15."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# BUAS® — PLAN DE ACCIÓN COMERCIAL\n\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}\n\n")
        f.write("---\n\n")

        for i, p in enumerate(prospects, 1):
            f.write(f"## {i}. {p.nombre_comercial or p.nombre_empresa}\n\n")
            f.write(f"**Sector**: {p.sector} | **Localización**: {p.ciudad}\n")
            f.write(f"**Score**: {p.score_total}/100 | **Prioridad**: {p.prioridad}\n\n")

            f.write(f"**Por qué contactar**: {p.motivo_contacto_ahora or p.descripcion_oportunidad}\n\n")
            f.write(f"**Servicio a ofrecer**: {p.servicio_potencial}\n\n")
            f.write(f"**Argumento comercial**: {p.argumento_comercial}\n\n")
            f.write(f"**Vía de contacto**: {p.via_contacto}\n\n")

            if p.proyecto_potencial:
                f.write(f"**Idea de proyecto**: {p.proyecto_potencial}\n\n")
            if p.ticket_potencial:
                f.write(f"**Presupuesto orientativo**: {p.ticket_potencial}\n\n")

            f.write(f"**Mejor momento**: Ahora\n\n")
            f.write(f"**Próximo paso**: Preparar presentación personalizada con análisis de su marca actual y propuesta de mejora.\n\n")
            f.write("---\n\n")

    return filepath


def generate_prospect_dossier(prospect, filepath=None):
    """Generate a full dossier for a single prospect."""
    p = prospect
    if not filepath:
        safe_name = p.nombre_empresa.replace(" ", "_").replace("/", "_")[:40]
        filepath = f"output/dossiers/{safe_name}.md"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {p.nombre_comercial or p.nombre_empresa}\n\n")
        f.write(f"**Score**: {p.score_total}/100 — **Prioridad {p.prioridad}**\n\n")

        f.write("## Identificación\n\n")
        f.write(f"| Campo | Valor |\n|---|---|\n")
        f.write(f"| Empresa | {p.nombre_empresa} |\n")
        f.write(f"| Nombre comercial | {p.nombre_comercial} |\n")
        f.write(f"| Sector | {p.sector} — {p.subsector} |\n")
        f.write(f"| Localización | {p.ciudad}, {p.pais} |\n")
        f.write(f"| Web | {p.url} |\n")
        f.write(f"| Instagram | {p.instagram} |\n")
        f.write(f"| LinkedIn | {p.linkedin} |\n")
        f.write(f"| Detectada | {p.fecha_deteccion} |\n\n")

        f.write("## Negocio\n\n")
        f.write(f"- **Qué vende**: {p.descripcion_negocio}\n")
        f.write(f"- **Público objetivo**: {p.publico_objetivo}\n")
        f.write(f"- **Posicionamiento**: {p.posicionamiento}\n")
        f.write(f"- **Modelo de negocio**: {p.modelo_negocio}\n")
        f.write(f"- **Tamaño estimado**: {p.tamano_estimado}\n")
        f.write(f"- **Ubicaciones**: {p.num_ubicaciones}\n")
        f.write(f"- **Presencia**: {p.presencia}\n")
        f.write(f"- **Competidores**: {p.competidores}\n\n")

        f.write("## Análisis de marca\n\n")
        f.write(f"- **Calidad de identidad visual**: {p.calidad_identidad}\n")
        f.write(f"- **Personalidad**: {p.personalidad_marca}\n")
        f.write(f"- **Coherencia**: {p.coherencia_marca}\n")
        f.write(f"- **Diferenciación**: {p.diferenciacion}\n")
        f.write(f"- **Percepción de valor**: {p.percepcion_valor}\n")
        f.write(f"- **Problemas detectados**: {p.problemas_marca}\n\n")

        f.write("## Análisis web\n\n")
        f.write(f"- **URL**: {p.url}\n")
        f.write(f"- **Diseño**: {p.web_diseno}\n")
        f.write(f"- **UX/UI**: {p.web_ux}\n")
        f.write(f"- **Arquitectura**: {p.web_arquitectura}\n")
        f.write(f"- **Experiencia móvil**: {p.web_movil}\n")
        f.write(f"- **Copywriting**: {p.web_copywriting}\n")
        f.write(f"- **Conversión**: {p.web_conversion}\n")
        f.write(f"- **Aspectos mejorables**: {p.web_mejoras}\n\n")

        f.write("## Oportunidad\n\n")
        f.write(f"- **Señal detectada**: {p.senal_detectada}\n")
        f.write(f"- **Fecha señal**: {p.fecha_senal}\n")
        f.write(f"- **Fuente**: {p.fuente_senal}\n")
        f.write(f"- **Motivo de oportunidad**: {p.descripcion_oportunidad}\n")
        f.write(f"- **Servicio potencial**: {p.servicio_potencial}\n")
        f.write(f"- **Idea de proyecto**: {p.proyecto_potencial}\n")
        f.write(f"- **Presupuesto potencial**: {p.ticket_potencial}\n\n")

        f.write("## Scoring\n\n")
        f.write(f"| Dimensión | Puntos | Máximo |\n|---|---|---|\n")
        f.write(f"| Encaje creativo | {p.score_encaje_creativo} | 25 |\n")
        f.write(f"| Necesidad branding/web | {p.score_necesidad} | 20 |\n")
        f.write(f"| Capacidad económica | {p.score_capacidad_economica} | 20 |\n")
        f.write(f"| Momento de oportunidad | {p.score_momento} | 15 |\n")
        f.write(f"| Potencial portfolio | {p.score_portfolio} | 10 |\n")
        f.write(f"| Accesibilidad decisor | {p.score_accesibilidad} | 10 |\n")
        f.write(f"| **TOTAL** | **{p.score_total}** | **100** |\n\n")

        if p.argumento_comercial:
            f.write("## Argumento comercial\n\n")
            f.write(f"{p.argumento_comercial}\n\n")

        if p.via_contacto:
            f.write("## Contacto\n\n")
            f.write(f"- **Contacto corporativo**: {p.contacto_corporativo}\n")
            if p.nombre_decisor:
                f.write(f"- **Decisor**: {p.nombre_decisor} ({p.cargo_decisor})\n")
            f.write(f"- **Vía de contacto**: {p.via_contacto}\n")
            f.write(f"- **Estado**: {p.estado_comercial}\n\n")

        f.write(f"---\n*Fuente: {p.fuente_origen} | Verificado: {'Sí' if p.verificado else 'No'}*\n")

    return filepath
