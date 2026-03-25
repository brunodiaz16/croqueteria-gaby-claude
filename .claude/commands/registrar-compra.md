---
description: Registra compra de proveedor desde foto de ticket o nota. Usar cuando Bruno dice "registra compra", "compra de Dartacan", o adjunta foto de ticket de proveedor. Extrae datos, actualiza costos en Sheet y markdown, genera XLSX de compra.
---

## Ejemplo de uso
```
/registrar-compra Dartacan
/registrar-compra Chapetes C:\ruta\foto_ticket.jpeg
/registrar-compra Dartacan         ← sin foto: busca automáticamente en carpeta de tickets
```

## Argumentos
$ARGUMENTS
- Proveedor (obligatorio): Chapetes, Dartacan, Invet, Costco
- Ruta a imagen del ticket (opcional): si no se da, buscar automáticamente

## Resolución automática del ticket
Si no se proporciona ruta, buscar en este orden:
1. `C:\Users\bruno\CroqueteriaGaby\Tickets\YYYY-MM\DD\[Proveedor].jpeg` (DD = día actual 2 dígitos)
2. `C:\Users\bruno\CroqueteriaGaby\Tickets\YYYY-MM\[Proveedor].jpeg`
3. Si no se encuentra, pedir a Bruno que adjunte la foto

## Contexto
- Proveedores: Chapetes, Dartacan, Invet, Costco
- Costos vigentes: leer CLAUDE.md seccion CATALOGO DE COSTOS VIGENTES
- Aliases conocidos: leer CLAUDE.md seccion ALIASES DE PROVEEDORES
- IMPORTANTE: "Africa" en un ticket = es Chapetes (Africa es la marca de la libreta)
- Tickets de Chapetes: formato "Nota de Remisión Africa", productos en nombre coloquial (Naranjas, Negros, etc.)
- Tickets de Dartacan: formato "PEDIDO", productos con código (20x0192x5) o nombre directo

## Instrucciones

1. **Identificar proveedor**: Validar contra lista conocida.

2. **Extraer datos del ticket**:
   - Fecha, numero de nota/factura
   - Productos, cantidades, precios unitarios, total
   - Para Invet: aplicar descuento (30% es comun) y sumar IVA al precio final

3. **Resolver aliases**: Usar tabla de aliases (ej: "20x0192x5" = Ganador Premium 20kg, "Naranjas" = Chapetes 18kg, "Amarillos" = Chapetes 20kg)

4. **Actualizar costos**:
   - Actualizar el Google Sheet Catalogo_Maestro via scripts/catalogo.py
   - Exportar backup markdown: `python -c "from scripts.catalogo import exportar_costos_md; exportar_costos_md()"`
   - Exportar XLSX del catálogo para Drive: `python -c "from scripts.catalogo import exportar_catalogo_xlsx; exportar_catalogo_xlsx()"`
   - Si hay alias nuevo, agregarlo al Sheet (hoja Aliases) y a CLAUDE.md

5. **Generar XLSX de compra**: `data/xlsx/Compra_[Proveedor]_YYYY-MM-DD.xlsx` con hojas:
   - Info: proveedor, nota, fecha, total
   - Detalle: producto, cantidad, precio_unit, total
   - Por_Marca: mismos datos pero agrupados y con subtotal por marca

6. **Guardar foto del ticket**: Si se proporciono foto, copiarla a:
   `C:\Users\bruno\CroqueteriaGaby\Tickets\YYYY-MM\[Proveedor]_YYYY-MM-DD.jpg`

7. **Recalcular alertas**: Si un costo cambio, recalcular margen y actualizar ALERTAS ACTIVAS en CLAUDE.md

8. **Subir a Drive y limpiar**: `python scripts/upload_to_drive.py --clean`
   Sube: Compra_[Proveedor]_YYYY-MM-DD.xlsx + Catalogo_Maestro_YYYY-MM-DD.xlsx (siempre que se actualice el catálogo)

9. **Commit**: `git add . && git commit -m "compra [proveedor] YYYY-MM-DD - $X total, N productos"`

## Reglas
- Chapetes Premium = 18kg SIEMPRE, nunca 19kg
- Para Invet: costo = P.Final + IVA (16%) — Bruno no deduce IVA
- Si Bruno pasa un precio explicitamente, ese toma precedencia sobre cualquier calculo
- Si el costo cambio vs el registro anterior, marcar en historial
- Siempre preguntar si hay datos ambiguos en el ticket
- Cuando el total del ticket no cuadra con lo leído → calcular algebraicamente qué cantidad/precio falta antes de preguntar
- Si Bruno menciona "X es un doble pack" o "vendemos X como 2-pack" → registrar en Sheet con costo del pack (costo_unit × N), MLM ID propio, y nota "Nx [producto] $Y c/u"
- NO crear entrada "2-Pack" si el MLM ID ya existe en otra fila → actualizar esa fila directamente

## Multi-packs al registrar compra
Cuando en el ticket aparece un producto que en ML se vende como pack:
1. Registrar el costo **unitario** (precio del ticket) en la fila del producto simple
2. Verificar si existe entrada "NxPack" en el Sheet con ese MLM ID — si no existe, crearla con costo = N × unitario
3. Si Bruno confirma que "las ventas de X son Npacks" → asegurar que el MLM ID del listing apunte a la entrada pack, no a la simple
