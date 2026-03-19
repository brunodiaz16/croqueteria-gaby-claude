---
description: Registra compra de proveedor desde foto de ticket o nota. Usar cuando Bruno dice "registra compra", "compra de Dartacan", o adjunta foto de ticket de proveedor. Extrae datos, actualiza costos en Sheet y markdown, genera XLSX de compra.
---

## Ejemplo de uso
```
/registrar-compra Dartacan
/registrar-compra Chapetes C:\ruta\foto_ticket.jpg
```

## Argumentos
$ARGUMENTS
- Proveedor (obligatorio): Chapetes, Dartacan, Martacan, Invet, Costco
- Puede incluir ruta a imagen del ticket

## Contexto
- Proveedores: Chapetes, Dartacan, Martacan, Invet, Costco
- Costos vigentes: leer CLAUDE.md seccion CATALOGO DE COSTOS VIGENTES
- Aliases conocidos: leer CLAUDE.md seccion ALIASES DE PROVEEDORES
- IMPORTANTE: "Africa" en un ticket = es Chapetes (Africa es la marca de la libreta)

## Instrucciones

1. **Identificar proveedor**: Validar contra lista conocida.

2. **Extraer datos del ticket**:
   - Fecha, numero de nota/factura
   - Productos, cantidades, precios unitarios, total
   - Para Invet: aplicar descuento (30% es comun) y sumar IVA al precio final

3. **Resolver aliases**: Usar tabla de aliases (ej: "20x0192x5" = Ganador Premium 20kg, "Naranjas" = Chapetes 18kg, "Amarillos" = Chapetes 20kg)

4. **Actualizar costos**:
   - Actualizar el Google Sheet Catalogo_Maestro via scripts/catalogo.py
   - Exportar backup: `python -c "from scripts.catalogo import exportar_costos_md; exportar_costos_md()"`
   - Si hay alias nuevo, agregarlo al Sheet (hoja Aliases) y a CLAUDE.md

5. **Generar XLSX de compra**: `data/xlsx/Compra_[Proveedor]_YYYY-MM-DD.xlsx` con hojas:
   - Info: proveedor, nota, fecha, total
   - Detalle: producto, cantidad, precio_unit, total
   - Por_Marca: mismos datos pero agrupados y con subtotal por marca

6. **Guardar foto del ticket**: Si se proporciono foto, copiarla a:
   `C:\Users\bruno\CroqueteriaGaby\Tickets\YYYY-MM\[Proveedor]_YYYY-MM-DD.jpg`

7. **Recalcular alertas**: Si un costo cambio, recalcular margen y actualizar ALERTAS ACTIVAS en CLAUDE.md

8. **Subir a Drive y limpiar**: `python scripts/upload_to_drive.py --clean`

9. **Commit**: `git add . && git commit -m "compra [proveedor] YYYY-MM-DD - $X total, N productos"`

## Reglas
- Chapetes Premium = 18kg SIEMPRE, nunca 19kg
- Para Invet: costo = P.Final + IVA (16%) — Bruno no deduce IVA
- Si el costo cambio vs el registro anterior, marcar en historial
- Siempre preguntar si hay datos ambiguos en el ticket
