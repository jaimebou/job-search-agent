# Runbook — Buscar ofertas de empleo (LinkedIn, InfoJobs, Indeed)

Cómo ejecutar una ronda de búsqueda de empleo, filtrar contra tus criterios, y presentar solo lo nuevo y relevante — con independencia de en qué portal aparezca. Complementa `apply_external_job.md` (que arranca donde este runbook termina: una oferta concreta que decides perseguir).

Ver también: `JOB_SEARCH_CRITERIA.md` (criterios) y `candidaturas/SCREENED.md` (ledger de ofertas ya vistas, para no repetir — con columna de fuente y de URL de aplicación real para deduplicar entre portales).

## 0. Verificación de sesión

Antes de tocar cualquier portal, confirma que la sesión activa es tu cuenta personal (LinkedIn con tu nombre real, Google con tu email personal). Para InfoJobs e Indeed, verifica de la misma forma (nombre/email visible en el menú de cuenta) antes de buscar o aplicar — nunca asumas que la sesión sigue abierta de una vez anterior.

## 1. Qué fuentes tocar

Por defecto, busca en **las tres**: LinkedIn, InfoJobs, Indeed (las que tengas configuradas — ver `JOB_SEARCH_CRITERIA.md`). Si se pide acotar a una en concreto, respétalo. Cada fuente tiene su propia sección más abajo con la construcción de la búsqueda y la técnica de extracción.

## 1.bis Tres dimensiones de búsqueda — combinar según lo que se pida

Ver `JOB_SEARCH_CRITERIA.md` § "Dimensiones de búsqueda" para el detalle completo. Resumen operativo:

- **Por empresa** (ej. "revisa ofertas en la Empresa X"): usa la página de empleos de LinkedIn de esa empresa (`/company/<slug>/jobs/`) para obtener su `f_C=<company_id>` real (link "Mostrar todos los empleos" o cluster de empleos relacionados), no el nombre de la empresa como keyword suelta en el buscador general.
- **Por sector**: si se pide ampliar a más empresas del sector, identifica competidores/relacionadas y repite la búsqueda por `f_C` combinando varias en una sola URL (los `f_C` aceptan lista separada por comas).
- **Por rol**: no dependas de una sola keyword. Prueba variantes de título plausibles (según `JOB_SEARCH_CRITERIA.md` § Rol) y, si se señala una habilidad concreta como diferencial, añade esa keyword de herramienta/tecnología además del título. Antes de concluir "no hay nada", valida que el buscador realmente está discriminando: lanza una keyword sin sentido contra el mismo filtro de empresa/geo y comprueba que da 0 resultados (si no da 0, el "no hay nada" anterior no es fiable).

## 2. Screening de cada oferta nueva (igual para las tres fuentes)

Por cada oferta encontrada:

1. Comprueba primero contra `SCREENED.md` (por ID nativo de la fuente, y por URL de aplicación real si ya se conoce) — si ya está registrada, sáltala.
2. **Filtro de título** (rápido): ¿el título coincide con uno de los objetivo o es un derivado plausible? Si es claramente ajeno, descarta sin abrir la oferta.
3. Abre la oferta, extrae la descripción completa vía `browser_evaluate` (no snapshot completo) — funciones/responsabilidades **y** requisitos/herramientas, no solo el resumen.
4. **Lectura de funciones y % de encaje** (obligatoria, nunca decidir solo por el título o por el match de keyword): compara las funciones y el stack técnico de la oferta contra las funciones núcleo y el stack del CV (`JOB_SEARCH_CRITERIA.md` § "Rol"). Presta especial atención a roles que mencionan "IA"/"agentes"/"datos" en el título pero cuyo contenido real es otra cosa (ver exclusiones explícitas en tus criterios).
5. Extrae info de la empresa (industria, tamaño) — LinkedIn e InfoJobs suelen tener un panel dedicado; en Indeed a veces hay que mirar el perfil de empresa enlazado.
6. Contrasta contra `JOB_SEARCH_CRITERIA.md`: modalidad y % teletrabajo, sector/tamaño, consultora (salvo excepción), empresa en la lista de exclusión, rol/seniority (según el % de encaje del paso 4, no el título), salario si está visible.
7. Clasifica: **Encaja** / **Dudosa** (con motivo) / **Descartada** (con motivo, incluyendo desajuste de funciones si aplica).
8. Registra la fila en `SCREENED.md` sea cual sea el resultado — incluyendo la fuente y, si se llega a identificar, la URL de aplicación real (útil para deduplicar si la misma oferta aparece luego en otro portal).

Sé flexible con la ambigüedad (modalidad %, salario, seniority no especificados) — no descartes solo por eso, marca como Dudosa y deja que la persona decida.

## 3. Presentar los resultados

Solo muestra las **Encaja** y **Dudosa**, agrupadas o marcadas por fuente si sale de más de una. Formato tabla:

| Puesto | Empresa | Fuente | Modalidad | Sector | Tamaño | Consultora | Salario | Resultado |
|---|---|---|---|---|---|---|---|---|

