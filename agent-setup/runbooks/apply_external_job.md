# Runbook — Aplicar a una candidatura fuera de LinkedIn (ATS externo)

La mayoría de las ofertas en LinkedIn no se solicitan con "Solicitud sencilla" (Easy Apply) — redirigen a la web propia de la empresa (Teamtailor, Greenhouse, Workday, SAP SuccessFactors, etc.), con su propio formulario y preguntas de cribado. Este runbook documenta el proceso punta a punta, validado en producción en el agente original (decenas de candidaturas reales, agosto-septiembre 2026).

Ver también: `JOB_SEARCH_CRITERIA.md` (criterios de qué ofertas perseguir) y `candidaturas/TRACKING.md` (log de candidaturas).

## 0. Verificación de sesión (antes de tocar nada)

- Confirma que la sesión de LinkedIn activa en el navegador es la **personal**, no ninguna cuenta de trabajo.
- Confirma que la sesión de Google activa es tu cuenta **personal**, no una SSO corporativa. Verifica vía el botón de cuenta en la esquina superior derecha (`drive.google.com` → "Cuenta de Google: ...").
- Motivo: esta gestión usa Drive/Gmail personales para currículums y candidaturas; mezclar sesiones puede filtrar datos personales a herramientas de trabajo o viceversa.

**Aviso importante:** LinkedIn, Indeed e InfoJobs prohíben la automatización en sus Términos de Servicio — riesgo real de bloqueo de cuenta si se abusa. Por eso el agente nunca auto-envía en bucle ni actúa sin supervisión: cada acción de navegación debe ser deliberada (no scraping masivo agresivo, no reintentos automáticos sin pausa), y el envío final de cada candidatura requiere confirmación explícita, sin excepción.

## 1. Screening inicial contra los criterios de búsqueda

Antes de mover un dedo en el formulario, contrasta la oferta contra `JOB_SEARCH_CRITERIA.md`:
- Modalidad (según tu mínimo de teletrabajo/remoto)
- Sector / tamaño de empresa
- ¿Es consultora? (salvo excepción explícita)
- ¿Está en tu lista de empresas a excluir?
- Rol / seniority
- Salario (si está visible, contra tu mínimo)

Si algo no cumple o es dudoso, comunícalo explícitamente en vez de asumir. Solo se avanza al paso 2 con luz verde (explícita o porque encaja claramente con los criterios).

## 2. Leer la oferta completa

Extrae con `browser_evaluate` el texto completo de "Acerca del empleo" (más eficiente en tokens que un snapshot completo). Identifica: responsabilidades, requisitos, beneficios, y sobre todo el % de teletrabajo si no estaba en el resumen.

## 3. Identificar el mecanismo de aplicación

En la página de LinkedIn, busca el botón de aplicar:
- **"Solicitud sencilla"** → Easy Apply, todo dentro de LinkedIn, mucho más simple (formulario corto, a veces sin preguntas de cribado).
- **"Solicitar en el sitio web de la empresa"** + *"Respuestas gestionadas fuera de LinkedIn"* → redirige a un ATS externo. Al pulsar, LinkedIn muestra un interstitial ("Vas a salir de LinkedIn... Continuar") con la URL real de destino (`careers.<empresa>.com/...`). Síguelo.

Este runbook cubre el segundo caso.

## 4. Cruzar la oferta con el CV general

Lee tu CV general más reciente (`cv/CV_<MMAAAA>.md`) y compáralo con los requisitos de la oferta. Identifica qué bullets/orden hay que resaltar y si falta algo. Si hay un excompañero con rol equivalente en LinkedIn, su perfil puede ser fuente legítima para inspirar bullets — siempre reescritos, nunca copiados literalmente.

## 5. Crear la carpeta de la candidatura

Local: `candidaturas/<AAAA-MM>/<Empresa>/`
Drive: mismo esquema de carpetas dentro de tu carpeta de Drive para candidaturas (definida en `SETUP.md`/`ONBOARDING_QUESTIONNAIRE.md`).

## 6. Adaptar el CV a la oferta — dos pasadas, con gap analysis en medio

