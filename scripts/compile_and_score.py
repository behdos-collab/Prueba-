#!/usr/bin/env python3
"""
BUAS® Prospecting Intelligence System
Script de compilación: unifica datos de todos los sectores, aplica scoring y genera entregables.
"""
import sys
import os
import json
import csv
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from models import Prospect, ProspectDatabase
from scoring import score_prospect
from reports import generate_market_report, generate_action_plan, generate_prospect_dossier


def load_sector_files(data_dir="data"):
    """Carga todos los archivos JSON de sectores."""
    all_prospects = []
    sector_files = [f for f in os.listdir(data_dir) if f.startswith("sector_") and f.endswith(".json")]

    for sf in sorted(sector_files):
        filepath = os.path.join(data_dir, sf)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get("nombre_empresa"):
                            all_prospects.append(item)
                    print(f"  {sf}: {len(data)} empresas cargadas")
                else:
                    print(f"  {sf}: formato inesperado, saltando")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"  {sf}: error al cargar - {e}")

    return all_prospects


def deduplicate(prospects):
    """Elimina duplicados por nombre de empresa."""
    seen = set()
    unique = []
    for p in prospects:
        name = p.get("nombre_empresa", "").strip().lower()
        if name and name not in seen:
            seen.add(name)
            unique.append(p)
    return unique


