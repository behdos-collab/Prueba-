#!/usr/bin/env python3
"""
BUAS® Growth Intelligence & Opportunity Detection System
Script de compilación v2: unifica datos, aplica scoring y genera 7 entregables.
"""
import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from models import Prospect, ProspectDatabase
from scoring import score_prospect
from reports import (
    generate_top100_report,
    generate_top30_report,
    generate_top15_report,
    generate_top10_dossiers,
    generate_market_report,
    generate_action_plan,
)


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
                    count = 0
                    for item in data:
                        if isinstance(item, dict) and item.get("nombre_empresa"):
                            all_prospects.append(item)
                            count += 1
                    print(f"  {sf}: {count} empresas cargadas")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"  {sf}: error — {e}")

    return all_prospects


def deduplicate(prospects):
    """Elimina duplicados por nombre de empresa (case-insensitive)."""
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
    print("BUAS® — GROWTH INTELLIGENCE & OPPORTUNITY DETECTION SYSTEM")
    print(f"Compilación v2: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)

    # 1. Cargar datos de todos los sectores
    print("\n1. CARGANDO DATOS DE SECTORES...")
    raw = load_sector_files("data")
    print(f"   Total bruto: {len(raw)} registros")

    # 2. Deduplicar
    print("\n2. DEDUPLICANDO...")
    unique = deduplicate(raw)
    print(f"   Tras deduplicación: {len(unique)} empresas únicas")

    # 3. Crear base de datos y aplicar scoring
    print("\n3. APLICANDO SCORING (6 dimensiones, 100 pts)...")
    db = ProspectDatabase("data/prospects.json")
    db.prospects = []

    for item in unique:
        p = Prospect(**item)
        score_prospect(p)
        db.prospects.append(p)

    db.save()
    stats = db.stats()
    print(f"   Total en BD: {stats['total']}")
    print(f"   Puntuadas: {stats['scored']}")
    print(f"   Por prioridad: {stats['by_priority']}")

    # Preparar listas
    top100 = db.get_top_n(100)
    top30 = db.get_top_n(30)
    top15 = db.get_top_n(15)
    top10 = db.get_top_n(10)

    # 4. RESULTADO 01 — Master Database CSV
    print("\n4. RESULTADO 01 — MASTER DATABASE CSV...")
    db.export_csv("output/01_master_database.csv")
    print(f"   -> output/01_master_database.csv ({len(db.prospects)} registros)")

    # 5. RESULTADO 02 — Top 100
    print("\n5. RESULTADO 02 — TOP 100...")
    db.export_csv("output/02_top_100.csv", top100)
    generate_top100_report(top100)
    print(f"   -> output/02_top_100.csv + .md ({len(top100)} empresas)")

    # 6. RESULTADO 03 — Top 30
    print("\n6. RESULTADO 03 — TOP 30 (análisis)...")
    db.export_csv("output/03_top_30.csv", top30)
    generate_top30_report(top30)
    print(f"   -> output/03_top_30.csv + .md")

    # 7. RESULTADO 04 — Top 15
    print("\n7. RESULTADO 04 — TOP 15 (oportunidades prioritarias)...")
    db.export_csv("output/04_top_15.csv", top15)
    generate_top15_report(top15)
    print(f"   -> output/04_top_15.csv + .md")

    # 8. RESULTADO 05 — Top 10 dossiers
    print("\n8. RESULTADO 05 — TOP 10 (dossiers individuales)...")
    generate_top10_dossiers(top10)
    print(f"   -> output/dossiers/ ({len(top10[:10])} dossiers)")

    # 9. RESULTADO 06 — Market Intelligence Report
    print("\n9. RESULTADO 06 — INFORME DE INTELIGENCIA DE MERCADO...")
    generate_market_report(db)
    print("   -> output/06_informe_mercado.md")

    # 10. RESULTADO 07 — Action Plan
    print("\n10. RESULTADO 07 — PLAN DE ACCIÓN (4 semanas)...")
    generate_action_plan(top10)
    print("    -> output/07_plan_accion.md")

    # Summary
    print("\n" + "=" * 60)
    print("COMPILACIÓN COMPLETADA")
    print(f"  Empresas en base de datos: {stats['total']}")
    print(f"  Top 100: {min(100, stats['total'])} empresas")
    print(f"  Top 30 analizadas: {min(30, stats['total'])} empresas")
    print(f"  Top 15 oportunidades: {min(15, stats['total'])} empresas")
    print(f"  Top 10 con dossier: {min(10, stats['total'])} empresas")
    print()
    print("  Top 10 empresas:")
    for i, p in enumerate(top10, 1):
        name = p.nombre_comercial or p.nombre_empresa
        print(f"    {i}. {name} — {p.score_total}/100 ({p.prioridad}) — {p.sector}, {p.ciudad}")
    print("=" * 60)


if __name__ == "__main__":
    main()
