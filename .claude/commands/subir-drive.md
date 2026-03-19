---
description: Sube archivos XLSX y CSV generados a Google Drive. Usar cuando Bruno dice "sube a Drive", "manda los archivos", o despues de generar reportes. Ruteo automatico por prefijo del nombre.
---

## Ejemplo de uso
```
/subir-drive
/subir-drive Reporte_CroqueteriaGaby_2026-03-18.xlsx
```

## Argumentos
$ARGUMENTS
- Opcional: nombres de archivos especificos a subir
- Si no hay argumentos, sube todos los .xlsx y .csv encontrados

## Instrucciones

1. **Listar archivos pendientes**:
   ```
   ls data/xlsx/*.xlsx data/*.csv 2>/dev/null
   ```

2. **Subir y limpiar**: Ejecutar el script con --clean para borrar despues de subir:
   ```
   python scripts/upload_to_drive.py --clean $ARGUMENTS
   ```
   Si no hay argumentos, el script detecta automaticamente archivos en data/xlsx/ y data/*.csv.

3. **Reportar**: Mostrar los links de Drive generados para cada archivo.

## Ruteo automatico por prefijo
El script asigna carpeta en Drive segun el prefijo del nombre:
- Reporte_CroqueteriaGaby_ -> 08 - Generados por Claude
- Compra_Dartacan_ -> 03 - Compras / Dartacan
- Compra_Chapetes_ -> 03 - Compras / Chapetes
- Lista_Precios_Vigentes_ -> Listas de Precios Vigentes
- importar_inventario_ -> Carpeta CSVs inventario en Drive
- Otros -> carpeta raiz

## Despues de subir
Los archivos subidos exitosamente se borran del repo para mantenerlo limpio.
Los XLSX se generan en data/xlsx/ (temporal) y los CSV en data/.
