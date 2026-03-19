---
description: Procesa ventas diarias de Mercado Libre. Usar cuando Bruno dice "procesa ventas", "reporte del dia", o da una ruta a un XLSX de ML. Cruza costos, calcula margenes, genera reporte XLSX + CSV para la app, actualiza bitacora, sube a Drive y commitea.
---

## Ejemplo de uso
```
/procesar-ventas C:\Users\bruno\Desktop\Ventas de ML por dia\18 de Mar de 2026\archivo.xlsx
/procesar-ventas C:\ruta\ventas.xlsx 2026-03-18
```

## Argumentos
$ARGUMENTS
- Primer argumento: ruta al archivo XLSX de Mercado Libre
- Segundo argumento (opcional): fecha YYYY-MM-DD (default: hoy)

## Contexto
- Catalogo de costos: Google Sheet Catalogo_Maestro (via scripts/catalogo.py)
- Fallback: context/costos.md
- Costos vigentes: leer CLAUDE.md seccion CATALOGO DE COSTOS VIGENTES
- Aliases: leer CLAUDE.md seccion ALIASES DE PROVEEDORES

## Instrucciones

1. **Ejecutar el script de procesamiento**:
   ```
   python scripts/procesar_ventas.py <ruta-xlsx> [YYYY-MM-DD]
   ```
   Este script lee costos del Sheet (o fallback markdown), cruza con ventas, y genera:
   - `Reporte_CroqueteriaGaby_YYYY-MM-DD.xlsx`
   - `Lista_Precios_Vigentes_YYYY-MM-DD.xlsx`
   - `data/importar_inventario_YYYY-MM-DD.csv`

2. **Si hay tickets de compra adjuntos**: procesarlos ANTES de correr el script para que los costos esten actualizados. Usar `/registrar-compra` para cada ticket.

3. **Revisar alertas**: Si hay productos en ROJO o SIN COSTO, mostrar alerta con precio minimo recomendado (formula: Costo / 0.85 para margen 15%).

4. **Actualizar bitacora**: Agregar entrada en context/bitacora.md con formato:
   ```
   ## YYYY-MM-DD - Reporte del dia
   - N ordenes, N unidades, $X neto, $X ganancia, margen X%
   - Alertas: [productos en rojo]
   - Pendientes: [productos sin costo]
   ```

5. **Subir a Drive**: `python scripts/upload_to_drive.py`

6. **Commit**: `git add . && git commit -m "reporte YYYY-MM-DD - N ordenes $X neto, margen X%"`

7. **Mostrar resumen final** al usuario con ordenes, neto, ganancia, margen, y alertas.

## Reglas
- Columna de ingresos: "Total (MXN)" — ya es neto post-comision ML
- Chapetes Premium = 18kg SIEMPRE
- Resolver aliases ANTES de calcular margenes
- Si un producto no tiene costo -> SIN COSTO, incluir alerta
- Semaforo: VERDE >14%, AMARILLO 8-14%, ROJO <8%, PERDIDA <0%
