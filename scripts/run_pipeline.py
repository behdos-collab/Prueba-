#!/usr/bin/env python3
"""
BUAS Prospecting Intelligence System — Full Pipeline
Consolidates all sector data, scores, filters, and generates deliverables.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import glob
from src.models import Prospect, ProspectDatabase
from src.scoring import score_prospect
from src.reports import generate_market_report, generate_action_plan, generate_prospect_dossier


def load_all_sectors():
    prospects = []
    for path in sorted(glob.glob("data/sector_*.json")):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            for entry in data:
                prospects.append(Prospect.from_dict(entry))
        print(f"  Loaded {len(data)} from {os.path.basename(path)}")
    return prospects


def main():
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))

    print("=" * 60)
    print("BUAS® — PROSPECTING INTELLIGENCE SYSTEM")
    print("=" * 60)

    # Phase 1: Load all sector data
    print("\n[1/6] Loading sector research data...")
    all_prospects = load_all_sectors()
    print(f"  Total loaded: {len(all_prospects)}")

    # Phase 2: Consolidate into database (deduplicates)
    print("\n[2/6] Consolidating into database...")
    db = ProspectDatabase("data/prospects.json")
    db.prospects = []  # start fresh
    added = db.add_many(all_prospects)
    print(f"  Added: {added} (after deduplication)")

    # Phase 3: Score all prospects
    print("\n[3/6] Scoring all prospects...")
    for p in db.prospects:
        score_prospect(p)
    db.save()

    stats = db.stats()
    print(f"  Scored: {stats['scored']}")
    for pri in ["A", "B", "C", "DESCARTAR"]:
        count = stats["by_priority"].get(pri, 0)
        print(f"  Priority {pri}: {count}")

    # Phase 4: Generate deliverables
    print("\n[4/6] Generating deliverables...")

    # ENTREGABLE 1: Full database CSV
    db.export_csv("output/01_base_datos_completa.csv")
    print(f"  [1] Base de datos completa: {len(db.prospects)} empresas")

    # ENTREGABLE 2: Top 100
    top100 = db.get_top_n(100)
    db.export_csv("output/02_top_100.csv", top100)
    print(f"  [2] Top 100: {len(top100)} empresas (min score: {top100[-1].score_total})")

    # ENTREGABLE 3: Top 30
    top30 = db.get_top_n(30)
    db.export_csv("output/03_top_30.csv", top30)
    print(f"  [3] Top 30: {len(top30)} empresas (min score: {top30[-1].score_total})")

    # ENTREGABLE 4: Top 10-15 with dossiers
    top15 = db.get_top_n(15)
    db.export_csv("output/04_top_15_shortlist.csv", top15)
    print(f"  [4] Top 15 shortlist: {len(top15)} empresas (min score: {top15[-1].score_total})")

    os.makedirs("output/dossiers", exist_ok=True)
    for p in top15:
        generate_prospect_dossier(p)
    print(f"  Generated {len(top15)} individual dossiers")

    # ENTREGABLE 5: Market Report
    report_path = generate_market_report(db)
    print(f"  [5] Informe de mercado: {report_path}")

    # ENTREGABLE 6: Action Plan
    plan_path = generate_action_plan(top15)
    print(f"  [6] Plan de acción: {plan_path}")

    # Summary
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)
    print(f"\nTotal empresas descubiertas: {len(db.prospects)}")
    print(f"Top 100 (score >= {top100[-1].score_total})")
    print(f"Top 30  (score >= {top30[-1].score_total})")
    print(f"Top 15  (score >= {top15[-1].score_total})")
    print(f"\nTop 5 prospects:")
    for i, p in enumerate(db.get_top_n(5), 1):
        print(f"  {i}. {p.nombre_comercial or p.nombre_empresa} — {p.score_total}/100 ({p.prioridad}) — {p.ciudad}")

    print(f"\nDeliverables in output/:")
    for f in sorted(os.listdir("output")):
        if not f.startswith("."):
            full = os.path.join("output", f)
            if os.path.isfile(full):
                size = os.path.getsize(full)
                print(f"  {f} ({size:,} bytes)")
            elif os.path.isdir(full):
                count = len(os.listdir(full))
                print(f"  {f}/ ({count} files)")


if __name__ == "__main__":
    main()
