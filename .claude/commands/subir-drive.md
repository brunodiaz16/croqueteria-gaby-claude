---
description: Sube archivos generados a Google Drive
---

## Argumentos
$ARGUMENTS
- Opcional: nombres de archivos especificos a subir
- Si no hay argumentos, sube todos los .xlsx y .csv encontrados

## Instrucciones

1. **Listar archivos pendientes**:
   ```
   ls *.xlsx data/*.csv 2>/dev/null
   ```

2. **Subir**: Ejecutar el script con los archivos indicados:
   ```
   python scripts/upload_to_drive.py $ARGUMENTS
   ```
   Si no hay argumentos, el script detecta automaticamente .xlsx y .csv.

3. **Reportar**: Mostrar los links de Drive generados para cada archivo.

## Ruteo automatico por prefijo
El script asigna carpeta en Drive segun el prefijo del nombre:
- Reporte_CroqueteriaGaby_ -> 08 - Generados por Claude
- Compra_Dartacan_ -> 03 - Compras / Dartacan
- Compra_Chapetes_ -> 03 - Compras / Chapetes
- Lista_Precios_Vigentes_ -> Listas de Precios Vigentes
- importar_inventario_ -> 06 - Control de Inventario
- Otros -> carpeta raiz
