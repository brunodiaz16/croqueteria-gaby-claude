# CLAUDE.md — Croquetería Gaby
# Claude Code lee este archivo automáticamente en cada sesión.
# Contiene todo el contexto del negocio. No preguntar lo que ya está aquí.

## IDENTIDAD
- Negocio: Croquetería Gaby — venta de alimentos y accesorios para mascotas
- Dueño: Bruno Díaz
- Canal principal: Mercado Libre MX + Mercado Shops
- Canal secundario: Ventas directas (local, WhatsApp)
- Repo contexto: brunodiaz16/croqueteria-gaby-claude
- App inventario: https://croqueteria-gaby-inventario.vercel.app
- Drive raíz ID: 1PKGCW_SxrnPVnzh6Ah5_cg8klPQ735bq

## ROL DE CLAUDE CODE
Actuar como: analista financiero + operador de datos + estratega de negocio.
- Procesar ventas diarias (XLSX de ML)
- Registrar compras de proveedores (fotos/tickets)
- Calcular márgenes y alertas
- Generar reportes XLSX
- Mantener catálogo de costos actualizado
- Hacer commits al repo con aprendizajes del día
- Nombrar archivos con prefijos correctos para que Apps Script los mueva a Drive

## REGLAS OPERATIVAS (aplicar siempre)

### 1. Plan primero, código después
- Antes de tocar código, escribir o revisar el plan existente
- Si algo falla: parar, re-planear, NO empujar a la fuerza
- Plan activo: `~/.claude/plans/inherited-fluttering-wilkes.md`

### 2. Sub-agents para problemas complejos
- Delegar trabajo pesado a sub-agentes (búsqueda, análisis, etc.)
- Mantener el contexto principal limpio y enfocado

### 3. Loop de auto-mejora
- Cada iteración completada → guardar aprendizajes en `context/bitacora.md`
- Incluir: qué se hizo, qué falló, qué cambió, qué se aprendió
- Próxima sesión lee bitácora y aplica las lecciones

### 4. Probar que funciona
- NUNCA marcar una tarea como completa sin verificar
- Correr scripts, revisar output, verificar archivos generados
- Preguntarse: "¿un staff engineer aprobaría esto?"

### 5. Bug fixing autónomo
- Cuando hay un bug: ir a los logs, encontrar la causa raíz, y resolver
- No pedir al usuario que diagnostique — resolver solo primero
- Si no se puede resolver solo, presentar hallazgos y opciones

### 6. Estado actual (capa de contexto rápido)
- `context/estado_actual.md` se REESCRIBE al cierre de cada sesión
- Contiene: última acción, siguiente paso, blockers, alertas activas
- Al iniciar sesión nueva: leer estado_actual.md ANTES de preguntar al usuario qué hacer
- Diferencia con bitácora: bitácora es histórica (append), estado_actual es snapshot actual (rewrite)

---

## PROVEEDORES

| Proveedor  | Productos                                      |
|------------|------------------------------------------------|
| Chapetes   | Chapetes Premium 18kg, Chapetes 20kg (Amarillos), Maskottchen Premium, Cat Chow, Lukat, Gatina |
| Dartacan   | Ganador, Pedigree, Minino, Dog Chow, Perron, Silver Kan |
| Invet      | Pro Plan, Royal Canin, Nupec, LiveClear, Vet Diet latas |
| Costco     | Kirkland, Pedigree, Scoop Away, Maintenance    |

---

## ALIASES DE PROVEEDORES
# CRÍTICO: Resolver aliases ANTES de calcular márgenes

| Nombre en ticket      | Producto real                         | Peso | Proveedor |
|-----------------------|---------------------------------------|------|-----------|
| Naranjas              | Chapetes Premium Perro Adulto         | 18kg | Chapetes  |
| Amarillos             | Chapetes 20kg                         | 20kg | Chapetes  |
| Meskuten cubito pm    | Maskottchen Premium                   | 15kg | Chapetes  |
| 20x0192x5             | Ganador Premium Adulto                | 20kg | Dartacan  |
| 20x0068x5             | Pedigree Adulto Res/Vegetales         | 20kg | Dartacan  |
| Morado 5kg            | Chapetes Super Premium Gato           | 5kg  | Chapetes  |
| Gato Azul 15kg        | Chapetes Gato Azul                    | 15kg | Chapetes  |
| 25x0384x5             | Kan Kan                               | 25kg | Dartacan  |

