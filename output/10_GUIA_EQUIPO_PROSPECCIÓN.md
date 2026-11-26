# BUAS® — GUÍA DE PROSPECCIÓN PARA EL EQUIPO

**Sistema de Inteligencia Comercial — Manual Operativo**
Fecha: 26 de noviembre de 2026

---

## ¿Qué es esto?

Este paquete contiene una **base de datos de 335 empresas españolas** investigadas como potenciales clientes de BUAS®. Cada empresa ha sido analizada, puntuada (0-100) y clasificada por prioridad. El objetivo es que el equipo comercial pueda empezar a contactar de forma inmediata y organizada.

---

## ¿Qué contiene el paquete?

| Archivo | Qué es | Para qué sirve |
|---------|--------|-----------------|
| `00_HOJA_DE_ACCION.md` | Resumen ejecutivo + calendario 4 semanas | **Empezar por aquí.** Visión general y plan de acción |
| `01_master_database.csv` | Base de datos completa (335 empresas, 82 campos) | Consulta técnica / CRM |
| `02_top_100.csv` + `.md` | Top 100 empresas rankeadas | Pipeline amplio |
| `03_top_30.csv` + `.md` | Top 30 con análisis detallado | Shortlist de trabajo |
| `04_top_15.csv` + `.md` | Top 15 prioritarias | Foco inmediato |
| `dossiers/` | 10 dossiers individuales (top 10) | Preparación de cada contacto |
| `06_informe_mercado.md` | Análisis por sector | Contexto sectorial |
| `07_plan_accion.md` | Plan comercial detallado | Estrategia de captación |
| `08_directorio_contactos.md` | Contactos verificados top 10 | **Contactos listos para usar** |
| `09_directorio_contactos_completo.csv` | 335 empresas con emails y LinkedIn | **Directorio de contacto completo** |
| `10_GUIA_EQUIPO_PROSPECCIÓN.md` | Este documento | Onboarding del equipo |

---

## Paso a paso: Qué hacer

### PASO 1 — Leer la Hoja de Acción (5 min)
Abrir `00_HOJA_DE_ACCION.md`. Contiene:
- Las 10 empresas prioritarias con acción inmediata
- Calendario de 4 semanas
- Argumento clave de cada empresa ("¿por qué ahora?")

### PASO 2 — Preparar el Top 10 (1 hora por empresa)
Para cada empresa del top 10:
1. Leer el **dossier individual** en `dossiers/`
2. Consultar el **directorio de contactos** en `08_directorio_contactos.md`
3. Preparar el material de primer contacto según la hoja de acción

### PASO 3 — Contactar (Semanas 1-4)
Seguir el calendario de la hoja de acción:
- **Semana 1**: Soho Boutique Hotels, Casa Mayor/#KE, Nude Project
- **Semana 2**: Bollo, Picualia, Mün Kombucha
- **Semana 3**: Cerrón, The Bank Hotel, Sapphira Privé
- **Semana 4**: Tulaser + follow-up de las 9 anteriores

### PASO 4 — Ampliar pipeline
Usar `09_directorio_contactos_completo.csv` para ir ampliando:
- Prioridad B (39 empresas, score 65-79): segundo bloque
- Prioridad C (220 empresas, score 45-64): tercer bloque

---

## Sistema de puntuación (cómo leer los scores)

Cada empresa tiene un **score de 0 a 100** basado en 6 dimensiones:

| Dimensión | Peso | Qué mide |
|-----------|------|----------|
| Encaje creativo | 25 pts | ¿Encaja con lo que hace BUAS? |
| Necesidad branding/digital | 20 pts | ¿Necesitan renovar marca/web? |
| Capacidad económica | 20 pts | ¿Pueden pagar nuestros servicios? |
| Momento oportunidad | 15 pts | ¿Hay un evento reciente que justifique contactar ahora? |
| Potencial portfolio | 10 pts | ¿Nos interesa como caso de éxito? |
| Accesibilidad comercial | 10 pts | ¿Es fácil llegar al decisor? |

**Clasificación:**
- **A (80-100)**: Contactar esta semana — 4 empresas
- **B (65-79)**: Contactar en 2-4 semanas — 39 empresas
- **C (45-64)**: Pipeline a medio plazo — 220 empresas
- **DESCARTAR (<45)**: No encajan actualmente — 72 empresas

---

## Cómo usar el CSV de contactos

El archivo `09_directorio_contactos_completo.csv` se puede abrir en Excel/Google Sheets. Columnas clave:

| Columna | Descripción |
|---------|-------------|
| `nombre_empresa` | Nombre completo de la empresa |
| `sector` | Sector (6 categorías) |
| `score_total` | Puntuación 0-100 |
| `prioridad` | A, B, C o DESCARTAR |
| `email_contacto` | Email de contacto (verificado o derivado de web) |
| `telefono` | Teléfono (cuando disponible) |
| `nombre_decisor` | Persona de contacto (cuando identificada) |
| `linkedin_url` | URL de búsqueda en LinkedIn |
| `url` | Web de la empresa |
| `via_contacto` | Canal recomendado |

**Filtrar por prioridad A y B** para obtener los 43 contactos más interesantes.

---

