# CV Scripts

Utilidades para convertir entre PDF y Markdown, y para subir ficheros a tu Google Drive personal.

## Setup (una sola vez)

Ver `SETUP.md` en la raíz del paquete para la instalación completa (incluye `pip install -r scripts/requirements.txt`, `brew install pango`, y la configuración de tu propio OAuth de Google Drive).

## PDF → Markdown

Convierte tu CV en PDF a Markdown limpio para editarlo.

```bash
# Guarda el .md junto al PDF
python3 scripts/pdf_to_md.py cv/cv.pdf

# Especifica destino
python3 scripts/pdf_to_md.py cv/cv.pdf -o cv/cv.md

# Vuelca por stdout (útil para previsualizar o redirigir)
python3 scripts/pdf_to_md.py cv/cv.pdf --stdout
```

## Markdown → PDF

Convierte tu CV o carta de presentación en Markdown a un PDF listo para enviar.

```bash
# CV (tema harvard, por defecto)
python3 scripts/md_to_pdf.py cv/CV_012026.md --theme harvard

# Cover letter (tema espacioso, estilo carta)
python3 scripts/md_to_pdf.py candidaturas/2026-01-EJEMPLO/AcmeCorp/CoverLetter_AcmeCorp_012026.md --theme letter

# Especifica destino
python3 scripts/md_to_pdf.py cv/CV_012026.md -o cv/CV_012026_v2.pdf
```

## Temas disponibles (`--theme`)

| Tema | Uso | Características |
|---|---|---|
| `harvard` | Curriculum vitae (por defecto) | Serif, conservador, cabe en 2 páginas. |
| `cv` | Curriculum vitae (alternativo) | Compacto, sans-serif, más moderno — usar solo si el contexto de la empresa lo justifica (ej. startup muy informal). |
| `letter` | Carta de presentación | Espacioso, párrafos, fuente 11pt. |

## Subir a Google Drive

```bash
python3 scripts/upload_to_drive.py cv/CV_012026.pdf --folder-path "<tu carpeta de Drive>/candidaturas/2026-01/AcmeCorp"
```

Requiere haber completado el paso 3 de `SETUP.md` (tu propio proyecto de Google Cloud + primera autenticación).

## Flujo recomendado

```
1. Importar CV actual:
   pdf_to_md.py cv.pdf → cv.md

2. Revisar y editar cv.md

3. Exportar a PDF para enviar:
   md_to_pdf.py cv.md --theme harvard → cv.pdf

4. Subir a Drive:
   upload_to_drive.py cv.pdf --folder-path "..."
```
