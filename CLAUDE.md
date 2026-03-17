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

---

## PROVEEDORES

| Proveedor  | Productos                                      |
|------------|------------------------------------------------|
| Chapetes   | Chapetes Premium, Cat Chow, Lukat, Gatina      |
| Dartacan   | Ganador, Pedigree, Minino, Dog Chow, Perron    |
| Martacan   | Ganador, Minino, Dog Chow, Perron, Silver Kan  |
| Invet      | Pro Plan, Royal Canin, Nupec                   |
| Costco     | Kirkland, Pedigree, Scoop Away, Maintenance    |

---

## ALIASES DE PROVEEDORES
# CRÍTICO: Resolver aliases ANTES de calcular márgenes

| Nombre en ticket | Producto real                         | Peso | Proveedor |
|------------------|---------------------------------------|------|-----------|
| Naranjas         | Chapetes Premium Perro Adulto         | 18kg | Chapetes  |
| 20x0192x5        | Ganador Premium Adulto                | 20kg | Dartacan  |
| 20x0068x5        | Pedigree Adulto Res/Vegetales         | 20kg | Dartacan  |

REGLA FIJA: Chapetes Premium = 18kg. NUNCA 19kg.

---

## CATÁLOGO DE COSTOS VIGENTES
# Actualizar con cada ticket de proveedor recibido

| Producto                              | Costo | Proveedor | Actualizado  |
|---------------------------------------|-------|-----------|--------------|
| Chapetes Premium 18kg Perro Adulto    | $410  | Chapetes  | 2026-03-17   |
| Ganador Premium Adulto 20kg           | $990  | Dartacan  | 2026-03-17   |
| Pedigree Adulto Res/Vegetales 20kg    | $725  | Dartacan  | 2026-03-17   |

Si un producto no está aquí → margen = "SIN COSTO" → incluir alerta en reporte.

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

| Carpeta                              | ID                                  |
|--------------------------------------|-------------------------------------|
| 01 - Ventas por Día / 2026-03        | 1ID04u87lSj1bfyE02mfO3AqbYdORZRP7  |
| 02 - Reportes Semanales / 2026       | 1Lwa_15i5wtn4Ro5b4mq1ZHTYcSRRNVGH  |
| 03 - Compras / Chapetes              | 1y4WRQB7G9mDvNSD65oqNPw44OwbqUfz-  |
| 03 - Compras / Dartacan              | 10ihib3toJ3SeO6G1BdkaPcpg36YdVvOc  |
| 03 - Compras / Invet                 | 1bwCiAbVIt3QhJmSclhtX5gIz1ENp81Mj  |
| 03 - Compras / Costco                | 1z4iGSk9-0ym9BV24D0tfHLwzugegJ172  |
| 04 - Notas de Pedido / 2026-03       | 1y0i3xMuzm_AX_75KTx8ovdiImRoOAiee  |
| 05 - Catálogo y Precios              | 1uTeqMTUtzK-mLfT_LNEHAkns8Oc14yls  |
| 06 - Control de Inventario           | 1_xb-szCE1bHVa5_SXq8_CmcFdlEOOBAs  |
| 07 - Análisis y Estrategia           | 1B50RXBeCLe0LAayEzw4YhvUnA0L6pAAM  |
| 08 - Generados por Claude / 2026-03  | 1m4V3HZutVZ5nzRxwwWwnrREgIIGWEgvT  |
| Histórico de Precios                 | 1WV5mFQEDLsfym3-VQiiTWTMniX7a22lj  |
| Listas de Precios Vigentes           | 1KvJWSDh2xPIEBkfGI1LcB3K-ixsnZzGl  |

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

## ALERTA ACTIVA HOY
- Pedigree 20kg Res/Vegetales: margen 6.8% (🔴 por debajo de 8%)
  Neto ML $778 / Costo $725. Precio lista mínimo recomendado: ~$970
  Publicación: MLM4619784042

---

## ESTRUCTURA DEL REPO

```
context/
  aliases_proveedores.md       ← diccionario de nombres internos
  catalogo_maestro_costos.md   ← costos vigentes e histórico
  drive_folder_ids.md          ← IDs de carpetas Drive
  flujo_de_trabajo.md          ← operaciones día a día
  reglas_de_negocio.md         ← márgenes y SKUs prioritarios
  finanzas_negocio.md          ← ingresos, gastos, estado financiero
  roadmap_herramientas.md      ← qué herramientas usar y cuándo
  uso_carpetas_drive.md        ← quién sube qué y cuándo
  schema_inventario.md         ← estructura de la app en Vercel
  iteraciones/
    iteracion_01_aprendizajes.md
    iteracion_02_aprendizajes.md
    iteracion_NN_...            ← una por sesión con aprendizajes nuevos
scripts/
  OrganizarArchivosDeHoy.gs    ← Apps Script activo con trigger horario
  CrearCarpetasDrive.gs        ← script inicial de estructura Drive
  limpiar_xlsx_ml.py           ← parser del XLSX de ML
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
- [ ] Martacan: verificar si sigue activo como proveedor o todo viene por Dartacan