REGLA FIJA: Chapetes Premium = 18kg. NUNCA 19kg.

---

## CATÁLOGO DE COSTOS
# Fuente de verdad: Google Sheet Catalogo_Maestro (ver GOOGLE SHEETS IDs)
# Backup local auto-generado: context/costos.md (NO editar manual, correr: py scripts/catalogo.py)
# 83 productos registrados con costos históricos

Si un producto no está en el Sheet → margen = "SIN COSTO" → incluir alerta en reporte.

---

## MÁRGENES OBJETIVO

| Semáforo   | Margen    | Acción                              |
|------------|-----------|-------------------------------------|
| 🟢 Verde   | > 14%     | Proteger, no bajar precio           |
| 🟡 Amarillo| 8% – 14%  | Monitorear                          |
| 🔴 Rojo    | < 8%      | Repreciar o pausar urgente          |
| 🔴 Pérdida | < 0%      | Pausar publicación inmediatamente   |

Fórmula: `Margen = (Neto_ML - Costo) / Neto_ML * 100`
Comisión ML estimada: ~15% (ya descontada en columna "Total MXN" del XLSX)

---

## FORMATO XLSX DE MERCADO LIBRE
- Encabezados en FILA 6 (hay texto de presentación arriba)
- Columna clave de ingresos: `Total (MXN)` — ya es neto post-comisión
- Columna unidades: `Unidades`
- Columna producto: `Título de la publicación`
- La columna `Costo_Unidad` NO existe — cruzar desde catálogo de costos
- Estado `Etiqueta lista para imprimir` = aún no entregado (normal en corte de mañana)

---

## DRIVE — FOLDER IDs
<!-- IMPORTANTE: Carpetas con subcarpetas mensuales. Al cambiar de mes, actualizar los IDs de subcarpetas. -->

| Carpeta                              | ID                                  | Notas                    |
|--------------------------------------|-------------------------------------|--------------------------|
| 01 - Ventas por Día (padre)          | 1jgqqt_fXEoDv5YFbaS8Hldmu4C4Xstq0  |                          |
| 01 - Ventas por Día / 2026-03        | 1ID04u87lSj1bfyE02mfO3AqbYdORZRP7  | ← activa en config.py   |
| 02 - Reportes Diarios (padre)        | 1p6yZuGtwD_1nIRHyHJjnK8ah59U89h8J  |                          |
| 02 - Reportes Diarios / PDF / Marzo  | 1nW52l8hhqofwTds3z7ohtB3pEkD0WH0W  |                          |
| 02 - Reportes Diarios / CSV          | 1DcZDC9jnt_wvgfjotlmmstskG-FShzCI  | ← CSVS_INVENTARIO       |
| 03 - Compras / Chapetes              | 1y4WRQB7G9mDvNSD65oqNPw44OwbqUfz-  |                          |
| 03 - Compras / Dartacan              | 10ihib3toJ3SeO6G1BdkaPcpg36YdVvOc  |                          |
| 03 - Compras / Invet                 | 1bwCiAbVIt3QhJmSclhtX5gIz1ENp81Mj  |                          |
| 03 - Compras / Costco                | 1z4iGSk9-0ym9BV24D0tfHLwzugegJ172  |                          |
| 04 - Notas de Pedido (padre)         | 1EFyRedwQafW4A_MAQGUrerCB05v_r8cO  |                          |
| 04 - Notas de Pedido / Marzo 2026    | 1hCZuAB9uCHKSHdSJGWXYs3eMWYQx__H0  | ← activa en config.py   |
| 05 - Catálogo y Precios              | 1uTeqMTUtzK-mLfT_LNEHAkns8Oc14yls  |                          |
| 06 - Control de Inventario           | 1_xb-szCE1bHVa5_SXq8_CmcFdlEOOBAs  |                          |
| 07 - Análisis y Estrategia           | 1B50RXBeCLe0LAayEzw4YhvUnA0L6pAAM  |                          |
| 08 - Generados por Claude (padre)    | 1yYxUJOkVOHNCkVVaRlLXyCfyzEsQDmxR  |                          |
| 08 - Generados por Claude / 2026-03  | 1m4V3HZutVZ5nzRxwwWwnrREgIIGWEgvT  | ← activa en config.py   |
| Histórico de Precios                 | 1WV5mFQEDLsfym3-VQiiTWTMniX7a22lj  |                          |
| Listas de Precios Vigentes           | 1KvJWSDh2xPIEBkfGI1LcB3K-ixsnZzGl  |                          |

