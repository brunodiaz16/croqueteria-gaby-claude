# Estado Actual del Proyecto
<!-- Este archivo se REESCRIBE (no append) al final de cada sesión de Claude Code -->
<!-- Leer al inicio de cada sesión para retomar contexto inmediatamente -->

## Última sesión: 2026-03-26

### STOCK ESPECIAL — Pro Plan LiveClear Salmon 1.5kg
- Compra: 10 unidades a $370 c/u = $3,700 total (2026-03-26)
- MLM ID: MLM2743127883
- Gasto registrado en Sheet (compra_inventario) — ya contabilizado en reporte semanal
- Costo en catálogo: $370/unidad
- Unidades restantes: 10 (actualizar aquí cada vez que se vendan)
- REGLA: al vender este producto, el costo $370 ya está en catálogo → aplica normal en reportes diarios
- El gasto $3,700 en "Gastos" es la inversión inicial; los $370 por venta en reportes diarios reflejan el margen real
- Cuando lleguen a 0 unidades: avisar a Bruno y pedir nuevo precio si compra más stock

## Última sesión anterior: 2026-03-20

### Completado hoy
- Reporte 2026-03-20: 18 órdenes, $14,920 neto, 9.7% margen
- Compra Dartacan: Kan Kan 25kg $380 (nuevo producto)
- Compra Costco: 2x Kirkland + 2x Scoop Away ($2,360)
- Agregadas reglas operativas a CLAUDE.md (plan first, sub-agents, auto-mejora, verificar, bug fix)

### Siguiente paso
- Crear skill `/generar-notas-pedido` (notas por marca para trabajador)
- Crear skill `/generar-csv` (verifica costos registrados, genera CSV para app inventario)
- Actualizar plan con flujo diario completo

### Blockers abiertos
- Kan Kan 25kg (MLM2668287827): SIN COSTO registrado en Sheet
- Silver Kan 25kg: margen pendiente de calcular
- Costos Kirkland/Scoop Away: recién registrados, verificar en próximo reporte

### Alertas activas
- Campeón 25kg: 3.9% margen (ROJO) — repreciar urgente
- Perron x2 25kg: 6.9% (ROJO)
- Dog Chow 25kg: 5.7% (ROJO)
- Gatina 15kg: 5.5% (ROJO)

### Plan activo
Fase 1 completada. Fase 1.5-1.8 en progreso (nuevos items del plan).
Ver: `~/.claude/plans/inherited-fluttering-wilkes.md`
