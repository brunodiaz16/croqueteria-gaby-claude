# Plan: Registrar compra Chapetes 2026-03-19

## Contexto
Bruno adjuntó ticket de Africa (= Chapetes) del 19 de marzo 2026. Necesitamos registrar la compra, actualizar costos y aliases nuevos.

## Datos extraídos del ticket

**NOTA DE REMISION — Africa (Chapetes)**
- Fecha: 19-03-2026
- Cliente: Moreno
- Pago: Efectivo ("Efe")

| Qty | Artículo (ticket) | Producto real | Precio unit | Importe |
|-----|-------------------|---------------|-------------|---------|
| 4 | Naranjas | Chapetes Premium 18kg Perro Adulto | $410 | $1,640 |
| 1 | Morado 5 Kg | Chapetes Super Premium Gato 5kg | $185 | $185 |
| 2 | Gato azul 15Kg | Chapetes Pet Gato 15kg | $440 | $880 |

**Total: $2,705**

## Cambios en costos

| Producto | Costo anterior | Costo nuevo | Cambio |
|----------|---------------|-------------|--------|
| Chapetes Premium 18kg | $410 | $410 | SIN CAMBIO |
| Chapetes Super Premium Gato 5kg | — | $185 | NUEVO |
| Chapetes Pet Gato 15kg | — | $440 | NUEVO |

## Aliases nuevos a registrar

| Ticket dice | Producto real | Peso | Proveedor |
|-------------|---------------|------|-----------|
| Morado 5kg | Chapetes Super Premium Gato 5kg | 5kg | Chapetes |
| Gato azul 15kg | Chapetes Pet Gato 15kg | 15kg | Chapetes |

## Pasos de ejecución

### 1. Actualizar Google Sheet Catalogo_Maestro
- `actualizar_costo()` para Chapetes Super Premium Gato 5kg → $185 (si existe en Sheet)
- `actualizar_costo()` para Chapetes Pet Gato 15kg → $440 (si existe en Sheet)
- Chapetes Premium 18kg: sin cambio, no actualizar
- Agregar aliases nuevos a hoja Aliases

### 2. Actualizar context/costos.md
- Agregar 2 productos nuevos a la tabla de costos
- Agregar 2 aliases nuevos a la tabla de aliases
- Agregar entradas al historial de cambios

### 3. Actualizar CLAUDE.md
- Agregar aliases nuevos a sección ALIASES DE PROVEEDORES

### 4. Generar Compra_Chapetes_2026-03-19.xlsx
- Hoja "Info": proveedor, nota, fecha, total
- Hoja "Detalle": producto, cantidad, precio_unit, total
- Hoja "Por_Marca": agrupado con subtotales

### 5. Subir a Drive y limpiar
- `python -m scripts.upload_to_drive --clean`
- El prefijo `Compra_Chapetes_` rutea a carpeta `03 - Compras / Chapetes`

### 6. Commit
- `git add . && git commit -m "compra Chapetes 2026-03-19 - $2,705 total, 3 productos"`

## Archivos a modificar
- `context/costos.md` — agregar 2 productos nuevos + 2 aliases + historial
- `CLAUDE.md` — agregar 2 aliases nuevos
- `data/xlsx/Compra_Chapetes_2026-03-19.xlsx` — generar (temporal, se sube a Drive)

## Verificación
- Confirmar que los 2 productos nuevos aparecen en costos.md
- Confirmar que los aliases nuevos están en CLAUDE.md
- Confirmar que el XLSX se subió a Drive carpeta Chapetes
- `git log -1` muestra el commit de la compra
