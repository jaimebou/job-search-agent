# Setup — instalación técnica

Instalación de una sola vez, antes de poder usar el agente. Sigue los pasos en orden. Todo lo que configures aquí (sesiones de navegador, credenciales OAuth, tokens) es **tuyo y local a tu máquina** — nada de esto forma parte del paquete ni se comparte con nadie.

## 0. Requisitos previos

- **Claude Code** instalado y funcionando.
- **Python 3.10+** y `pip`.
- **Homebrew** (macOS) o equivalente, para instalar dependencias nativas.
- Cuenta de **Google personal** (Gmail) — se usa para Drive (subir CVs/cartas) y Gmail (seguimiento de candidaturas por email). Nunca uses una cuenta corporativa para esto.
- Cuentas ya creadas en los portales de empleo que quieras usar: **LinkedIn** (obligatorio), **InfoJobs** e **Indeed** (opcionales, el agente también funciona solo con LinkedIn si no las tienes).

## 1. MCP de Playwright (navegación automatizada)

El agente necesita un navegador controlable desde Claude Code. Instala el MCP de Playwright siguiendo la documentación oficial de Claude Code para MCP servers (`claude mcp add playwright ...` o equivalente, según tu setup — si ya usas Playwright MCP para otra cosa, no hace falta reinstalarlo, este agente reutiliza el mismo).

Verifica que funciona pidiéndole a Claude que abra una página cualquiera con `browser_navigate` antes de seguir.

## 2. Dependencias Python (conversión CV y subida a Drive)

```bash
pip install -r scripts/requirements.txt
```

Para renderizar PDFs (WeasyPrint) necesitas además la librería nativa `pango`:

```bash
brew install pango
```

## 3. Tu propio Google Drive (OAuth) — para subir CVs y cartas

**No reutilices credenciales de nadie más.** Cada persona crea su propio proyecto de Google Cloud (gratuito, tarda ~10 min la primera vez).

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
3. Playwright mantiene esa sesión abierta mientras dure el proceso del navegador en tu máquina — no persiste entre reinicios salvo que tu configuración de Playwright MCP use un perfil persistente (por defecto, no lo hace).

Antes de cualquier búsqueda o candidatura, el agente verificará explícitamente que la sesión activa es la tuya personal (nunca una cuenta de trabajo) — ver el paso "Verificación de sesión" en cada runbook.

## 5. Verificación final

Antes de pasar al cuestionario de criterios, confirma que:

- [ ] Playwright puede abrir una página y navegar.
- [ ] `python3 scripts/upload_to_drive.py --reauth` funcionó y subió el fichero de prueba.
- [ ] Tienes sesión iniciada en tu cuenta personal de Google (Drive + Gmail) y en LinkedIn.
- [ ] `pip install -r scripts/requirements.txt` y `brew install pango` no dieron error.

Con esto listo, sigue con `ONBOARDING_QUESTIONNAIRE.md` para configurar tus criterios de búsqueda.

## Nota de seguridad

- Nunca compartas `~/.cursor/gdrive-credentials.json` ni los ficheros `*-token*.json` — son tuyos, no se commitean ni se envían a nadie.
- Si en algún momento el agente crea una cuenta nueva en un portal ATS (ver `runbooks/apply_batch_jobs.md` § "Contraseñas de cuentas creadas"), la contraseña se guarda en texto plano en la propia carpeta de esa candidatura (`candidaturas/<mes>/<Empresa>/CREDENCIALES.md`). Es un patrón deliberadamente simple (validado en el agente original), pero significa que **esa carpeta no debe subirse a ningún repo Git ni compartirse** — solo vive en tu máquina local. Si migras este paquete a un repo, añade `candidaturas/*/*/CREDENCIALES.md` a tu `.gitignore` (ya está en el `.gitignore` de este paquete).