## CONVENCIÓN DE NOMBRES DE ARCHIVO
# Apps Script mueve automáticamente según el prefijo del nombre

| Prefijo                      | Carpeta destino automática           |
|------------------------------|--------------------------------------|
| Reporte_CroqueteriaGaby_     | 08 - Generados por Claude / 2026-03  |
| Reporte_Semanal_             | 02 - Reportes Semanales / 2026       |
| Historico_de_Precios_        | Histórico de Precios                 |
| Lista_Precios_Vigentes_      | Listas de Precios Vigentes           |
| Catalogo_Maestro_            | 05 - Catálogo y Precios              |
| Compra_Dartacan_             | 03 - Compras / Dartacan              |
| Compra_Chapetes_             | 03 - Compras / Chapetes              |
| Compra_Invet_                | 03 - Compras / Invet                 |
| Compra_Costco_               | 03 - Compras / Costco                |
| Nota_Pedido_                 | 04 - Notas de Pedido / 2026-03       |
| Ventas_MX_                   | 01 - Ventas por Día / 2026-03        |

---

## FLUJO DIARIO ESTÁNDAR

### Cuando Bruno dice "procesa las ventas de hoy" + adjunta XLSX:
1. Leer XLSX desde fila 6
2. Extraer: Título, Unidades, Total MXN
3. Cruzar costos desde catálogo de este archivo
4. Resolver aliases si hay tickets de proveedores adjuntos
5. Calcular: Ganancia = Neto - Costo | Margen = Ganancia/Neto*100
6. Aplicar semáforo de márgenes
7. Generar XLSX con 4 hojas: Ventas | Compras | Resumen | Histórico Costos
8. Nombrar: Reporte_CroqueteriaGaby_YYYY-MM-DD.xlsx
9. También generar: Lista_Precios_Vigentes_YYYY-MM-DD.xlsx
10. Si hubo compras: Compra_[Proveedor]_YYYY-MM-DD.xlsx
11. Actualizar catálogo de costos en este CLAUDE.md si cambiaron precios
12. Hacer commit: "reporte YYYY-MM-DD - [resumen de 1 línea]"

### Cuando Bruno dice "registra compra de [proveedor]" + adjunta foto:
1. Extraer: fecha, proveedor, productos, cantidades, precios unitarios
2. Resolver aliases del proveedor
3. Actualizar catálogo de costos en CLAUDE.md
4. Generar Compra_[Proveedor]_YYYY-MM-DD.xlsx
5. Hacer commit: "actualiza costos [proveedor] YYYY-MM-DD"

### Cuando Bruno dice "sube lo aprendido":
1. Crear context/iteraciones/iteracion_NN_aprendizajes.md
2. Incluir: aliases nuevos, costos nuevos, alertas activas, pendientes
3. Actualizar CLAUDE.md si hay cambios en costos o aliases
4. git add . && git commit -m "iteracion NN - [resumen]" && git push

### Cuando Bruno dice "reporte semanal":
1. Consolidar ventas de los últimos 7 días
2. Calcular: ventas totales, ganancia, margen promedio, top productos
3. Generar Reporte_Semanal_S[N]_2026.xlsx
4. Identificar productos por debajo del margen objetivo
5. Generar lista de compras recomendadas

---

## ALERTAS AUTOMÁTICAS
Incluir siempre en el reporte cuando se detecten:
- Margen < 0% → pérdida activa, pausar publicación
- Margen < 8% con 2+ unidades vendidas → repreciar urgente
- Producto sin costo registrado → dato faltante, solicitar a Bruno
- Costo aumentó vs registro anterior → marcar cambio en histórico

## ALERTAS ACTIVAS
- Ganador Premium 20kg: margen 6.0% (🔴) — 5 ventas hoy
  Neto ML $1,053.60 / Costo $990. Precio lista mínimo recomendado: ~$1,350
  Publicación: MLM4663694700
