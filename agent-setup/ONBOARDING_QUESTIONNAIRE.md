# Runbook — Cuestionario de configuración inicial

Esto es un runbook para el agente (Claude), no un formulario para rellenar a mano. Se ejecuta **una sola vez**, al instalar el paquete (o cuando quieras revisar tus criterios a fondo). Al terminar, genera `JOB_SEARCH_CRITERIA.md` en la **raíz del repo** (no dentro de `agent-setup/` — ahí solo viven los documentos de instalación), con la misma estructura que `JOB_SEARCH_CRITERIA.template.md` — revisa ese fichero antes de empezar para conocer el formato de destino.

> **Rutas de este documento** (`scripts/...`, `cv/...`, `candidaturas/...`, `runbooks/...`) son relativas a la raíz del repo, no a esta carpeta `agent-setup/`.

No sustituye la flexibilidad del agente real: estos criterios son el punto de partida, no reglas rígidas — igual que en `JOB_SEARCH_CRITERIA.template.md`, el agente debe seguir tratando lo ambiguo como "Dudosa, a confirmar" en vez de descartar en silencio.

## Antes de preguntar nada

1. Comprueba si ya existe `JOB_SEARCH_CRITERIA.md` en la raíz del repo. Si existe, pregunta primero si quiere **rehacerlo desde cero** o **revisar/editar secciones concretas** — no lo sobrescribas sin confirmación.
2. Pide el CV actual de la persona (ruta a un PDF o Markdown, o que lo pegue). Conviértelo a Markdown si hace falta (`scripts/pdf_to_md.py`) y guárdalo en `cv/` con el nombre que prefiera (ej. `cv/CV_<MMAAAA>.md`). Este CV es la base para inferir funciones núcleo y stack técnico en la sección de Rol — no lo inventes ni lo completes sin leerlo.

## Ronda 1 — Datos de contacto y ubicación (AskUserQuestion, 1 llamada)

Pregunta, en una sola tanda:
- Nombre completo (para nombrar ficheros de CV/carta y rellenar formularios).
- Email personal y teléfono (para autofill de formularios — nunca el corporativo).
- URL de tu perfil de LinkedIn.
- Ciudad/zona donde buscas trabajo.

## Ronda 2 — Modalidad y fuentes (AskUserQuestion, 1 llamada, máx. 4 preguntas)

- Modalidad aceptada: presencial / híbrido con mínimo de teletrabajo (pide el % o los días concretos) / remoto total / cualquiera de las anteriores.
- Fuentes a usar: LinkedIn (asumido salvo que diga lo contrario) + ¿tiene cuenta en InfoJobs? ¿en Indeed? (multiSelect).
- Salario mínimo aceptable, y salario preferido (dos cifras o una franja).

## Ronda 3 — Sector y tamaño de empresa (AskUserQuestion, 1 llamada)

- Sectores de interés (multiSelect, con opción "cualquiera/sin preferencia") — ofrece ejemplos genéricos (energía, movilidad, salud, retail, banca/finanzas, industrial, telecomunicaciones, tecnología/SaaS...) más una opción abierta.
- Tamaño de empresa preferido: startup / scaleup financiada / mediana / grande / sin preferencia. Si excluye startups, pregunta si hay una excepción tipo "scaleup grande y bien financiada" (como hicimos nosotros — ver `JOB_SEARCH_CRITERIA.template.md` § Sector y tamaño).
- **Empresas concretas a excluir** (blacklist) — pregunta explícitamente si hay empresas donde no quiere trabajar (ex-empleador con mal recuerdo, competencia directa de su empleador actual, lo que sea) y por qué, para poder aplicar el filtro sin tener que volver a preguntar cada vez.
- **Empresas concretas a vigilar de forma recurrente** (opcional) — si hay una empresa que le interesa especialmente (cercanía geográfica, marca, etc.), para revisarla en cada ronda de búsqueda aunque no lo pida explícitamente.

## Ronda 4 — Consultoras (AskUserQuestion, 1 llamada)

- ¿Descartar consultoras/staffing por defecto? (sí, recomendado, salvo que busque específicamente ese tipo de puesto).
- Si sí: ¿conoce ya alguna consultora "buena" que quiera dejar como excepción (proyecto estable con cliente final, no rotación pura)? Explica la distinción (ver plantilla) para que pueda decidir con criterio, no solo por nombre.

## Ronda 5 — Rol y funciones núcleo (AskUserQuestion + lectura del CV)

1. Antes de preguntar, lee el CV ya guardado y propón un borrador de "funciones núcleo" y "funciones que suman" basado en su experiencia real (no inventes herramientas que no aparezcan en el CV).
2. Pregunta (1 llamada AskUserQuestion):
   - Título(s) de puesto objetivo (uno o varios — ej. "Data Analyst", "Analytics Engineer", "Business Analyst"...).
   - ¿Confirma el borrador de funciones núcleo que propusiste, o quiere corregirlo?
   - Roles que quiere excluir explícitamente aunque el título coincida (ej. "aunque diga Data Analyst, si es realmente un rol de ventas/ingeniería de software/etc., descartar").
   - Seniority objetivo (junior/mid/senior/lead, o rango de años de experiencia).

## Cierre — generar los ficheros

1. Escribe `JOB_SEARCH_CRITERIA.md` en la raíz del repo, con la misma estructura de secciones que `JOB_SEARCH_CRITERIA.template.md` (Ubicación y modalidad, Sector y tamaño de empresa, Consultoras, Rol, Salario, Empresas a excluir, Empresas a vigilar, Dimensiones de búsqueda, Cómo aplico estos criterios), usando las respuestas de las 5 rondas. Añade la fecha de hoy como "última actualización".
2. Vacía (o crea si no existen) `candidaturas/TRACKING.md` y `candidaturas/SCREENED.md` a partir de las plantillas ya presentes en `candidaturas/` — quita la fila de ejemplo ficticia antes de dejarlo listo para uso real.
3. Confirma con un resumen breve de lo configurado, y recuérdale que puede pedir "revisa mis criterios" en cualquier momento para reabrir este cuestionario en modo edición.
4. Indícale explícitamente que ya puede activar el agente con `runbooks/start_job_agent.md`.
