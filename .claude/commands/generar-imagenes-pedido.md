---
description: Genera imágenes PNG tipo tarjeta de notas de pedido para enviar por WhatsApp. Usar cuando Bruno dice "genera imagenes", "imagenes de pedido", "png de notas", "tarjetas de pedido".
---

## Ejemplo de uso
```
/generar-imagenes-pedido
/generar-imagenes-pedido 2026-03-19
```

## Argumentos
$ARGUMENTS
- Opcional: fecha YYYY-MM-DD (default: hoy)

## Prerrequisito
- Debe existir `data/xlsx/Nota_Pedido_General_YYYY-MM-DD.xlsx` (generado por `/generar-notas-pedido`)
- Bruno debe haber corregido/validado el General XLSX antes de generar imágenes

## Instrucciones

1. **Verificar que existe el General XLSX**:
   - Buscar `data/xlsx/Nota_Pedido_General_YYYY-MM-DD.xlsx`
   - Si no existe, pedir a Bruno que corra `/generar-notas-pedido` primero

2. **Preguntar confirmación**:
   - "¿Ya corregiste/validaste el General XLSX? Las imágenes se generan a partir de ese archivo."
   - Si Bruno dice que sí, continuar. Si no, esperar.

3. **Ejecutar script**:
   ```bash
   python scripts/generar_notas_imagen.py data/xlsx/Nota_Pedido_General_YYYY-MM-DD.xlsx YYYY-MM-DD
   ```

4. **Verificar output**: Confirmar que se generaron los PNGs en `data/xlsx/`
   - Uno por proveedor: `Nota_Pedido_[Proveedor]_YYYY-MM-DD.png`

5. **Subir a Drive y limpiar**: `python scripts/upload_to_drive.py --clean`

6. **Mostrar resumen**: Listar PNGs generados con proveedor y cantidad de productos

## Colores por proveedor
| Proveedor | Color header |
|-----------|-------------|
| Chapetes  | Verde/teal  |
| Dartacan  | Azul oscuro |
| Invet     | Morado      |
| Costco    | Naranja     |

## Reglas
- SIEMPRE verificar que Bruno validó el General XLSX antes de generar
- Las imágenes son para WhatsApp — diseño limpio, fácil de leer en celular
- NO incluir precios, solo producto y cantidad
