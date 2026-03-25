---
description: Procesa ventas diarias de Mercado Libre. Usar cuando Bruno dice "procesa ventas", "reporte del dia", o da una ruta a un XLSX de ML. Cruza costos, calcula margenes, genera reporte XLSX + CSV para la app, actualiza bitacora, sube a Drive y commitea.
---

## Ejemplo de uso
```
/procesar-ventas 20260325_Ventas_MX_...xlsx
/procesar-ventas C:\ruta\ventas.xlsx 2026-03-18
/procesar-ventas          ← sin argumento: busca el XLSX de hoy automáticamente
```

## Argumentos
$ARGUMENTS
- Primer argumento: nombre de archivo o ruta completa al XLSX de Mercado Libre (opcional)
- Segundo argumento (opcional): fecha YYYY-MM-DD (default: hoy)

## Resolución automática del archivo
Si el argumento NO es una ruta absoluta (o no hay argumento), buscar el archivo en:
- `C:\Users\bruno\CroqueteriaGaby\Ventas\YYYY-MM\` donde YYYY-MM corresponde al mes de la fecha a procesar
- Si hay argumento: buscar archivo cuyo nombre contenga ese argumento en esa carpeta
- Si no hay argumento: buscar el archivo cuyo nombre empiece con la fecha de hoy en formato YYYYMMDD
- Si hay múltiples archivos del mismo día, tomar el más reciente (por nombre, el de hora más alta)
- Si no se encuentra, informar al usuario y mostrar los archivos disponibles en esa carpeta

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
   - `/registrar-compra` ya se encarga de actualizar el Sheet y exportar el Catalogo_Maestro XLSX.

2b. **Si Bruno da precios inline** (ej: "Kan Kan $380") sin ticket formal:
   - Actualizar el Sheet directamente: `python -c "from scripts.catalogo import actualizar_costo; actualizar_costo('Kan Kan 25kg', 380, 'Dartacan', 'inline')"`
   - Exportar costos.md y XLSX del catálogo:
     ```
     python -c "from scripts.catalogo import exportar_costos_md, exportar_catalogo_xlsx; exportar_costos_md(); exportar_catalogo_xlsx()"
     ```
   - El Catalogo_Maestro_YYYY-MM-DD.xlsx se sube junto con el reporte del día en el paso 5.

3. **Revisar alertas**: Si hay productos en ROJO o SIN COSTO, mostrar alerta con precio minimo recomendado (formula: Costo / 0.85 para margen 15%).

4. **Bitacora**: Se actualiza AUTOMATICAMENTE por el script (auto_bitacora). No requiere paso manual.

5. **Subir a Drive (parcial — NO limpiar todavía)**:
   - Si hubo compras: `python -m scripts.upload_to_drive` (sin --clean) para subir Compra_* ya finales
   - El `Reporte_*` y `Lista_Precios_Vigentes_*` se quedan en `data/xlsx/` para que /generar-csv los lea
   - El clean final lo hace /generar-csv cuando Bruno da el visto bueno

6. **Commit**: `git add . && git commit -m "reporte YYYY-MM-DD - N ordenes $X neto, margen X%"`
   Solo quedan los archivos de contexto (bitacora, costos), no los XLSX/CSV generados.

7. **Mostrar resumen final** al usuario con ordenes, neto, ganancia, margen, y alertas.

## Flujo iterativo con tickets

El flujo normal NO es todo-de-una. Es:
1. Bruno pasa el XLSX de ventas → generar reporte con costos que existan en el Sheet (algunos pueden quedar SIN COSTO)
2. Bruno sube tickets o menciona precios → correr `/registrar-compra` por cada uno → Sheet se actualiza, se exporta Catalogo_Maestro XLSX
3. Bruno revisa el reporte y confirma → correr `/generar-csv` con costos ya completos
4. `/generar-notas-pedido` e `/generar-imagenes-pedido` son independientes y van por aparte (para el trabajador, no para el CSV)

Si al generar el CSV todavía hay productos SIN COSTO → preguntar a Bruno si los ignora o los registra primero.

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

## Multi-packs — detección intuitiva
El catálogo guarda costo unitario. Multiplicar cuando el título del listing indique claramente cantidad:

**Patrones que significan x2:**
- "2 Costales...", "2 Bultos...", "2 Bolsas...", "2 Pack...", "2-Pack", "Paquete 2", "Pack 2", "Doble Pack", "Duo"
- Cualquier número al inicio + sustantivo + producto: "2 [unidad] [producto]"

**Patrones que significan x3, x6, x24, etc.:**
- "3 Costales...", "6 Latas..." → x3, x6, etc.
- "24 Sobres..." → x24

**Excepciones (NO multiplicar — el catálogo ya tiene el costo del pack):**
- "6 Latas ProPlan Gastro 380g" → costo ya es del 6-pack ($418.55)
- Verificar notas del producto en el Sheet si hay duda

**Regla general:** número al inicio del título + unidad (costales, bultos, bolsas, latas, sobres, packs) → multiplicar costo x ese número.
