---
description: Genera notas de pedido por marca/proveedor para el trabajador. Usar cuando Bruno dice "genera notas", "que necesito comprar", "pedido para el trabajador", o despues de procesar ventas del dia.
---

## Ejemplo de uso
```
/generar-notas-pedido
/generar-notas-pedido 2026-03-18
```

## Argumentos
$ARGUMENTS
- Opcional: fecha YYYY-MM-DD (default: hoy)
- Si no hay fecha, usa el reporte mas reciente disponible

## Contexto
- Reportes diarios: data/xlsx/Reporte_CroqueteriaGaby_*.xlsx
- Catalogo de costos: Google Sheet Catalogo_Maestro
- Proveedores: Chapetes, Dartacan, Invet, Costco

## Instrucciones

1. **Leer reporte del dia**: Abrir `data/xlsx/Reporte_CroqueteriaGaby_YYYY-MM-DD.xlsx` hoja "Ventas"
   - Si no existe, buscar el mas reciente
   - Si no hay ninguno, pedir a Bruno que corra `/procesar-ventas` primero

2. **Agrupar ventas por proveedor y marca**: Usar columna "Proveedor" del reporte
   - Para cada proveedor, listar productos vendidos con cantidades
   - Agrupar por marca dentro de cada proveedor

3. **Generar notas de pedido**: Crear archivos en `data/xlsx/`:
   - `Nota_Pedido_[Proveedor]_YYYY-MM-DD.xlsx` — una por proveedor con:
     - Hoja "Pedido": producto, marca, cantidad vendida, cantidad sugerida a comprar
     - Cantidad sugerida = cantidad vendida (reposicion 1:1 por default)
   - `Nota_Pedido_General_YYYY-MM-DD.xlsx` — consolidado de todos los proveedores

4. **Generar resumen para WhatsApp**: Mostrar en pantalla un resumen COPIABLE con formato:
   ```
   PEDIDO CHAPETES - 18 Mar 2026
   - 2x Chapetes 20kg (Amarillos)
   - 1x Maskottchen 15kg

   PEDIDO DARTACAN - 18 Mar 2026
   - 5x Ganador Premium 20kg
   - 2x Pedigree 20kg
   - 1x Dog Chow 25kg
   ```
   Este texto Bruno lo puede copiar y pegar directo en WhatsApp para su trabajador.

5. **Subir notas a Drive**: Las notas se suben a carpeta "04 - Notas de Pedido" con `/subir-drive`

## Reglas
- Cantidad sugerida = cantidad vendida hoy (reposicion 1:1)
- Si un producto se vendio 2+ unidades, marcar como PRIORITARIO
- Separar SIEMPRE por proveedor — el trabajador va a un proveedor a la vez
- El resumen para WhatsApp debe ser texto plano, facil de leer en celular
- NO incluir precios en la nota del trabajador (solo producto y cantidad)