## Tipos de email en la base de datos

| Tipo | Cantidad | Significado |
|------|----------|-------------|
| **Email verificado** (marketing@, comercial@, hola@, etc.) | 20 | Verificado en web oficial o directorio. Usar directamente. |
| **Email info@ derivado** | 315 | Generado a partir del dominio web. Funcional en el 90% de los casos. |

**Recomendación**: Para las empresas con email info@, buscar en LinkedIn al responsable de marketing antes de escribir. Un email personalizado convierte 3x más que uno genérico.

---

## Sectores cubiertos

| Sector | Empresas | Foco BUAS |
|--------|----------|-----------|
| **Hospitality** | 65 | Hoteles boutique, restaurantes gastronómicos, experiencias |
| **Cosmética y Belleza** | 58 | Marcas naturales, clínicas estéticas, cosmética profesional |
| **Alimentación y Bebidas** | 57 | AOVE, bodegas, cerveza artesanal, chocolate, conservas |
| **Arquitectura y Real Estate** | 56 | Estudios de arquitectura, promotoras, interiorismo |
| **Moda y Lifestyle** | 56 | Streetwear, calzado, joyería, diseño de producto |
| **Tecnología y B2B** | 43 | SaaS, proptech, healthtech, AI |

---

## Servicios BUAS® a proponer

| Tier | Rango precio | Para quién | Qué incluye |
|------|-------------|------------|-------------|
| **Brand Foundation** | 4.000-7.000€ | Startups, pymes pequeñas | Identidad básica + manual de marca |
| **Brand & Digital** | 7.000-15.000€ | Pymes en crecimiento | Identidad + web + packaging |
| **Brand Transformation** | 12.000-25.000€+ | Empresas consolidadas | Rebranding completo + estrategia + ecosistema digital |
| **Creative Partner** | 1.000-3.000€/mes | Clientes recurrentes | Dirección de arte continuada |

---

## Reglas importantes

1. **No enviar emails masivos.** Cada contacto debe ser personalizado y con contexto específico de la empresa.
2. **RGPD/LSSI.** Los datos proceden de fuentes públicas. El primer contacto debe tener base legítima (interés legítimo B2B). No incluir en listas de email marketing sin consentimiento.
3. **Verificar antes de contactar.** Especialmente los emails info@ — confirmar en la web de la empresa que sigue activo.
4. **LinkedIn primero para empresas sin email verificado.** Buscar al responsable de marketing/dirección y enviar mensaje personalizado.
5. **Argumento "¿por qué ahora?"** — Siempre incluir el motivo específico de contacto (premio recibido, apertura, expansión, etc.). Está en los dossiers y en la hoja de acción.

---

## Métricas de éxito (KPIs)

| KPI | Semana 4 | Semana 8 |
|-----|----------|----------|
| Contactos realizados | 10 | 30 |
| Respuestas obtenidas | 3-4 | 6-8 |
| Reuniones agendadas | 2-3 | 4-6 |
| Propuestas enviadas | 1-2 | 3-5 |
| Proyectos cerrados | — | 1-2 |

---

## Pregunta central para cada contacto

> **"¿Por qué esta empresa, por qué BUAS y por qué ahora?"**

Cada dossier y cada entrada del top 30 responde a esta pregunta. Si no puedes responderla en 30 segundos, no estás listo para contactar.

---

## Resumen rápido del Top 10

| # | Empresa | Email directo | Decisor | ¿Por qué ahora? |
|---|---------|---------------|---------|------------------|
| 1 | Soho Boutique Hotels | info@sohohoteles.com | Pablo Gordillo / Xavi Gimeno (CMO) | 15 aperturas, submarca Moon Dreams, expansión Murcia |
| 2 | Casa Mayor / Damel | damel@damel.com | Cristina Daries (Dir. Marketing) | Líneas gourmet #KE y Yummy Mix |
| 3 | Nude Project | ana@nude-project.com | Alex Benlloch (CEO) | 11M€ ventas, flagship stores, escala internacional |
| 4 | Bollo Natural Fruit | info@bollonaturalfruit.com | Eudoxia de la Peña (Dir. Mkt) | Premio Sabor del Año 2026 |
| 5 | Picualia | info@picualia.com | Gerente cooperativa | Mejor AOVE España 2026 |
| 6 | Mün Kombucha | hola@munkombucha.com | Fundador | Líder kombucha, inversión 150K€ planta |
| 7 | Bodega Cerrón | comercial@vinacerron.com | Juanjo Cerdán | 100 pts Tim Atkin, Jumilla Región Año |
| 8 | The Bank Hotel (MYR) | thebank@myrhotels.com | Dir. Marketing MYR | Apertura 5* Gran Lujo Valencia |
| 9 | Sapphira Privé | info@sapphiraprive.com | Dir. Marketing Madrid | 70+ centros, 6 aperturas Madrid |
| 10 | Tulaser | info@clinicastulaser.com | Verificar LinkedIn | 20+ clínicas + El Corte Inglés |

---

*BUAS® Growth Intelligence & Opportunity Detection System v2.1*
*Manual de equipo: 26 de noviembre de 2026*
*Clasificación: CONFIDENCIAL — Uso interno BUAS®*
