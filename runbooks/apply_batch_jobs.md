# Runbook — Aplicar a varias ofertas en paralelo (lote)

Extiende `apply_external_job.md` para el caso de **2 o más ofertas pendientes de aplicar en la misma sesión** (p. ej. tras una ronda de `search_jobs.md` con varias "Encaja"/"Dudosa" confirmadas, o varios pendientes acumulados de sesiones anteriores). Objetivo: minimizar rondas de preguntas y evitar perder trabajo por errores de navegador, sin saltarse ninguna verificación del runbook base.

Validado en producción en el agente original con un lote real de 6 candidaturas en paralelo.

## Cuándo usar este runbook

Se pide aplicar a varias ofertas a la vez, o algo como "aplica a todas", "tengo N pendientes", "hazlo en paralelo". Si es solo 1 oferta, usa `apply_external_job.md` directamente (más simple).

## Fase 0 — Screening

Ya resuelto antes de llegar aquí: todas las ofertas del lote deben tener luz verde (vía `search_jobs.md` o confirmación explícita oferta por oferta). Este runbook no sustituye el screening, solo la ejecución de la aplicación.

## Fase 1 — Reconocimiento (sin arriesgar nada)

Para cada oferta del lote, en la pestaña de LinkedIn:
1. Si no se ha leído ya, extrae la descripción completa (`browser_evaluate`, no snapshot completo).
2. Busca el botón de aplicar y anota el mecanismo:
   - "Solicitud sencilla" → Easy Apply (poco frecuente para las que llegan a este runbook, normalmente ya se filtran antes).
   - "Solicitar en el sitio web de la empresa" → clica y captura la URL real del interstitial de LinkedIn (`/safety/go/?url=...`) sin necesidad de seguir el redirect todavía.
3. Identifica el ATS por el dominio (`job-boards.eu.greenhouse.io`, `jobs.ashbyhq.com`, `*.teamtailor.com`, `career5.successfactors.eu` / `jobs.<empresa>.com`, `*.talentclue.com`, `careers-*.com` vía Viterbit, etc.) — predice qué tipo de formulario esperar (ver tabla en Fase 3).

No hace falta abrir todos los formularios en esta fase si ya se conoce el patrón del ATS; para los desconocidos, sí conviene abrir y mapear campos antes de pasar a la Fase 2, para saber qué preguntas de cribado habrá que consolidar en la Fase 4.

## Fase 2 — CVs y textos, en bloque

Por cada oferta:
1. Copia el CV general más reciente (`cv/CV_<MMAAAA>.md`) a `candidaturas/<mes>/<Empresa>/CV_<Empresa>_<MMAAAA>.md`.
2. Ajuste ligero, no reescritura: reordena bullets/skills ya existentes para adelantar lo más relevante a esa oferta, con el vocabulario literal de la oferta cuando sea honesto hacerlo.
3. Gap analysis igual de obligatorio que en modo individual: identifica huecos reales (herramienta no usada) y decide CV vs. respuesta abierta según el caso honesto/inventado de siempre — no se relaja por ser un lote.
4. Si hay preguntas abiertas tipo "por qué esta empresa" / "cuál es tu experiencia con..." — redacta un borrador por oferta basado en hechos reales del CV, incluyendo el gap si aplica (no ocultarlo).
5. Renderiza todos los CVs a PDF en un único bucle de shell:
   ```
   for f in candidaturas/<mes>/<Empresa1>/....md candidaturas/<mes>/<Empresa2>/....md ...; do
     python3 scripts/md_to_pdf.py "$f" --theme harvard
   done
   ```

## Fase 3 — Rellenar formularios, una pestaña de navegador por oferta

**Regla crítica de esta fase**: nunca reutilizar la misma pestaña para navegar de una oferta a otra después de haber rellenado un formulario. Un `browser_navigate` sobre una pestaña con un formulario ya relleno **descarta todo lo escrito** (confirmado empíricamente en el agente original: se perdieron varios formularios completos por este motivo antes de corregirlo). En su lugar:

```
Primera oferta:  browser_navigate directamente (pestaña ya abierta)
Resto:           browser_tabs(action: "new", url: "<url externa>")
Volver a una:    browser_tabs(action: "select", index: N)
```

