---
description: Genera CSV para importar en la app de inventario (croqueteria-gaby-inventario). Usar cuando Bruno dice "genera csv", "csv para la app", "importar inventario". Verifica que todos los productos tengan costo registrado antes de generar.
---

## Ejemplo de uso
```
/generar-csv
/generar-csv 2026-03-18
```

## Argumentos
$ARGUMENTS
- Opcional: fecha YYYY-MM-DD (default: hoy)

## Contexto
- Reporte del dia: data/xlsx/Reporte_CroqueteriaGaby_YYYY-MM-DD.xlsx
- Catalogo: Google Sheet Catalogo_Maestro
- App destino: https://croqueteria-gaby-inventario.vercel.app -> Importar
- Formato CSV: Titulo de la publicacion, Cantidad, Neto_a_recibir_MXN, Por_Unidad, Costo_Unidad

## Instrucciones

1. **Leer reporte del dia**: Abrir `data/xlsx/Reporte_CroqueteriaGaby_YYYY-MM-DD.xlsx` hoja "Ventas"

2. **VERIFICAR COSTOS** (paso critico):
   - Revisar CADA producto en el reporte
   - Si alguno tiene Semaforo = "SIN COSTO":
     - Mostrar lista de productos sin costo
     - Preguntar a Bruno: "Estos productos no tienen costo registrado. Quieres registrar compras primero? (/registrar-compra)"
     - NO generar CSV hasta que Bruno confirme o diga que ignore esos productos
   - Si todos tienen costo, continuar

3. **Verificar costos del dia** (calidad):
   - Comparar costos usados en el reporte vs costos en el Sheet
   - Si hay diferencia (ej: se registro compra DESPUES de procesar ventas):
     - Avisar: "El costo de [producto] cambio desde que se proceso el reporte"
     - Sugerir re-procesar ventas primero

4. **Generar CSV**: `data/importar_inventario_YYYY-MM-DD.csv`
   - Columnas: Titulo de la publicacion, Cantidad, Neto_a_recibir_MXN, Por_Unidad, Costo_Unidad
   - Solo incluir productos CON costo (excluir SIN COSTO)
   - Usar el costo del Sheet (fuente de verdad), no el del reporte

5. **Mostrar resumen**:
   ```
   CSV generado: data/importar_inventario_2026-03-18.csv
   - 17 productos incluidos
   - 0 excluidos por sin costo
   - Listo para subir en: croqueteria-gaby-inventario.vercel.app -> Importar
   ```

6. **Subir CSV a Drive**: Se sube con `/subir-drive` a la carpeta de CSVs de inventario

## Inventario futuro
Cuando la app tenga control de inventario:
- Antes de generar, consultar stock actual de la app
- Si un producto YA esta en inventario, marcarlo como "EN STOCK - NO COMPRAR"
- Usar el costo de compra original (el que se registro con /registrar-compra), no el costo actual del Sheet
- Agregar columna "Accion" al CSV: COMPRAR vs YA EN STOCK

## Multi-packs
Algunos listings venden packs. El catalogo guarda costo unitario, multiplicar segun listing:
- "2 Costales..." -> costo x2
- "3 Costales..." -> costo x3
- "24 Sobres..." -> costo x24
- "6 Latas ProPlan Gastro" -> NO multiplicar, catalogo ya tiene costo del 6-pack
Verificar notas del producto en el Sheet para saber si costo es unitario o del pack.

## Reglas
- NUNCA generar CSV con productos SIN COSTO sin confirmacion de Bruno
- Costo viene del Sheet (fuente de verdad), no hardcodeado
- El CSV se sube a la carpeta de Drive: CSVs de inventario
- Si Bruno pasa un precio nuevo explicitamente, ese toma precedencia sobre el Sheet
