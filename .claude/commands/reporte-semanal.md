---
description: Genera reporte semanal consolidando ventas de los ultimos 7 dias. Usar cuando Bruno dice "reporte semanal", "como vamos esta semana", o "consolida la semana". Rankings, margenes, tendencias y recomendaciones de compra.
---

## Ejemplo de uso
```
/reporte-semanal
/reporte-semanal 12
```

## Argumentos
$ARGUMENTS
- Opcional: numero de semana o rango de fechas

## Contexto
- Reportes diarios disponibles en la raiz del proyecto: Reporte_CroqueteriaGaby_*.xlsx
- Bitacora con entradas diarias: context/bitacora.md
- Catalogo de costos: CLAUDE.md seccion CATALOGO DE COSTOS VIGENTES

## Instrucciones

1. **Identificar periodo**: Ultimos 7 dias desde hoy (o semana/rango especificado)

2. **Leer reportes diarios**: Abrir cada Reporte_CroqueteriaGaby_YYYY-MM-DD.xlsx del periodo, hoja "Ventas"

3. **Consolidar ventas**:
   - Total neto, total costos, ganancia, margen promedio ponderado
   - Ordenes totales, unidades totales
   - Desglose por dia
   - Desglose Flex vs Normal (ordenes, neto, margen por tipo)

4. **Consolidar gastos operativos**: Leer gastos del periodo desde Google Sheet:
   ```python
   from scripts.gastos import leer_gastos_periodo, resumen_gastos
   gastos = leer_gastos_periodo(fecha_inicio, fecha_fin)
   resumen = resumen_gastos(gastos)
   ```
   - Desglose por categoria (gasolina, trabajador, transporte_flex, etc.)
   - Total gastos operativos
   - **Ganancia real** = Ganancia bruta (ventas - costos) - Gastos operativos
   - **Margen real** = Ganancia real / Neto total

5. **Rankings**:
   - Top 10 por volumen de ventas
   - Top 10 por margen
   - Bottom 5 por margen (candidatos a repreciar)

5. **Comparativa**: vs semana anterior si hay datos

6. **Recomendaciones de compra**: Basado en velocidad de venta semanal, estimar que productos necesitan restock

8. **Generar**: `Reporte_Semanal_S[N]_2026.xlsx` con hojas:
   - Resumen: metricas consolidadas + ganancia real post-gastos
   - Por_Dia: desglose diario
   - Top_Productos: rankings
   - Alertas: productos en rojo
   - Gastos: desglose por categoria con total
   - Compras_Sugeridas: recomendaciones de restock

9. **Subir a Drive**: `python scripts/upload_to_drive.py Reporte_Semanal_S[N]_2026.xlsx`

10. **Commit**: `git add . && git commit -m "reporte semanal S[N] 2026"`
