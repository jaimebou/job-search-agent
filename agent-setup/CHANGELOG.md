# Changelog

Versionado del paquete "agente de búsqueda de empleo". No confundir con `candidaturas/TRACKING.md` (eso es tu log personal de candidaturas, no de este paquete).

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
