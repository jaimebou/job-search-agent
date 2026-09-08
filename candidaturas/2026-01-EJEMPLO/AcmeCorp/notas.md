# Notas — Candidatura Acme Corp (EJEMPLO — Senior Data Analyst)

> Carpeta de ejemplo, ficticia, para mostrar cómo queda la carpeta de una candidatura real tras seguir `runbooks/apply_external_job.md`. Bórrala (o déjala como referencia fuera de tu flujo real) cuando empieces a usar el agente en serio.

## Qué más habría en esta carpeta en una candidatura real

- `CV_AcmeCorp_012026.md` / `.pdf` — el CV adaptado a esta oferta (paso 6 de `apply_external_job.md`).
- `CoverLetter_AcmeCorp_012026.md` / `.pdf` — si la oferta pedía carta de presentación (paso 9).
- `CREDENCIALES.md` — **solo si** el ATS obligó a crear una cuenta nueva. Ejemplo de cómo se ve (con datos ficticios):

  ```
  ## Cuenta Workday (Acme Corp Candidate Home)

  - Portal: acmecorp-ejemplo.wd3.myworkdayjobs.com
  - Email: tu-email-personal@gmail.com
  - Contraseña: EjemploFicticio26@

  No compartir. Esta carpeta no debe subirse a ningún repo Git.
  ```

## Nota de seguridad

Si migras este paquete a un repositorio Git, asegúrate de que `candidaturas/*/*/CREDENCIALES.md` está en tu `.gitignore` (ya lo está en el de este paquete) — son credenciales reales en texto plano, nunca deben salir de tu máquina.