Metodología obligatoria (validada en producción): **primera optimización → gap analysis de keywords → segunda optimización**. No es opcional, se hace en cada candidatura.

1. **Primera pasada**: copia el CV general a `candidaturas/<mes>/<Empresa>/CV_<Empresa>_<MMAAAA>.md`. Ajusta resumen y orden de bullets para resaltar lo relevante a esta oferta concreta (sin inventar datos).
2. **Gap analysis (obligatorio, no lo saltes)**: lee el texto completo de la oferta (Job Description + requisitos + "what it takes", sin cortar por longitud) y compáralo contra el CV de la primera pasada. Busca explícitamente: herramientas/tecnologías nombradas que falten, palabras clave de función que el CV describe con otro sinónimo pero no usa literalmente, y términos de sector/rol de la oferta ausentes. Reporta el gap siempre — aunque luego se resuelva sin preguntar nada más.
3. **Segunda pasada — aplicar el gap**: para cada hueco encontrado, dos casos:
   - **Es honesto** (ya se hace eso, solo falta la palabra exacta o un sinónimo más cercano a la oferta): aplícalo directamente, no hace falta preguntar cada vez.
   - **Sería inventar** (tecnología/herramienta no usada realmente): **nunca añadirlo** — consulta si hay duda de si cuenta como invención o no; si es claro que sí, ni se pregunta, se omite y se avisa en el resumen.
- Renderiza a PDF con el script ya existente (no reinventar un pipeline con Playwright/HTML), y vuelve a renderizar tras la segunda pasada:
  ```
  python3 scripts/md_to_pdf.py candidaturas/<mes>/<Empresa>/CV_<Empresa>_<MMAAAA>.md --theme harvard
  ```
  Requiere WeasyPrint + su dependencia nativa `pango` (`brew install pango`, ya cubierto en `SETUP.md`) además de `pip install -r scripts/requirements.txt`. **`harvard` es el tema por defecto para el CV** (serif, conservador, cabe en 2 páginas). Usa `cv` (sans-serif, moderno) solo si el contexto de la empresa lo justifica claramente (ej. startup/tech muy informal), avisando del cambio de tema en vez de decidirlo en silencio. `letter` es solo para la cover letter (ver paso 9).
- Fechas: si falta algún dato (fecha de inicio/fin de un puesto anterior), **pregunta, nunca fabriques**. Anota como placeholder visible si hace falta seguir sin la respuesta.
- Si el CV ya se subió a un formulario externo antes del gap analysis, **vuelve a subir la versión corregida** (no dejar la versión de la primera pasada en el ATS).

## 7. Abrir el formulario externo y mapearlo (sin enviar)

- Extrae todos los campos con `browser_evaluate` (inputs, selects, textareas, radios) para ver required/optional y el texto real de cada pregunta (los radios suelen mostrar solo "Yes"/"No" como label — el texto de la pregunta está en el bloque contenedor, no en el input).
- Separa mentalmente:
  - Campos que se pueden rellenar con datos ya conocidos (nombre, email, teléfono, CV).
  - Preguntas de cribado que **requieren criterio de la persona** (periodo de preaviso, nivel de idioma autoevaluado, expectativas, preguntas sí/no sobre autorización de trabajo o referidos, preguntas abiertas tipo "cuéntanos tu experiencia con X").
- No enviar nada todavía.

## 8. Preguntar lo necesario

Presenta la lista completa de preguntas de cribado (texto literal) y pide las respuestas. Para preguntas abiertas donde se puede aportar una propuesta de texto, redacta un borrador basado en hechos reales verificables, y **confírmalo explícitamente antes de usarlo** (contar caracteres si hay límite).

## 9. Cover letter (si la piden)

Si el formulario tiene un campo de cover letter (obligatorio u opcional), redacta una propuesta breve (3 párrafos: interés + fit con la oferta, experiencia relevante cruzada con la descripción, cierre) y confírmala antes de meterla en el formulario. Guárdala también como fichero aparte en la carpeta de la candidatura:
```
candidaturas/<mes>/<Empresa>/CoverLetter_<Empresa>_<MMAAAA>.md
python3 scripts/md_to_pdf.py <ese_md> --theme letter
```

