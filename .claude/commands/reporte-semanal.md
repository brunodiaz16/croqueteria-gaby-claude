---
description: Genera reporte semanal consolidando los ultimos 7 dias
---

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

3. **Consolidar**:
   - Total neto, total costos, ganancia, margen promedio ponderado
   - Ordenes totales, unidades totales
   - Desglose por dia

4. **Rankings**:
   - Top 10 por volumen de ventas
   - Top 10 por margen
   - Bottom 5 por margen (candidatos a repreciar)

5. **Comparativa**: vs semana anterior si hay datos

6. **Recomendaciones de compra**: Basado en velocidad de venta semanal, estimar que productos necesitan restock

7. **Generar**: `Reporte_Semanal_S[N]_2026.xlsx` con hojas:
   - Resumen: metricas consolidadas
   - Por_Dia: desglose diario
   - Top_Productos: rankings
   - Alertas: productos en rojo
   - Compras_Sugeridas: recomendaciones de restock

8. **Subir a Drive**: `python scripts/upload_to_drive.py Reporte_Semanal_S[N]_2026.xlsx`

9. **Commit**: `git add . && git commit -m "reporte semanal S[N] 2026"`