Deja cada formulario relleno y abierto en su pestaña — no los envíes todavía.

Rellena en cada formulario, sin preguntar (datos ya conocidos/estables, de `JOB_SEARCH_CRITERIA.md` § Datos de contacto):
- Nombre, apellidos, email, teléfono, LinkedIn, CV (subida de fichero).
- "¿Cómo nos conociste?" → LinkedIn.
- Checkboxes de consentimiento de privacidad obligatorios (marcar, es requisito mínimo para poder enviar algo que ya se decidió enviar).
- Textos abiertos ya redactados y aprobados en la Fase 4.

### Patrones por ATS observados

| ATS (dominio) | Peculiaridad |
|---|---|
| Greenhouse (`job-boards.*.greenhouse.io`) | Formulario simple, campos con `aria-label` fiable. Combos de país/teléfono son react-select: **hay que clicar la opción del listbox renderizado**, no basta con fijar el `value` del input oculto vía JS — si no, el campo queda "Select..." y falla la validación al enviar. |
| Ashby (`jobs.ashbyhq.com`) | Botones Yes/No en vez de checkboxes/radio para preguntas de sí/no (right to work, fluidez de idioma) — usar `getByRole('button', {name:'Yes'}).nth(N)` cuando hay varias con el mismo texto. |
| Teamtailor (`*.teamtailor.com`) | El formulario real vive en un `<dialog>` que aparece tras clicar "Enviar solicitud" la primera vez (puede estar "disabled" hasta que carga). Casilla de consentimiento obligatoria + una opcional de contacto futuro (dejar sin marcar por defecto salvo indicación contraria). |
| TalentClue (`*.talentclue.com`) | Selects nativos reales (`<select>`) para documento de identidad/género/país/formación — sí funciona fijar `.value` + `dispatchEvent('change')` directamente. reCAPTCHA visible al final; **si el primer intento de envío falla, varios campos de texto se vacían y el reCAPTCHA se invalida** — hay que releer el mensaje de error, rellenar de nuevo los campos de texto (los selects sobreviven) y resolver el reCAPTCHA otra vez antes de reintentar. |
| SuccessFactors (`career5.successfactors.eu`, `jobs.<empresa>.com`) | El paso de "Solicitar" desde LinkedIn a veces exige **crear una cuenta nueva** en el portal (email + contraseña) antes de acceder al formulario. Genera una contraseña robusta única por empresa (ver más abajo) y guárdala — no reutilizar entre portales. Los desplegables de país son un widget propio: **hay que clicar la opción del listbox**, fijar el `<select>` nativo no es suficiente para los que están enmascarados como combobox (aunque sí lo es para los verdaderos `<select>`). Para roles con perfil extendido, al expandir "Educación" puede autogenerar varias filas vacías obligatorias — usar los botones "Borrar" para dejar solo 1 fila con el título/nivel/área más relevante (honesto, no hace falta rellenar las 4 si el CV ya tiene el detalle completo). El desplegable "Especialidad" a veces no muestra opciones hasta que el campo se vacía primero (bug del propio widget) — si `[role=option]` sale vacío tras abrir, limpiar el valor y volver a abrir. |
| Viterbit (`careers-*.com` con footer "Hiring with Viterbit") | Formulario corto (Nombre/Apellidos/Email/Teléfono/País/Ciudad/CV), campos Select2 estándar — clicar la opción tras escribir en el buscador interno (`.select2-search__field`). Checkbox de privacidad a veces tapado visualmente por el párrafo adyacente — clicar el `<input>` por id vía `evaluate` si el click normal da timeout por "intercepts pointer events". |

### Contraseñas de cuentas creadas

Si un ATS obliga a crear cuenta, genera una contraseña con:
```
python3 -c "
import secrets, string
alphabet = string.ascii_letters + string.digits
while True:
    pw = ''.join(secrets.choice(alphabet) for _ in range(14))
    if any(c.islower() for c in pw) and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw):
        break
print(pw + '!7')
"
```
Guárdala en `candidaturas/<mes>/<Empresa>/CREDENCIALES.md` (usuario + contraseña, nota de "no compartir"). Menciónala en el resumen final. **Esta carpeta nunca debe subirse a un repo Git ni compartirse** — ver nota de seguridad en `SETUP.md`.