Para cada "Dudosa", indica el motivo concreto. Las Descartadas se registran en `SCREENED.md` pero no se detallan (como mucho un recuento por fuente).

## 4. Esperar decisión

La persona decide, oferta por oferta, si quiere seguir ("candidatura OK"). A partir de ahí, continúa con `apply_external_job.md` para esa oferta concreta.

---

## Fuentes

### LinkedIn

URL base:

```
https://www.linkedin.com/jobs/search/?keywords=<KEYWORDS>&location=<CIUDAD>&f_WT=2,3
```

- `f_WT=2,3` → **Remoto (2) e Híbrido (3)** a la vez. `f_WT=1` es Presencial.
- `keywords`: combina con OR los roles objetivo, ej. `Data Analyst OR Analista de datos OR Data Scientist OR Analytics Engineer`.
- Si se da una URL de búsqueda ya armada (con `currentJobId`, `trackingId`, etc.), úsala directamente.

**Extracción** — la lista virtualiza el DOM (solo renderiza unas pocas tarjetas, carga más al hacer scroll del contenedor interno, no de la ventana):

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  // El contenedor con scroll real es un div con overflow-y:auto cuyo clientHeight << scrollHeight.
  // La clase es un hash que cambia con cada deploy de LinkedIn — si este selector falla, re-localízalo
  // subiendo por parentElement desde el <ul> que contiene los enlaces /jobs/view/ hasta encontrar ese div.
  const scroller = document.querySelector('div[class]'); // sustituir por el selector real detectado en vivo
  const seen = new Map();
  const collect = () => {
    document.querySelectorAll('a[href*="/jobs/view/"]').forEach(a => {
      const href = a.href.split('?')[0];
      const jobId = href.match(/\/jobs\/view\/(\d+)/)?.[1];
      const title = a.textContent.trim().replace(/\s+/g,' ');
      if (!title || !jobId || seen.has(jobId)) return;
      const card = a.closest('li');
      seen.set(jobId, { jobId, title, href, cardText: (card?.textContent || '').replace(/\s+/g,' ').trim().slice(0,250) });
    });
  };
  collect();
  const step = Math.max(300, scroller.clientHeight * 0.8);
  for (let i = 0; i < 20; i++) {
    scroller.scrollTop += step;
    await sleep(500);
    collect();
    if (scroller.scrollTop + scroller.clientHeight >= scroller.scrollHeight - 5) break;
  }
  return { count: seen.size, results: Array.from(seen.values()) };
}
```

Repite por página (`&start=25`, `&start=50`, ...) hasta agotar resultados.

**Mecanismo de aplicación**: "Solicitud sencilla" (Easy Apply, dentro de LinkedIn) vs "Solicitar en el sitio web de la empresa" (externo, con interstitial "vas a salir de LinkedIn"). Ver `apply_external_job.md`.

### InfoJobs

URL de búsqueda: usar el buscador normal de `infojobs.net` con la palabra clave y tu ubicación, y aplicar en los filtros de la propia web la opción de teletrabajo — InfoJobs suele distinguir explícitamente "Teletrabajo total" / "Teletrabajo híbrido" en sus filtros, más granular que LinkedIn. **La primera vez que se use esta fuente, verifica los parámetros exactos de la URL navegando el buscador manualmente y anótalos aquí** (no están verificados todavía en este runbook).

**Extracción**: aplica la misma técnica de scroll+collect que en LinkedIn, adaptando el selector a la estructura de InfoJobs (buscar los enlaces de detalle de oferta, típicamente bajo un patrón `/of-i/` en la URL — confirmar la primera vez).

**Mecanismo de aplicación**: InfoJobs tiene su propia "Inscripción sencilla" (equivalente al Easy Apply de LinkedIn) y también ofertas que redirigen a "Solicitar en la web de la empresa". Misma lógica de rama que en `apply_external_job.md`.

### Indeed

URL de búsqueda: `es.indeed.com` (o el dominio de tu país) con la palabra clave y tu ubicación, filtrando por modalidad remoto/híbrido en los filtros de la propia web. **Verifica y anota los parámetros exactos de la URL la primera vez que se use.**

**Extracción**: mismo patrón de scroll+collect, adaptado a la estructura de Indeed (los enlaces de detalle suelen llevar un identificador `jk=` en la query string — usar ese como ID nativo para `SCREENED.md`).

**Mecanismo de aplicación**: Indeed tiene "Solicitar ahora" (a menudo un flujo de aplicación alojado por el propio Indeed) vs. redirección a la web de la empresa. Misma lógica de rama.

---

## Nota sobre fuentes no verificadas

Las secciones de InfoJobs e Indeed están basadas en el funcionamiento general conocido de ambos portales, pero **no se han verificado en vivo todavía** en este paquete (a diferencia de LinkedIn, verificado y usado en producción en el agente original). La primera vez que se busque en cualquiera de las dos, contrasta lo que dice aquí contra lo que se ve realmente en el navegador, y actualiza esta sección con los detalles correctos (URL exacta, selectores, nombre real de los botones de aplicación) — luego considera aportar la mejora de vuelta si este paquete pasa a un repo compartido (ver `CHANGELOG.md`).
