# Runbook — Seguimiento de candidaturas (modo manual, no periódico)

Cómo actualizar `candidaturas/TRACKING.md` con lo que ha ido pasando en las candidaturas enviadas. **No es un proceso automático ni periódico** — se ejecuta solo cuando se pide explícitamente (ej. "revisa el estado de mis candidaturas"). La monitorización autónoma/periódica queda descartada por ahora (ver `README.md` § Fuera de alcance).

Diseño deliberadamente simple porque parte de la señal (llamadas, conversaciones) no es automatizable — solo lo es la parte que deja rastro escrito (email).

## Qué se puede automatizar y qué no

- **Email** — sí, totalmente. Se puede buscar en Gmail (cuenta personal) por navegador, igual que con Drive.
- **Llamadas / entrevistas presenciales o por videollamada** — no. No hay forma de que el agente "esté" en una llamada. Aquí el proceso es al revés: se cuenta lo que pasó, y el agente solo estructura esa información en `TRACKING.md`.
- **Portales de candidato de cada ATS** (ej. "mi cuenta" en Teamtailor/Bizneo, donde a veces se ve el estado sin que llegue email) — parcialmente automatizable si ya hay login ahí, pero no está montado en este runbook todavía; de momento se apoya solo en email + lo que se cuente.

## 1. Verificación de sesión

Confirma que la sesión de Gmail activa en el navegador es la personal, igual que para Drive.

## 2. Revisar email por candidatura activa

Para cada fila de `TRACKING.md` con Estado "Enviada" o "En proceso":

1. Ve a `mail.google.com` y busca por el nombre de la empresa combinado con términos como `candidatura`, `application`, `entrevista`, `interview`, o el dominio conocido del ATS.
2. Filtra a correos posteriores a la "Última actualización" registrada en `TRACKING.md` para esa fila — no releer todo el historial cada vez.
3. Para cada correo relevante encontrado, extrae remitente, fecha, asunto y un resumen breve del cuerpo (no hace falta reproducirlo entero).

## 3. Presentar los hallazgos — nunca decidir solo

Los correos de procesos de selección son ambiguos con frecuencia ("seguimos revisando otros perfiles" puede ser un descarte suave o no). **No infieras el nuevo Estado automáticamente** — muestra el correo (o el resumen) y pregunta cómo se interpreta / qué Estado corresponde.

## 4. Registrar lo que se cuente aparte

Si se menciona algo que no dejó rastro en email (una llamada, una entrevista, feedback verbal), pide los detalles mínimos (fecha, con quién, qué se dijo, próximos pasos) y añádelo directamente a Notas — no hace falta que se redacte, solo que se cuente.

## 5. Actualizar TRACKING.md

Por cada candidatura con novedades confirmadas:
- Actualiza **Estado** según la leyenda de `TRACKING.md`.
- Añade una línea nueva en **Notas** con fecha: `[2026-08-15] Email de RRHH: pasan a entrevista técnica, la semana que viene.`
- Actualiza **Última actualización** a la fecha de hoy.

No borres Notas antiguas — es un historial acumulativo de la candidatura, útil para recordar contexto si el proceso se alarga.
