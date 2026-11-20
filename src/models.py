"""
BUAS® Growth Intelligence & Opportunity Detection System — Data Models v2
"""
import json
import csv
import os
from datetime import datetime
from typing import Optional

# Signal types per spec v2
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

# Project tiers per spec v2
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

SECTORS = [
    "Hospitality & Experiences",
    "Food & Beverage",
    "Lifestyle, Beauty & Consumer",
    "Architecture, Real Estate & Spaces",
    "Technology & B2B",
]


class Prospect:
    """A single prospect company — full field set per BUAS spec v2."""

    def __init__(self, **kwargs):
        # --- IDENTIFICATION ---
        self.nombre_empresa = kwargs.get("nombre_empresa", "")
        self.nombre_comercial = kwargs.get("nombre_comercial", "")
        self.sector = kwargs.get("sector", "")
        self.subsector = kwargs.get("subsector", "")
        self.ciudad = kwargs.get("ciudad", kwargs.get("localizacion", ""))
        self.provincia = kwargs.get("provincia", "")
        self.pais = kwargs.get("pais", "España")
        self.url = kwargs.get("url", "")
        self.instagram = kwargs.get("instagram", "")
        self.linkedin = kwargs.get("linkedin", "")
        self.otros_canales = kwargs.get("otros_canales", "")
        self.fecha_deteccion = kwargs.get("fecha_deteccion", datetime.now().strftime("%Y-%m-%d"))

        # Backwards compat: localizacion -> ciudad
        if not self.ciudad and kwargs.get("localizacion"):
            self.ciudad = kwargs["localizacion"]

        # --- BUSINESS ---
        self.descripcion_negocio = kwargs.get("descripcion_negocio", kwargs.get("que_vende", ""))
        self.productos_servicios = kwargs.get("productos_servicios", "")
        self.modelo_negocio = kwargs.get("modelo_negocio", "")
        self.publico_objetivo = kwargs.get("publico_objetivo", "")
        self.posicionamiento = kwargs.get("posicionamiento", "")
        self.tamano_estimado = kwargs.get("tamano_estimado", "")
        self.capacidad_economica = kwargs.get("capacidad_economica", "")
        self.competidores = kwargs.get("competidores", "")
        self.num_ubicaciones = kwargs.get("num_ubicaciones", "")
        self.presencia = kwargs.get("presencia", "")

        # --- BRAND ---
        self.calidad_identidad = kwargs.get("calidad_identidad", "")
        self.personalidad_marca = kwargs.get("personalidad_marca", "")
        self.coherencia_marca = kwargs.get("coherencia_marca", "")
        self.diferenciacion = kwargs.get("diferenciacion", "")
        self.percepcion_valor = kwargs.get("percepcion_valor", "")
        self.problemas_marca = kwargs.get("problemas_marca", "")

        # --- WEB / DIGITAL ---
        self.web_diseno = kwargs.get("web_diseno", "")
        self.web_ux = kwargs.get("web_ux", "")
        self.web_arquitectura = kwargs.get("web_arquitectura", "")
        self.web_movil = kwargs.get("web_movil", "")
        self.web_copywriting = kwargs.get("web_copywriting", "")
        self.web_conversion = kwargs.get("web_conversion", "")
        self.web_mejoras = kwargs.get("web_mejoras", "")

        # --- OPPORTUNITY ---
        self.signal_type = kwargs.get("signal_type", "")  # one of SIGNAL_TYPES keys
        self.senal_detectada = kwargs.get("senal_detectada", "")
        self.descripcion_oportunidad = kwargs.get("descripcion_oportunidad", kwargs.get("motivo_oportunidad", ""))
        self.fecha_senal = kwargs.get("fecha_senal", "")
        self.fuente_senal = kwargs.get("fuente_senal", "")
        self.evidencia = kwargs.get("evidencia", "")
        self.necesidad_branding = kwargs.get("necesidad_branding", "")
        self.necesidad_digital = kwargs.get("necesidad_digital", "")
        self.necesidad_packaging = kwargs.get("necesidad_packaging", "")
        self.necesidad_estrategica = kwargs.get("necesidad_estrategica", "")
        self.potencial_transformacion = kwargs.get("potencial_transformacion", "")

        # --- BUAS FIT ---
        self.encaje_creativo = kwargs.get("encaje_creativo", "")
        self.potencial_portfolio = kwargs.get("potencial_portfolio", "")
        self.tipo_proyecto = kwargs.get("tipo_proyecto", "")  # PROJECT_TIERS key
        self.servicio_potencial = kwargs.get("servicio_potencial", "")
        self.ticket_potencial = kwargs.get("ticket_potencial", kwargs.get("presupuesto_rango", ""))
        self.justificacion_buas = kwargs.get("justificacion_buas", "")

        # --- SCORING ---
        self.score_encaje_creativo = kwargs.get("score_encaje_creativo", 0)
        self.score_necesidad = kwargs.get("score_necesidad", 0)
        self.score_capacidad_economica = kwargs.get("score_capacidad_economica", 0)
        self.score_momento = kwargs.get("score_momento", 0)
        self.score_portfolio = kwargs.get("score_portfolio", 0)
        self.score_accesibilidad = kwargs.get("score_accesibilidad", 0)
        self.score_total = kwargs.get("score_total", 0)
        self.prioridad = kwargs.get("prioridad", "")

        # --- COMMERCIAL ---
        self.contacto_corporativo = kwargs.get("contacto_corporativo", "")
        self.nombre_decisor = kwargs.get("nombre_decisor", "")
        self.cargo_decisor = kwargs.get("cargo_decisor", "")
        self.fuente_contacto = kwargs.get("fuente_contacto", "")
        self.via_contacto = kwargs.get("via_contacto", "")
        self.estado_comercial = kwargs.get("estado_comercial", "Nuevo")
        self.proxima_accion = kwargs.get("proxima_accion", "")
        self.fecha_revision = kwargs.get("fecha_revision", "")

        # --- DEEP ANALYSIS (top 10-15) ---
        self.analisis_fase_negocio = kwargs.get("analisis_fase_negocio", "")
        self.oportunidad_crecimiento = kwargs.get("oportunidad_crecimiento", "")
        self.problema_branding = kwargs.get("problema_branding", "")
        self.problema_digital = kwargs.get("problema_digital", "")
        self.proyecto_potencial = kwargs.get("proyecto_potencial", kwargs.get("idea_proyecto", ""))
        self.argumento_comercial = kwargs.get("argumento_comercial", "")
        self.motivo_contacto_ahora = kwargs.get("motivo_contacto_ahora", kwargs.get("motivo_contacto", ""))
        self.por_que_buas = kwargs.get("por_que_buas", "")

        # --- EVIDENCE ---
        self.fuente_origen = kwargs.get("fuente_origen", "")
        self.urls_evidencia = kwargs.get("urls_evidencia", "")
        self.fecha_consulta = kwargs.get("fecha_consulta", kwargs.get("fecha_deteccion", ""))
        self.notas = kwargs.get("notas", "")
        self.verificado = kwargs.get("verificado", False)
        self.tipo_dato = kwargs.get("tipo_dato", "")  # HECHO / EVIDENCIA / HIPÓTESIS / RECOMENDACIÓN

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

    def to_csv_dict(self):
        """Flat dict for CSV export with clean column names."""
        d = self.to_dict()
        return {k.replace("_", " ").title(): v for k, v in d.items()}

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
        name = prospect.nombre_empresa.strip().lower()
        for existing in self.prospects:
            if existing.nombre_empresa.strip().lower() == name:
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
        return [p for p in self.prospects if sector.lower() in p.sector.lower()]

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
        by_region = {}
        for p in self.prospects:
            r = p.provincia or p.ciudad or "Desconocida"
            by_region[r] = by_region.get(r, 0) + 1
        return {
            "total": total,
            "scored": scored,
            "by_priority": by_priority,
            "by_sector": by_sector,
            "by_region": by_region,
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
