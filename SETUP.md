# Setup — instalación técnica

Instalación de una sola vez, antes de poder usar el agente. Sigue los pasos en orden. Todo lo que configures aquí (sesiones de navegador, credenciales OAuth, tokens) es **tuyo y local a tu máquina** — nada de esto forma parte del paquete ni se comparte con nadie.

## 0. Requisitos previos

- **Claude Code** instalado y funcionando.
- **Python 3.10+** y `pip`.
- **Homebrew** (macOS) o equivalente, para instalar dependencias nativas.
- Cuenta de **Google personal** (Gmail) — se usa para el seguimiento de candidaturas por email (obligatorio) y, opcionalmente, para subir CVs/cartas a Drive (§3). Nunca uses una cuenta corporativa para esto.
- Cuentas ya creadas en los portales de empleo que quieras usar: **LinkedIn** (obligatorio), **InfoJobs** e **Indeed** (opcionales, el agente también funciona solo con LinkedIn si no las tienes).

## 1. MCP de Playwright (navegación automatizada)

El agente necesita un navegador controlable desde Claude Code. Si ya tienes el MCP de Playwright configurado para otra cosa, puedes saltar directo a "1.3 Verificación" — si no, instálalo desde cero con estos 3 pasos.

### 1.1 Instalar el browser que usa `@playwright/mcp`

```bash
mkdir -p ~/.claude/playwright-personal-profile
npx @playwright/mcp@latest install-browser chrome-for-testing
```

> No uses `npx playwright install chromium` a secas — descarga el binario en otra ruta de caché que `@playwright/mcp` no busca. El subcomando correcto es `install-browser chrome-for-testing`.

### 1.2 Registrar el servidor MCP

Edita `~/.claude.json` y añade esta entrada dentro de `mcpServers` (sustituye `<tu-usuario>` por tu usuario de macOS):

```json
"playwright": {
  "type": "stdio",
  "command": "npx",
  "args": [
    "@playwright/mcp@latest",
    "--browser",
    "chromium",
    "--user-data-dir",
    "/Users/<tu-usuario>/.claude/playwright-personal-profile"
  ],
  "env": {}
}
```

- `--browser chromium` es la clave: hace que Playwright use su propio binario ("Google Chrome for Testing"), no tu Chrome real ni uno gestionado por el MDM si usas un Mac corporativo.
- El `--user-data-dir` dedicado (creado en 1.1) es lo que hace que la sesión de LinkedIn/Google del agente **persista entre reconexiones** — inicias sesión a mano una vez y no hace falta repetirlo cada vez que reconectes el MCP.

### 1.3 Activar y verificar

Dentro de Claude Code, ejecuta `/mcp` para que reconecte y cargue esta configuración (no hace falta reiniciar la app). Luego pide que se abra una página cualquiera con `browser_navigate` — si el navegador que se abre es "Google Chrome for Testing" (compruébalo en el dock o con `ps aux | grep "Chrome for Testing"`), está bien configurado.

## 2. Dependencias Python (conversión CV y subida a Drive)

```bash
pip install -r scripts/requirements.txt
```

Para renderizar PDFs (WeasyPrint) necesitas además la librería nativa `pango`:

```bash
brew install pango
```

## 3. Tu propio Google Drive (OAuth) — opcional, solo para subir CVs y cartas

**Este paso es opcional.** No hay ningún MCP de Drive en este paquete — el único sitio donde se usa Google Drive es el script `scripts/upload_to_drive.py`, en el paso final de `apply_external_job.md`/`apply_batch_jobs.md` (§ "Subir a Drive"), para dejar una copia del CV y la cover letter en tu Drive junto al resto de candidaturas.

Si te lo saltas, el agente sigue funcionando igual para buscar, aplicar y hacer seguimiento — simplemente omite ese paso final y los ficheros se quedan solo en `candidaturas/<mes>/<Empresa>/` en tu máquina (puedes subirlos a mano más tarde, o nunca).

Si sí quieres la subida automática, **no reutilices credenciales de nadie más** — cada persona crea su propio proyecto de Google Cloud (gratuito, tarda ~10 min la primera vez).