## 10. Rellenar el formulario

- Texto/radios/checkboxes: vía `browser_evaluate` con `setNativeValue` + eventos `input`/`change`, y `.click()` en los radios correctos (matcheando por texto de la label, no solo por posición).
- Adjuntar CV (y cover letter si aplica): el MCP de Playwright solo acepta rutas dentro de sus "allowed roots" — su propio directorio de salida (revisa la configuración de tu Playwright MCP) y el directorio de trabajo principal de la sesión. Copia el PDF a un directorio scratch permitido (no un repo git) y súbelo con `browser_file_upload`. **No borres la copia hasta confirmar que la candidatura se envió con éxito** (paso 13) — algunos widgets de subida (dropzone/htmx) leen el fichero de forma diferida y no en el momento de seleccionarlo, y borrar la copia demasiado pronto rompe el envío con un error silencioso (`htmx:sendError` / `net::ERR_FILE_NOT_FOUND` en consola, sin mensaje visible en pantalla).
- Antes de pulsar enviar, comprueba si hay un **banner de cookies** superpuesto (típico en ATS que no son LinkedIn) — puede bloquear o interceptar el click sobre el botón de envío sin dar ningún error visible. Ciérralo (aceptar/rechazar, indistinto) antes de intentar enviar.
- Checkboxes de consentimiento: el de privacidad obligatorio se puede marcar como parte de "rellenar el formulario" (es el mínimo para poder enviar una candidatura ya decidida). El de retención de datos para futuras vacantes u otros opcionales **se preguntan explícitamente**, no se asume.

## 11. Verificar todo antes de enviar — pausa obligatoria

Relee del DOM (no de una captura, más fiable) el valor final de cada campo y muéstralo en un resumen claro. **No pulses el botón de enviar sin confirmación explícita en ese momento** — una candidatura enviada no se puede deshacer, y el formulario puede tener preguntas cuya respuesta correcta solo la persona conoce.

## 12. Enviar

Solo tras el "sí, envía" explícito. Click en el botón de envío final.

## 13. Verificar la confirmación

Comprueba la página/URL de destino tras enviar (suele incluir `/thanks/`, `?new_candidate=true` o similar en la URL, y un mensaje tipo "We have received your application"). Si la URL no cambia y no aparece confirmación clara, **no asumas que se envió** — revisa `browser_console_messages` (nivel error) buscando fallos de red o de subida de fichero (ej. `htmx:sendError`, `ERR_FILE_NOT_FOUND`), cierra cualquier banner de cookies que pueda haber interceptado el click, re-adjunta el CV si hiciera falta, y reintenta el envío antes de confirmar nada.

Solo borra la copia temporal del PDF (paso 10) una vez visto el mensaje/URL de confirmación.

## 14. Subir a Drive

Usa el script existente, no subir a mano vía la interfaz de Drive salvo que haga falta crear una carpeta nueva:
```
python3 scripts/upload_to_drive.py <pdf_cv> --folder-path "<tu carpeta de Drive>/candidaturas/<mes>/<Empresa>"
python3 scripts/upload_to_drive.py <pdf_cover_letter> --folder-path "<tu carpeta de Drive>/candidaturas/<mes>/<Empresa>"
```
**Importante:** `--folder-path` necesita que la ruta completa ya exista en Drive — no crea subcarpetas anidadas automáticamente. Si `<mes>` o `<Empresa>` son nuevos, crea esas carpetas una vez a mano en Drive (o con `browser_file_upload`/clicks de Playwright) antes de llamar al script.

## 15. Actualizar el tracking

Añade una fila en `candidaturas/TRACKING.md`: fecha, empresa, puesto, modalidad, salario (si se conoce), estado = "Enviada", enlace a la oferta, carpeta.

## 16. Limpieza

Borra cualquier copia temporal usada para subir ficheros y cualquier captura/snapshot intermedia que no aporte valor de seguir guardando.
