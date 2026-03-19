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
   - `data/xlsx/Reporte_CroqueteriaGaby_YYYY-MM-DD.xlsx`
   - `data/xlsx/Lista_Precios_Vigentes_YYYY-MM-DD.xlsx`
   - `data/importar_inventario_YYYY-MM-DD.csv`

2. **Si hay tickets de compra adjuntos**: procesarlos ANTES de correr el script para que los costos esten actualizados. Usar `/registrar-compra` para cada ticket.

3. **Revisar alertas**: Si hay productos en ROJO o SIN COSTO, mostrar alerta con precio minimo recomendado (formula: Costo / 0.85 para margen 15%).

4. **Bitacora**: Se actualiza AUTOMATICAMENTE por el script (auto_bitacora). No requiere paso manual.

5. **Subir a Drive y limpiar**: `python scripts/upload_to_drive.py --clean`
   Esto sube todos los archivos de data/xlsx/ y data/*.csv a Drive y los borra del repo despues.

6. **Commit**: `git add . && git commit -m "reporte YYYY-MM-DD - N ordenes $X neto, margen X%"`
   Solo quedan los archivos de contexto (bitacora, costos), no los XLSX/CSV generados.

7. **Mostrar resumen final** al usuario con ordenes, neto, ganancia, margen, y alertas.

## Doble corrida diaria (Flex)
Si Bruno baja el XLSX en la manana y luego caen pedidos Flex en la tarde:
- Correr de nuevo con el XLSX actualizado
- El script preguntara si quiere sobreescribir (idempotencia)
- Responder "s" para reemplazar el reporte con datos completos
- La bitacora se actualiza automaticamente con los numeros finales

## Reglas
- Columna de ingresos: "Total (MXN)" — ya es neto post-comision ML
- Columna "Forma de entrega" / "Transportista" distingue Flex vs Mercado Envios
- Chapetes Premium = 18kg SIEMPRE
- Resolver aliases ANTES de calcular margenes
- Si un producto no tiene costo -> SIN COSTO, incluir alerta
- Semaforo: VERDE >14%, AMARILLO 8-14%, ROJO <8%, PERDIDA <0%

## Envios divididos y Flex
- **Flex**: Bruno entrega personalmente, se queda con ingreso de envio. Neto Flex > Neto normal para el mismo producto. No comparar directamente.
- **Envios divididos**: Cuando un cliente compra 2+ unidades y ML separa envios, asigna costos de envio desproporcionalmente a uno. Ejemplo: Silver Kan $630.80 + $351.80 promedia $491.30 (neto real individual).
- **Antes de alertar perdida**: Verificar si hay otra venta del mismo producto en la misma fecha. Si la suma/promedio da el neto individual esperado, reportar margen COMBINADO en lugar de falsa perdida.

## Multi-packs
Algunos listings venden packs. El catalogo guarda costo unitario, multiplicar segun listing:
- "2 Costales..." -> costo x2
- "3 Costales..." -> costo x3
- "24 Sobres..." -> costo x24
- "6 Latas ProPlan Gastro" -> NO multiplicar, catalogo ya tiene costo del 6-pack ($418.55)
Verificar en las notas del producto en el Sheet si el costo es unitario o del pack.