def main():
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))

    print("=" * 60)
    print("BUAS® — SISTEMA DE INTELIGENCIA DE PROSPECCIÓN")
    print(f"Compilación: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)

    # 1. Cargar datos de todos los sectores
    print("\n1. CARGANDO DATOS DE SECTORES...")
    raw_prospects = load_sector_files("data")
    print(f"   Total bruto: {len(raw_prospects)} empresas")

    # 2. Deduplicar
    print("\n2. DEDUPLICANDO...")
    unique = deduplicate(raw_prospects)
    print(f"   Tras deduplicación: {len(unique)} empresas únicas")

    # 3. Crear base de datos y aplicar scoring
    print("\n3. CREANDO BASE DE DATOS Y APLICANDO SCORING...")
    db = ProspectDatabase("data/prospects.json")
    db.prospects = []  # reset

    for item in unique:
        p = Prospect(**item)
        score_prospect(p)
        db.prospects.append(p)

    db.save()
    stats = db.stats()
    print(f"   Total en BD: {stats['total']}")
    print(f"   Puntuadas: {stats['scored']}")
    print(f"   Por prioridad: {stats['by_priority']}")
    print(f"   Por sector: {stats['by_sector']}")

    # 4. ENTREGABLE 1 — Base de datos CSV completa
    print("\n4. GENERANDO ENTREGABLE 1 — BASE DE DATOS CSV...")
    db.export_csv("output/01_base_datos_completa.csv")
    print(f"   -> output/01_base_datos_completa.csv ({len(db.prospects)} registros)")

    # 5. ENTREGABLE 2 — Top 100
    print("\n5. GENERANDO ENTREGABLE 2 — TOP 100...")
    top100 = db.get_top_n(100)
    db.export_csv("output/02_top_100.csv", top100)

    # Generar también resumen MD
    with open("output/02_top_100.md", "w", encoding="utf-8") as f:
        f.write("# BUAS® — TOP 100 EMPRESAS POTENCIALES\n\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}\n\n")
        f.write("| # | Empresa | Sector | Localización | Score | Prioridad |\n")
        f.write("|---|---------|--------|-------------|-------|----------|\n")
        for i, p in enumerate(top100, 1):
            f.write(f"| {i} | {p.nombre_comercial or p.nombre_empresa} | {p.sector} | {p.localizacion} | {p.score_total} | {p.prioridad} |\n")
    print(f"   -> output/02_top_100.csv + .md ({len(top100)} empresas)")

    # 6. ENTREGABLE 3 — Top 30
    print("\n6. GENERANDO ENTREGABLE 3 — TOP 30 (análisis profundo)...")
    top30 = db.get_top_n(30)
    db.export_csv("output/03_top_30.csv", top30)

    with open("output/03_top_30.md", "w", encoding="utf-8") as f:
        f.write("# BUAS® — TOP 30 EMPRESAS ANALIZADAS\n\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}\n\n")
        f.write("---\n\n")
        for i, p in enumerate(top30, 1):
            f.write(f"## {i}. {p.nombre_comercial or p.nombre_empresa}\n\n")
            f.write(f"**Sector**: {p.sector} — {p.subsector}  \n")
            f.write(f"**Localización**: {p.localizacion}  \n")
            f.write(f"**Score**: {p.score_total}/100 — Prioridad **{p.prioridad}**  \n")
            f.write(f"**Web**: {p.url}  \n\n")
            f.write(f"**Qué vende**: {p.que_vende}  \n")
            f.write(f"**Posicionamiento**: {p.posicionamiento}  \n")
            f.write(f"**Tamaño**: {p.tamano_estimado}  \n\n")
            f.write(f"**Señal detectada**: {p.senal_detectada}  \n")
            f.write(f"**Problemas de marca**: {p.problemas_marca}  \n")
            f.write(f"**Mejoras web**: {p.web_mejoras}  \n\n")
            f.write(f"**Servicio potencial BUAS**: {p.servicio_potencial}  \n")
            f.write(f"**Presupuesto orientativo**: {p.presupuesto_rango}  \n")
            f.write(f"**Motivo de oportunidad**: {p.motivo_oportunidad}  \n\n")

            f.write("**Desglose scoring**:\n")
            f.write(f"- Encaje creativo: {p.score_encaje_creativo}/25\n")
            f.write(f"- Necesidad branding/web: {p.score_necesidad}/20\n")
            f.write(f"- Capacidad económica: {p.score_capacidad_economica}/20\n")
            f.write(f"- Momento oportunidad: {p.score_momento}/15\n")
            f.write(f"- Potencial portfolio: {p.score_portfolio}/10\n")
            f.write(f"- Accesibilidad decisor: {p.score_accesibilidad}/10\n\n")
            f.write("---\n\n")
    print(f"   -> output/03_top_30.csv + .md")

    # 7. ENTREGABLE 4 — Top 10-15 (shortlist)
    print("\n7. GENERANDO ENTREGABLE 4 — SHORTLIST TOP 15...")
    top15 = db.get_top_n(15)
    db.export_csv("output/04_shortlist_top15.csv", top15)

    # Generar dossiers individuales
    os.makedirs("output/dossiers", exist_ok=True)
    for p in top15:
        generate_prospect_dossier(p)

    with open("output/04_shortlist_top15.md", "w", encoding="utf-8") as f:
        f.write("# BUAS® — SHORTLIST: 15 MEJORES OPORTUNIDADES\n\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}\n\n")
        f.write("Estas son las empresas que BUAS debería contactar primero.\n\n")
        f.write("---\n\n")
        for i, p in enumerate(top15, 1):
            f.write(f"## {i}. {p.nombre_comercial or p.nombre_empresa}\n\n")
            f.write(f"**{p.sector}** | {p.localizacion} | Score: **{p.score_total}/100** | Prioridad **{p.prioridad}**\n\n")
            f.write(f"**Qué hace**: {p.que_vende}\n\n")
            f.write(f"**Por qué BUAS**: {p.motivo_oportunidad or p.problemas_marca}\n\n")
            f.write(f"**Servicio a ofrecer**: {p.servicio_potencial}\n\n")
            f.write(f"**Presupuesto estimado**: {p.presupuesto_rango}\n\n")
            f.write(f"**Señal**: {p.senal_detectada} ({p.fecha_senal})\n\n")
            f.write(f"**Web**: {p.url}\n\n")
            if p.argumento_comercial:
                f.write(f"**Argumento comercial**: {p.argumento_comercial}\n\n")
            f.write("---\n\n")
    print(f"   -> output/04_shortlist_top15.csv + .md + {len(top15)} dossiers")

    # 8. ENTREGABLE 5 — Informe de mercado
    print("\n8. GENERANDO ENTREGABLE 5 — INFORME DE MERCADO...")
    generate_market_report(db)
    print("   -> output/05_informe_mercado.md")

    # 9. ENTREGABLE 6 — Plan de acción
    print("\n9. GENERANDO ENTREGABLE 6 — PLAN DE ACCIÓN...")
    generate_action_plan(top15)
    print("   -> output/06_plan_accion.md")

    print("\n" + "=" * 60)
    print("COMPILACIÓN COMPLETADA")
    print(f"Total empresas en base de datos: {stats['total']}")
    print(f"Top 100 generado: {min(100, stats['total'])} empresas")
    print(f"Top 30 con análisis: {min(30, stats['total'])} empresas")
    print(f"Shortlist final: {min(15, stats['total'])} empresas")
    print("=" * 60)


if __name__ == "__main__":
    main()
