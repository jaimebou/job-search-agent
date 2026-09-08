# Agente de búsqueda de empleo — paquete de instalación

Un agente que corre dentro de **Claude Code** y te acompaña en todo el proceso de búsqueda de empleo: busca ofertas en LinkedIn/InfoJobs/Indeed filtradas por tus criterios, adapta tu CV oferta por oferta, rellena y envía candidaturas (una a una o en lote), sube todo a tu Google Drive personal (opcional), y hace seguimiento de tus candidaturas por email.

No es una idea teórica: es la extracción de un flujo que llevamos usando y depurando semanas — búsquedas reales, decenas de candidaturas aplicadas, patrones de formularios de ATS ya mapeados (Greenhouse, Ashby, Teamtailor, SuccessFactors, TalentClue, Viterbit...). Sin ninguno de mis datos personales, listo para que configures el tuyo.

## Qué incluye

`agent-setup/` guarda solo lo que se consume **una vez**, al instalar. Todo lo demás es de uso recurrente (cada sesión de búsqueda/aplicación) y vive en la raíz.

| Carpeta/fichero | Qué es |
|---|---|
| [`agent-setup/SETUP.md`](agent-setup/SETUP.md) | Instalación técnica: Claude Code, Playwright, tu propio Google Drive (OAuth, opcional), login en los portales de empleo. **Empieza por aquí.** |
| [`agent-setup/ONBOARDING_QUESTIONNAIRE.md`](agent-setup/ONBOARDING_QUESTIONNAIRE.md) | El cuestionario que tu Claude te hace para construir tu `JOB_SEARCH_CRITERIA.md` (sector, rol, salario, empresas a excluir...). |
| [`agent-setup/JOB_SEARCH_CRITERIA.template.md`](agent-setup/JOB_SEARCH_CRITERIA.template.md) | Ejemplo de criterios ya rellenos (con un perfil ficticio) para que veas el formato antes de generar el tuyo. |
| [`runbooks/start_job_agent.md`](runbooks/start_job_agent.md) | El prompt que activa el agente. Este es el fichero que le pegas a tu Claude para arrancar una sesión — se usa en cada sesión, no solo al instalar. |
| [`runbooks/search_jobs.md`](runbooks/search_jobs.md) | Cómo busca y filtra ofertas en LinkedIn/InfoJobs/Indeed. |
| [`runbooks/apply_external_job.md`](runbooks/apply_external_job.md) | Cómo aplica a una oferta concreta, de principio a fin. |
| [`runbooks/apply_batch_jobs.md`](runbooks/apply_batch_jobs.md) | Cómo aplica a varias ofertas a la vez, en paralelo. |
| [`runbooks/check_status.md`](runbooks/check_status.md) | Cómo revisa el estado de tus candidaturas ya enviadas (vía email). |
| `candidaturas/TRACKING.md`, `SCREENED.md` | Tu log de candidaturas y el ledger de ofertas ya vistas — se van rellenando sesión a sesión (plantillas vacías con una fila de ejemplo ficticia). |
| `candidaturas/2026-01-EJEMPLO/AcmeCorp/` | Ejemplo de cómo queda la carpeta de una candidatura concreta. |
| `cv/EJEMPLO_CV.md` | CV de ejemplo (persona ficticia) en el formato que usa el agente para adaptar tu CV a cada oferta. |
| `scripts/` | Scripts Python para convertir CV Markdown↔PDF y subir ficheros a Google Drive. |
| `CHANGELOG.md` | Versionado de este paquete. |

**Lo que este paquete NO incluye, a propósito:** ninguna credencial, cookie de sesión, dato personal, candidatura real ni CV real mío. Cada persona autentica sus propias cuentas (LinkedIn, InfoJobs, Indeed, Google) en su propio navegador, y crea su propio proyecto de Google Cloud si quiere el envío automático a Drive. Ver "Nota de seguridad" en `agent-setup/SETUP.md`.

## Quickstart

1. Clona este repo.
2. Lee y ejecuta [`agent-setup/SETUP.md`](agent-setup/SETUP.md) de principio a fin (una sola vez). Los comandos de ese documento son relativos a la raíz del repo, no a `agent-setup/`.
3. Abre una conversación con Claude Code **en la raíz del repo** y pégale exactamente esto:
   ```
   Lee y sigue @agent-setup/SETUP.md, y cuando termine la instalación técnica ejecuta el cuestionario de @agent-setup/ONBOARDING_QUESTIONNAIRE.md para configurar mis criterios de búsqueda.
   ```
4. Al terminar el cuestionario, tendrás tu propio `JOB_SEARCH_CRITERIA.md` en la raíz del repo (no en `agent-setup/`). A partir de ahí, el agente se activa siempre con `runbooks/start_job_agent.md` — ver el propio fichero para los 4 modos (búsqueda, aplicación, aplicación en lote, seguimiento).

## Por qué es "susceptible a mejora"

Este repo vive en GitHub para eso: mejoras futuras en el motor (nuevos patrones de ATS, ajustes a un runbook, nuevas fuentes de búsqueda) se comparten con un simple `git pull`. Cualquier persona que use este paquete puede además evolucionar sus propios runbooks locales igual que hicimos nosotros: si el agente comete un error o hay un paso que falta, se corrige el runbook en el momento, no se reintenta ciegamente la próxima vez — y si el cambio es de interés general, un PR a este repo lo comparte con todo el mundo que lo use.

### Cómo contribuir

Este es un repo privado de cuenta personal gratuita, así que GitHub no permite forzar la protección de la rama `main` (esa función requiere GitHub Pro o repo público). Por convención, no por imposición técnica:

- **No empujes directo a `main`.** Crea una rama y abre un Pull Request.
- El propietario del repo revisa y mergea. Si algo es urgente, avisa aparte.

## Fuera de alcance (por ahora)

- Monitorización autónoma/periódica — el agente no busca ni revisa el email por su cuenta sin que se lo pidas en cada sesión.
- Scoring numérico de ofertas — la clasificación es cualitativa (Encaja/Dudosa/Descartada).
- Multi-idioma / mercados fuera de España — los runbooks de InfoJobs e Indeed asumen España; LinkedIn es más portable pero no se ha probado fuera de este mercado.
