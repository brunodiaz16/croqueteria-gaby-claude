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

### FASE 1 — Mostrar tabla para revisión (NO generar CSV todavía)

1. **Leer reporte del dia**: `data/xlsx/Reporte_CroqueteriaGaby_YYYY-MM-DD.xlsx` hoja "Ventas"

2. **Cruzar costos frescos del Sheet** (fuente de verdad, no los del reporte):
   - `from scripts.catalogo import leer_catalogo`
   - Aplicar reglas de multi-pack según título del listing
   - Si costo cambió desde que se procesó el reporte → marcar con ⚠️

3. **Mostrar tabla de revisión en el chat**:
   ```
   | # | Producto                        | Cant | Neto/u   | Costo/u  | Margen | 🚦 |
   |---|----------------------------------|------|----------|----------|--------|----|
   | 1 | Chapetes Premium 18kg            |  3   | $1,020   | $410     | 59.8%  | 🟢 |
   | 2 | Kan Kan 25kg                     |  5   | $491     | $380     | 22.6%  | 🟢 |
   | 3 | Producto sin costo               |  1   |  —       |  —       |   —    | ⚪ |
   ```
   - Ordenar por margen ASC (los problemáticos arriba)
   - Mostrar totales: órdenes, neto total, ganancia estimada, margen promedio

4. **Preguntar**:
   > "¿Algún cambio o está bien? Si todo ok dime y genero el CSV y subo a Drive."
   - Si hay SIN COSTO: listarlos explícitamente y preguntar si registra compras primero o los ignora

### FASE 2 — Aplicar cambios si Bruno los pide

- Bruno puede pedir cambios puntuales: "el costo de X es $Y", "ignora el producto Z", etc.
- Aplicar cada cambio: actualizar Sheet, re-calcular fila afectada, mostrar tabla actualizada
- Repetir hasta que Bruno dé visto bueno

### FASE 3 — Generar CSV y subir a Drive (solo con visto bueno)

5. **Generar CSV**: `data/importar_inventario_YYYY-MM-DD.csv`
   - Columnas: Titulo de la publicacion, Cantidad, Neto_a_recibir_MXN, Por_Unidad, Costo_Unidad
   - Solo productos CON costo (excluir SIN COSTO confirmados por Bruno)
   - Usar costos finales ya corregidos

6. **Subir a Drive**: `python -m scripts.upload_to_drive --clean`
   - Sube: `importar_inventario_YYYY-MM-DD.csv`, `Reporte_CroqueteriaGaby_YYYY-MM-DD.xlsx`, `Lista_Precios_Vigentes_YYYY-MM-DD.xlsx`
   - Limpia archivos locales después de subir

7. **Confirmar**:
   ```
   ✓ CSV generado: importar_inventario_2026-03-20.csv
   ✓ 17 productos incluidos, 1 excluido (sin costo)
   ✓ Subido a Drive — listo para importar en croqueteria-gaby-inventario.vercel.app
   ```

## Inventario futuro
Cuando la app tenga control de inventario:
- Antes de generar, consultar stock actual de la app
- Si un producto YA esta en inventario, marcarlo como "EN STOCK - NO COMPRAR"
- Usar el costo de compra original (el que se registro con /registrar-compra), no el costo actual del Sheet
- Agregar columna "Accion" al CSV: COMPRAR vs YA EN STOCK

## Multi-packs — detección intuitiva
El catálogo guarda costo unitario. Multiplicar cuando el título del listing indique claramente cantidad:

**Patrones que significan x2:**
- "2 Costales...", "2 Bultos...", "2 Bolsas...", "2 Pack...", "2-Pack", "Paquete 2", "Pack 2", "Doble Pack", "Duo"
- Cualquier número al inicio + sustantivo en plural + producto: "2 [cosa] [producto]"

**Patrones que significan x3, x6, x24, etc.:**
- "3 Costales...", "6 Latas..." → x3, x6, etc.
- "24 Sobres..." → x24

**Excepciones (NO multiplicar — el catálogo ya tiene el costo del pack):**
- "6 Latas ProPlan Gastro 380g" → costo ya es del 6-pack ($418.55)
- Verificar notas del producto en el Sheet si hay duda

**Regla general:** si el título empieza con un número seguido de una unidad (costales, bultos, bolsas, latas, sobres, packs) → multiplicar costo x ese número. Si empieza con "2 Pack" o "Paquete 2" o similar → x2.

## Reglas
- NUNCA generar CSV con productos SIN COSTO sin confirmacion de Bruno
- Costo viene del Sheet (fuente de verdad), no hardcodeado
- El CSV se sube a la carpeta de Drive: CSVs de inventario
- Si Bruno pasa un precio nuevo explicitamente, ese toma precedencia sobre el Sheet