### 3.1 Crear el proyecto y las credenciales OAuth

1. Ve a [console.cloud.google.com](https://console.cloud.google.com) con tu cuenta de Google **personal**.
2. Crea un proyecto nuevo (ej. `mi-agente-empleo`).
3. **APIs y servicios → Pantalla de consentimiento OAuth**: tipo "Externo", rellena lo mínimo (nombre de la app, tu email de contacto). En "Usuarios de prueba" añade tu propio email de Google.
4. **APIs y servicios → Biblioteca**: activa la **Google Drive API**.
5. **APIs y servicios → Credenciales → Crear credenciales → ID de cliente de OAuth**, tipo **"App de escritorio"**.
6. Descarga el JSON generado y guárdalo como `~/.cursor/gdrive-credentials.json` (la ruta es fija, la usa `scripts/upload_to_drive.py` — puedes cambiarla editando la constante `CREDENTIALS_FILE` en ese script si prefieres otra).

> Guardarlo fuera de esta carpeta (en `~/.cursor/`, no dentro del paquete) es intencional: así nunca se comparte por accidente al reexportar o subir el paquete a un repo.

### 3.2 Primera autenticación

```bash
python3 scripts/upload_to_drive.py --reauth
```

Esto abrirá el navegador para que autorices el acceso con tu cuenta de Google. El token queda guardado en `~/.cursor/gdrive-token-upload.json` (tampoco se comparte, no se toca a mano).

### 3.3 Probarlo

```bash
python3 scripts/upload_to_drive.py cv/EJEMPLO_CV.md
```

Si te devuelve un link de Drive, funciona. Borra ese fichero de prueba de tu Drive después.

## 4. Sesiones de los portales de empleo — sin cookies, login manual

El agente **nunca** usa cookies ni credenciales guardadas en este paquete. En tu primera sesión con el agente, cuando te pida buscar o aplicar a algo, hará esto:

1. Abrirá el navegador (vía Playwright) en LinkedIn/InfoJobs/Indeed.
2. Si no hay sesión activa, te pedirá que inicies sesión tú mismo, a mano, en esa ventana del navegador (usuario/contraseña, 2FA si lo tienes activado).
3. Con el `--user-data-dir` dedicado del paso 1.2, esa sesión persiste entre reconexiones del MCP — solo tienes que hacer login manual la primera vez por portal, no en cada sesión de trabajo.

Antes de cualquier búsqueda o candidatura, el agente verificará explícitamente que la sesión activa es la tuya personal (nunca una cuenta de trabajo) — ver el paso "Verificación de sesión" en cada runbook.

## 5. Verificación final

Antes de pasar al cuestionario de criterios, confirma que:

- [ ] Playwright puede abrir una página y navegar (con "Google Chrome for Testing", no tu Chrome normal).
- [ ] `pip install -r scripts/requirements.txt` y `brew install pango` no dieron error.
- [ ] Tienes sesión iniciada en tu cuenta personal de Google (Gmail, para seguimiento) y en LinkedIn.
- [ ] *(Opcional)* `python3 scripts/upload_to_drive.py --reauth` funcionó y subió el fichero de prueba — solo si vas a usar la subida automática a Drive (§3).

Con esto listo, sigue con `ONBOARDING_QUESTIONNAIRE.md` para configurar tus criterios de búsqueda.

## Nota de seguridad

- Nunca compartas `~/.cursor/gdrive-credentials.json` ni los ficheros `*-token*.json` — son tuyos, no se commitean ni se envían a nadie.
- Si en algún momento el agente crea una cuenta nueva en un portal ATS (ver `runbooks/apply_batch_jobs.md` § "Contraseñas de cuentas creadas"), la contraseña se guarda en texto plano en la propia carpeta de esa candidatura (`candidaturas/<mes>/<Empresa>/CREDENCIALES.md`). Es un patrón deliberadamente simple (validado en el agente original), pero significa que **esa carpeta no debe subirse a ningún repo Git ni compartirse** — solo vive en tu máquina local. Si migras este paquete a un repo, añade `candidaturas/*/*/CREDENCIALES.md` a tu `.gitignore` (ya está en el `.gitignore` de este paquete).
