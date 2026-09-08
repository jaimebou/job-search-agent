# Ofertas revisadas (ledger de búsqueda) — PLANTILLA

> **Este es el fichero plantilla, versionado en el repo.** El cuestionario de `agent-setup/ONBOARDING_QUESTIONNAIRE.md` lo copia a `candidaturas/SCREENED.md` (ignorado por git, solo en tu máquina, sin las filas de ejemplo) la primera vez que lo ejecutas. **No edites este `.template.md` con tus ofertas reales** — edita `SCREENED.md` una vez generado.

Registro de **toda** oferta evaluada en una búsqueda, sea o no candidatura final. Su propósito es que una búsqueda nueva no vuelva a presentar una oferta ya vista — en la misma fuente o en otra distinta. Ver `runbooks/search_jobs.md` para el proceso que rellena esta tabla, y `TRACKING.md` para las que llegaron a candidatura real.

## Cómo deduplicar

- Dentro de una misma fuente: por su **ID nativo** (el Job ID numérico de LinkedIn, el ID de la URL de InfoJobs, el `jk=` de Indeed) — nunca por la URL completa, que suele llevar parámetros de tracking distintos cada vez para la misma oferta.
- **Entre fuentes distintas**: la misma vacante real a menudo aparece en LinkedIn, InfoJobs e Indeed a la vez, o en LinkedIn + la web propia de la empresa. Antes de dar por "nueva" una oferta, compara también contra la columna **URL de aplicación real** (el ATS final al que redirige) de las filas ya existentes. Si coincide, es la misma oferta vista desde otro sitio: añade la fuente nueva en la misma fila (no crear fila duplicada) y anótalo.

| Fecha revisión | Fuente | ID nativo | URL de aplicación real | Puesto | Empresa | Resultado | Motivo |
|---|---|---|---|---|---|---|---|
| 2026-01-10 | LinkedIn | 0000000000 | careers.acmecorp-ejemplo.com/jobs/senior-data-analyst | Senior Data Analyst | Acme Corp (EJEMPLO) | Encaja → Aplicada | Sector tecnología, grande, no consultora, híbrido 40% presencial |
| 2026-01-10 | LinkedIn | 1111111111 | — | Data Analyst Junior | Otra Empresa (EJEMPLO) | Descartada | Seniority junior, no encaja con el objetivo Senior |
