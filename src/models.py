"""
BUAS Prospecting Intelligence System - Data Models
"""
import json
import csv
import os
from datetime import datetime
from typing import Optional


class Prospect:
    """A single prospect company with all fields from the BUAS spec."""

    def __init__(self, **kwargs):
        # Identification
        self.nombre_empresa = kwargs.get("nombre_empresa", "")
        self.nombre_comercial = kwargs.get("nombre_comercial", "")
        self.sector = kwargs.get("sector", "")
        self.subsector = kwargs.get("subsector", "")
        self.localizacion = kwargs.get("localizacion", "")
        self.pais = kwargs.get("pais", "España")
        self.url = kwargs.get("url", "")
        self.instagram = kwargs.get("instagram", "")
        self.linkedin = kwargs.get("linkedin", "")
        self.fecha_deteccion = kwargs.get("fecha_deteccion", datetime.now().strftime("%Y-%m-%d"))

        # Business
        self.que_vende = kwargs.get("que_vende", "")
        self.publico_objetivo = kwargs.get("publico_objetivo", "")
        self.posicionamiento = kwargs.get("posicionamiento", "")
        self.modelo_negocio = kwargs.get("modelo_negocio", "")
        self.tamano_estimado = kwargs.get("tamano_estimado", "")
        self.num_ubicaciones = kwargs.get("num_ubicaciones", "")
        self.presencia = kwargs.get("presencia", "")
        self.competidores = kwargs.get("competidores", "")

        # Brand
        self.calidad_identidad = kwargs.get("calidad_identidad", "")
        self.personalidad_marca = kwargs.get("personalidad_marca", "")
        self.coherencia_marca = kwargs.get("coherencia_marca", "")
        self.diferenciacion = kwargs.get("diferenciacion", "")
        self.percepcion_valor = kwargs.get("percepcion_valor", "")
        self.problemas_marca = kwargs.get("problemas_marca", "")

        # Web
        self.web_diseno = kwargs.get("web_diseno", "")
        self.web_ux = kwargs.get("web_ux", "")
        self.web_arquitectura = kwargs.get("web_arquitectura", "")
        self.web_movil = kwargs.get("web_movil", "")
        self.web_copywriting = kwargs.get("web_copywriting", "")
        self.web_conversion = kwargs.get("web_conversion", "")
        self.web_mejoras = kwargs.get("web_mejoras", "")

        # Opportunity
        self.senal_detectada = kwargs.get("senal_detectada", "")
        self.fecha_senal = kwargs.get("fecha_senal", "")
        self.fuente_senal = kwargs.get("fuente_senal", "")
        self.motivo_oportunidad = kwargs.get("motivo_oportunidad", "")
        self.servicio_potencial = kwargs.get("servicio_potencial", "")
        self.idea_proyecto = kwargs.get("idea_proyecto", "")
        self.presupuesto_rango = kwargs.get("presupuesto_rango", "")
        self.score_total = kwargs.get("score_total", 0)
        self.prioridad = kwargs.get("prioridad", "")

        # Score breakdown
        self.score_encaje_creativo = kwargs.get("score_encaje_creativo", 0)
        self.score_necesidad = kwargs.get("score_necesidad", 0)
        self.score_capacidad_economica = kwargs.get("score_capacidad_economica", 0)
        self.score_momento = kwargs.get("score_momento", 0)
        self.score_portfolio = kwargs.get("score_portfolio", 0)
        self.score_accesibilidad = kwargs.get("score_accesibilidad", 0)

        # Contact
        self.contacto_corporativo = kwargs.get("contacto_corporativo", "")
        self.nombre_decisor = kwargs.get("nombre_decisor", "")
        self.cargo_decisor = kwargs.get("cargo_decisor", "")
        self.fuente_contacto = kwargs.get("fuente_contacto", "")
        self.via_contacto = kwargs.get("via_contacto", "")
        self.estado_comercial = kwargs.get("estado_comercial", "Nuevo")

        # Deep analysis (for top 30)
        self.analisis_problema = kwargs.get("analisis_problema", "")
        self.oportunidad_negocio = kwargs.get("oportunidad_negocio", "")
        self.oportunidad_branding = kwargs.get("oportunidad_branding", "")
        self.oportunidad_web = kwargs.get("oportunidad_web", "")
        self.posible_proyecto = kwargs.get("posible_proyecto", "")
        self.motivo_contacto = kwargs.get("motivo_contacto", "")
        self.mejor_momento = kwargs.get("mejor_momento", "")
        self.argumento_comercial = kwargs.get("argumento_comercial", "")

        # Metadata
        self.fuente_origen = kwargs.get("fuente_origen", "")
        self.notas = kwargs.get("notas", "")
        self.verificado = kwargs.get("verificado", False)

    def calculate_score(self):
        self.score_total = (
            self.score_encaje_creativo
            + self.score_necesidad
            + self.score_capacidad_economica
            + self.score_momento
            + self.score_portfolio
            + self.score_accesibilidad
        )
        if self.score_total >= 80:
            self.prioridad = "A"
        elif self.score_total >= 65:
            self.prioridad = "B"
        elif self.score_total >= 45:
            self.prioridad = "C"
        else:
            self.prioridad = "DESCARTAR"
        return self.score_total

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


class ProspectDatabase:
    """Manages the full prospect database."""

    def __init__(self, filepath="data/prospects.json"):
        self.filepath = filepath
        self.prospects: list[Prospect] = []
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.prospects = [Prospect.from_dict(p) for p in data]

    def save(self):
        os.makedirs(os.path.dirname(self.filepath) or ".", exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.prospects], f, ensure_ascii=False, indent=2)

    def add(self, prospect: Prospect):
        for existing in self.prospects:
            if existing.nombre_empresa.lower() == prospect.nombre_empresa.lower():
                return False
        self.prospects.append(prospect)
        return True

    def add_many(self, prospects: list[Prospect]) -> int:
        added = 0
        for p in prospects:
            if self.add(p):
                added += 1
        return added

    def get_by_priority(self, priority: str) -> list[Prospect]:
        return [p for p in self.prospects if p.prioridad == priority]

    def get_top_n(self, n: int) -> list[Prospect]:
        scored = sorted(self.prospects, key=lambda p: p.score_total, reverse=True)
        return scored[:n]

    def get_by_sector(self, sector: str) -> list[Prospect]:
        return [p for p in self.prospects if p.sector.lower() == sector.lower()]

    def get_scored(self) -> list[Prospect]:
        return [p for p in self.prospects if p.score_total > 0]

    def stats(self) -> dict:
        total = len(self.prospects)
        scored = len(self.get_scored())
        by_priority = {}
        for p in self.prospects:
            pri = p.prioridad or "Sin puntuar"
            by_priority[pri] = by_priority.get(pri, 0) + 1
        by_sector = {}
        for p in self.prospects:
            s = p.sector or "Sin sector"
            by_sector[s] = by_sector.get(s, 0) + 1
        return {
            "total": total,
            "scored": scored,
            "by_priority": by_priority,
            "by_sector": by_sector,
        }

    def export_csv(self, filepath: str, prospects: Optional[list[Prospect]] = None):
        data = prospects or self.prospects
        if not data:
            return
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        fieldnames = list(data[0].to_dict().keys())
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for p in data:
                writer.writerow(p.to_dict())
