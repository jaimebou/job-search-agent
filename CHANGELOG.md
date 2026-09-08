# Changelog

Versionado del paquete "agente de búsqueda de empleo". No confundir con `candidaturas/TRACKING.md` (eso es tu log personal de candidaturas, no de este paquete).

## v0.1.1 — 2026-09-08

Correcciones tras la primera revisión del paquete, antes del primer uso real:

- `agent-setup/SETUP.md` — pasos concretos y validados para instalar el MCP de Playwright (antes asumía que ya estaba configurado). Google Drive marcado explícitamente como **opcional**, aclarando que solo lo usa `scripts/upload_to_drive.py` (no hay MCP de Drive en este paquete).
- Reorganización de carpetas: `agent-setup/` ahora contiene solo lo que se consume **una vez** (`SETUP.md`, `ONBOARDING_QUESTIONNAIRE.md`, `JOB_SEARCH_CRITERIA.template.md`). `runbooks/`, `scripts/`, `candidaturas/` y `cv/` — de uso recurrente en cada sesión — viven en la raíz del repo.
- `agent-setup/ONBOARDING_QUESTIONNAIRE.md` § "Antes de preguntar nada" — el paso de importar el CV ahora incluye reestructurarlo al formato de las plantillas (referencia `cv/EJEMPLO_CV.md`), elegir tema (`harvard` por defecto o `cv`) y renderizarlo a PDF para validación, no solo la extracción en bruto del PDF (antes ese paso se quedaba corto).

## v0.1.0 — 2026-09-08

Primera versión exportada, extraída del uso real de un agente personal equivalente durante agosto-septiembre 2026 (más de 20 candidaturas reales aplicadas, 3 fuentes de búsqueda, aplicación en lote validada con 6 candidaturas en paralelo).

- `runbooks/search_jobs.md` — búsqueda y screening en LinkedIn (verificado en producción), InfoJobs e Indeed (mecánica documentada, pendiente de primer uso real — ver nota al final del runbook).
- `runbooks/apply_external_job.md` — aplicación individual a ATS externos, con metodología de adaptación de CV en dos pasadas (gap analysis obligatorio).
- `runbooks/apply_batch_jobs.md` — aplicación en lote (2+ ofertas en paralelo), con tabla de patrones conocidos de 6 ATS (Greenhouse, Ashby, Teamtailor, TalentClue, SuccessFactors, Viterbit).
- `runbooks/check_status.md` — seguimiento manual de candidaturas vía email.
- `ONBOARDING_QUESTIONNAIRE.md` — cuestionario inicial de configuración de criterios (nuevo en esta versión, no existía en el agente original — se construyó específicamente para este paquete).
- Scripts de conversión CV Markdown↔PDF (temas `harvard`, `cv`, `letter`) y subida a Google Drive vía OAuth propio.

### Pendiente para próximas versiones

- Verificar en vivo las secciones de InfoJobs e Indeed en `search_jobs.md` (selectores y parámetros de URL) y actualizar con los datos reales.
- Evaluar si tiene sentido un scoring numérico de ofertas si el volumen por búsqueda crece mucho.
- Decidir si este paquete pasa a vivir en un repositorio Git personal (no en infraestructura corporativa) para versionado real entre instalaciones.