- Pedigree 20kg Res/Vegetales: margen 6.8% (🔴)
  Neto ML $778 / Costo $725. Precio lista mínimo recomendado: ~$970
  Publicación: MLM4619784042
- Dog Chow 25kg: margen 5.7% (🔴)
  Neto ML $955 / Costo $900. Precio lista mínimo recomendado: ~$1,230
  Publicación: MLM4663526262
- Gatina 15kg: margen 5.5% (🔴)
  Neto ML $524 / Costo $495. Precio lista mínimo recomendado: ~$680
  Publicación: MLM4619796770
- LiveClear Gato 3.18kg: margen 3.6% (🔴)
  Neto ML $798 / Costo $768.61. Precio lista mínimo recomendado: ~$1,090
  Publicación: MLM2743362281
- Silver Kan 25kg: margen pendiente de calcular (costo provisional $450, Dartacan)
  Publicación: MLM2668236083

---

## GOOGLE SHEETS IDs

| Sheet               | ID                                        |
|----------------------|------------------------------------------|
| Catalogo_Maestro     | 1ypPZlGeRp7QgL6Jpj7Oo6p8RfrqqW1MCcxWF8dDwsCc       |

## NOTA: ESTRUCTURA DE CARPETAS DRIVE
Las carpetas 01, 02, 04 y 08 tienen subcarpetas mensuales. Los IDs en config.py
deben apuntar a la **subcarpeta del mes activo**, no a la carpeta padre.
Al inicio de cada mes, crear subcarpeta nueva y actualizar IDs en config.py + SubirArchivoDrive.gs.

---

## ESTRUCTURA DEL REPO

```
.claude/
  commands/
    procesar-ventas.md         ← skill /procesar-ventas
    registrar-compra.md        ← skill /registrar-compra
    reporte-semanal.md         ← skill /reporte-semanal
    subir-drive.md             ← skill /subir-drive
    generar-imagenes-pedido.md ← skill /generar-imagenes-pedido
context/
  costos.md                    ← costos vigentes + aliases + historial (backup del Sheet)
  bitacora.md                  ← entradas diarias de aprendizajes (append)
  estado_actual.md             ← snapshot de sesión actual (rewrite cada sesión)
  flujo_de_trabajo.md          ← operaciones día a día
  reglas_de_negocio.md         ← márgenes y SKUs prioritarios
  finanzas_negocio.md          ← ingresos, gastos, estado financiero
  roadmap_herramientas.md      ← qué herramientas usar y cuándo
  schema_inventario.md         ← estructura de la app en Vercel
  uso_carpetas_drive.md        ← quién sube qué y cuándo
scripts/
  catalogo.py                  ← módulo para leer/escribir Google Sheet Catalogo_Maestro
  crear_catalogo_maestro.py    ← script one-time para crear el Sheet
  procesar_ventas.py           ← procesador de ventas reutilizable (no hardcodear fechas)
  upload_to_drive.py           ← sube archivos a Drive con ruteo por prefijo
  OrganizarArchivosDeHoy.gs    ← Apps Script activo con trigger horario
  SubirArchivoDrive.gs         ← Web App para subir archivos a Drive
  generar_notas_imagen.py      ← genera PNGs de notas de pedido para WhatsApp
  limpiar_xlsx_ml.py           ← parser del XLSX de ML (legacy)
prompts/
  procesar_ventas.md
  registrar_compra.md
  reporte_semanal.md
  lista_de_compra.md
docs/
  app_inventario.md
CLAUDE.md                      ← este archivo (leer siempre primero)
README.md
```

---

## DATOS HISTÓRICOS DE REFERENCIA
- Ventas totales registradas: $575,771 MXN
- Ganancia neta histórica: $50,281 MXN (8.7% margen promedio)
- Período: ene 22 – feb 17, 2026
- Mejor día: 16 feb 2026 ($94,872 ventas, 57 órdenes, 8.8% margen)
- SKUs activos: 79

## PENDIENTES ABIERTOS
- [ ] Confirmar si ventas directas van al costo o tienen margen
- [ ] Costos de Kirkland, Scoop Away, Pro Plan — esperando tickets Costco/Invet
- [ ] Crear subcarpetas 2026-04 cuando llegue abril
