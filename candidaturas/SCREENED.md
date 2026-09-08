# Ofertas revisadas (ledger de búsqueda)

Registro de **toda** oferta evaluada en una búsqueda, sea o no candidatura final. Su propósito es que una búsqueda nueva no vuelva a presentar una oferta ya vista — en la misma fuente o en otra distinta. Ver `runbooks/search_jobs.md` para el proceso que rellena esta tabla, y `TRACKING.md` para las que llegaron a candidatura real.

> **Filas de ejemplo (ficticias) más abajo** — bórralas antes de tu primer uso real. El cuestionario de onboarding también las borra si generas este fichero desde ahí.

## Cómo deduplicar

- Dentro de una misma fuente: por su **ID nativo** (el Job ID numérico de LinkedIn, el ID de la URL de InfoJobs, el `jk=` de Indeed) — nunca por la URL completa, que suele llevar parámetros de tracking distintos cada vez para la misma oferta.
- **Entre fuentes distintas**: la misma vacante real a menudo aparece en LinkedIn, InfoJobs e Indeed a la vez, o en LinkedIn + la web propia de la empresa. Antes de dar por "nueva" una oferta, compara también contra la columna **URL de aplicación real** (el ATS final al que redirige) de las filas ya existentes. Si coincide, es la misma oferta vista desde otro sitio: añade la fuente nueva en la misma fila (no crear fila duplicada) y anótalo.

| Fecha revisión | Fuente | ID nativo | URL de aplicación real | Puesto | Empresa | Resultado | Motivo |
|---|---|---|---|---|---|---|---|
| 2026-01-10 | LinkedIn | 0000000000 | careers.acmecorp-ejemplo.com/jobs/senior-data-analyst | Senior Data Analyst | Acme Corp (EJEMPLO) | Encaja → Aplicada | Sector tecnología, grande, no consultora, híbrido 40% presencial |
| 2026-01-10 | LinkedIn | 1111111111 | — | Data Analyst Junior | Otra Empresa (EJEMPLO) | Descartada | Seniority junior, no encaja con el objetivo Senior |
