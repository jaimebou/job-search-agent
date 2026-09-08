# Agente de búsqueda de empleo — paquete de instalación

Un agente que corre dentro de **Claude Code** y te acompaña en todo el proceso de búsqueda de empleo: busca ofertas en LinkedIn/InfoJobs/Indeed filtradas por tus criterios, adapta tu CV oferta por oferta, rellena y envía candidaturas (una a una o en lote), sube todo a tu Google Drive personal, y hace seguimiento de tus candidaturas por email.

No es una idea teórica: es la extracción de un flujo que llevamos usando y depurando semanas — búsquedas reales, decenas de candidaturas aplicadas, patrones de formularios de ATS ya mapeados (Greenhouse, Ashby, Teamtailor, SuccessFactors, TalentClue, Viterbit...). Este paquete es ese motor, sin ninguno de mis datos personales, listo para que configures el tuyo.

## Qué incluye

| Carpeta/fichero | Qué es |
|---|---|
| `SETUP.md` | Instalación técnica: Claude Code, Playwright, tu propio Google Drive (OAuth), login en los portales de empleo. **Empieza por aquí.** |
| `ONBOARDING_QUESTIONNAIRE.md` | El cuestionario que tu Claude te hace para construir tu `JOB_SEARCH_CRITERIA.md` (sector, rol, salario, empresas a excluir...). |
| `JOB_SEARCH_CRITERIA.template.md` | Ejemplo de criterios ya rellenos (con un perfil ficticio) para que veas el formato antes de generar el tuyo. |
| `runbooks/start_job_agent.md` | El prompt que activa el agente. Este es el fichero que le pegas a tu Claude para arrancar una sesión. |
| `runbooks/search_jobs.md` | Cómo busca y filtra ofertas en LinkedIn/InfoJobs/Indeed. |
| `runbooks/apply_external_job.md` | Cómo aplica a una oferta concreta, de principio a fin. |
| `runbooks/apply_batch_jobs.md` | Cómo aplica a varias ofertas a la vez, en paralelo. |
| `runbooks/check_status.md` | Cómo revisa el estado de tus candidaturas ya enviadas (vía email). |
| `candidaturas/TRACKING.md`, `candidaturas/SCREENED.md` | Plantillas vacías (con una fila de ejemplo ficticia) del log de candidaturas y del ledger de ofertas ya vistas. |
| `candidaturas/2026-01-EJEMPLO/AcmeCorp/` | Ejemplo de cómo queda la carpeta de una candidatura concreta. |
| `cv/EJEMPLO_CV.md` | CV de ejemplo (persona ficticia) en el formato que usa el agente para adaptar tu CV a cada oferta. |
| `scripts/` | Scripts Python para convertir CV Markdown↔PDF y subir ficheros a Google Drive. |

**Lo que este paquete NO incluye, a propósito:** ninguna credencial, cookie de sesión, dato personal, candidatura real ni CV real mío. Cada persona autentica sus propias cuentas (LinkedIn, InfoJobs, Indeed, Google) en su propio navegador, y crea su propio proyecto de Google Cloud para el acceso a Drive. Ver "Nota de seguridad" en `SETUP.md`.

## Quickstart

1. Lee y ejecuta `SETUP.md` de principio a fin (una sola vez).
2. Abre una conversación con Claude Code en esta carpeta y pégale exactamente esto:
   ```
   Lee y sigue @job-search-agent/SETUP.md, y cuando termine la instalación técnica ejecuta el cuestionario de @job-search-agent/ONBOARDING_QUESTIONNAIRE.md para configurar mis criterios de búsqueda.
   ```
3. Al terminar el cuestionario, tendrás tu propio `JOB_SEARCH_CRITERIA.md` en la raíz de esta carpeta. A partir de ahí, el agente se activa siempre con `runbooks/start_job_agent.md` — ver el propio fichero para los 4 modos (búsqueda, aplicación, aplicación en lote, seguimiento).

## Por qué es "susceptible a mejora"

Esta carpeta está pensada para vivir en un repositorio Git propio más adelante (tiene ya `.gitignore` y `CHANGELOG.md`). Por ahora es una copia exportada a fecha de hoy — mejoras futuras en el motor (nuevos patrones de ATS, ajustes a un runbook, nuevas fuentes de búsqueda) se comparten reexportando o, si migramos a un repo Git compartido, con un simple `git pull`. Cualquier persona que use este paquete puede además evolucionar sus propios runbooks locales igual que hicimos nosotros: si el agente comete un error o hay un paso que falta, se corrige el runbook en el momento, no se reintenta ciegamente la próxima vez.

## Fuera de alcance (por ahora)

- Monitorización autónoma/periódica — el agente no busca ni revisa el email por su cuenta sin que se lo pidas en cada sesión.
- Scoring numérico de ofertas — la clasificación es cualitativa (Encaja/Dudosa/Descartada).
- Multi-idioma / mercados fuera de España — los runbooks de InfoJobs e Indeed asumen España; LinkedIn es más portable pero no se ha probado fuera de este mercado.