## Fase 4 — Una sola tanda de preguntas para todo el lote

En vez de preguntar oferta por oferta, recopila durante la Fase 1-3 **todo** lo que de verdad requiere criterio humano y consolídalo en una o dos llamadas a AskUserQuestion (máx. 4 preguntas por llamada):

- Expectativas salariales — propón un rango por defecto consistente con `JOB_SEARCH_CRITERIA.md` y solo pregunta si se quiere variarlo para alguna oferta en concreto.
- Datos personales que un ATS suele pedir y que no cambian entre ofertas — **preguntar una sola vez por sesión** y reutilizar en todos los formularios del lote: DNI/NIE o equivalente, fecha de nacimiento, dirección completa. Si ya se preguntaron en una sesión anterior y el dato es estable, no volver a preguntar salvo duda.
- Fecha de incorporación / periodo de preaviso, si el formulario lo pide como fecha concreta (calcular la fecha real a partir de "N días laborables" con Python, no dejarlo en manos del ATS).
- Decisiones de sí/no que son elección personal real (ej. acuerdo B2B vs B2C, adaptaciones de accesibilidad) — explicar la ambigüedad si el formulario no distingue bien las opciones.
- Aprobación de los textos abiertos redactados en la Fase 2 — mostrarlos todos juntos y pedir un solo "apruebo todos" o las correcciones puntuales.

Valida los datos que se den por coherencia obvia (ej. código postal vs. ciudad declarada) antes de usarlos.

## Fase 5 — Revisión final única y confirmación

Presenta **una tabla consolidada** con las N ofertas (empresa/puesto/CV usado/puntos a revisar — contraseñas generadas, gaps comunicados, defaults aplicados sin preguntar) y pide una sola confirmación de envío para todo el lote, tal como exige `apply_external_job.md` §11 (pausa obligatoria). Si se confirma con matices para alguna oferta concreta, aplica solo esos matices antes de enviar esa oferta.

## Fase 6 — Envío secuencial

Recorre las pestañas con `browser_tabs(action:"select", index:N)` — nunca `browser_navigate` — y pulsa el botón de envío de cada una, verificando la confirmación real (texto o cambio de URL a `/thanks`, `/apply-thanks`, `/confirmation`, o similar) antes de pasar a la siguiente. Si un envío falla por validación (ver tabla de ATS arriba), corrige en esa misma pestaña y reintenta antes de seguir con las demás.

## Fase 7 — Cierre en bloque

1. Crea todas las carpetas de Drive que falten en una sola pasada (reutilizar `find_folder_by_path`/`create_subfolder` de `scripts/upload_to_drive.py` vía un script Python de una vez, no una llamada CLI por carpeta):
   ```python
   import sys; sys.path.insert(0, 'scripts')
   from upload_to_drive import find_folder_by_path, create_subfolder, get_service
   service = get_service()
   candidaturas_id = find_folder_by_path(['<tu carpeta de Drive>', 'candidaturas'])
   month_id = create_subfolder(candidaturas_id, '<mes>')
   for company in ['<Empresa1>', '<Empresa2>', ...]:
       create_subfolder(month_id, company)
   ```
2. Sube todos los CVs con `upload_to_drive.py --folder-path` en una secuencia de comandos.
3. Actualiza `TRACKING.md` con una fila por oferta enviada (todas en una sola edición del fichero si es posible) y `SCREENED.md` marcando cada una como "→ Aplicada".
4. Borra todas las copias temporales usadas para subir ficheros, en un único paso.
5. Cierra todas las pestañas del navegador (`browser_close` cierra la actual; repetir o comprobar con `browser_tabs list` que no queda ninguna).

## Lo que NO cambia respecto al modo individual

- Pausa obligatoria antes de cada envío real (Fase 5) — no se salta por ser un lote.
- Nunca inventar datos de cribado, fechas o experiencia — los gaps se comunican, no se disimulan, igual que en `apply_external_job.md`.
- Verificación de sesión (personal, no de trabajo) sigue aplicando una vez al principio de la sesión, no hace falta repetirla por oferta.
