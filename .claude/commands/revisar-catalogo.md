# /revisar-catalogo — Health check del Catalogo Maestro

Revisa la salud del Catalogo_Maestro en Google Sheet y reporta problemas.

## Que hacer

1. Leer el Sheet Catalogo_Maestro completo (hoja Productos)
2. Para cada producto, verificar:

### Checks obligatorios
- **Sin costo**: `costo_actual` vacio o 0 → listar producto
- **Sin publicacion ML**: `publicacion_ml` vacia → listar producto
- **Costo viejo**: `fecha_costo` tiene mas de 30 dias → listar con fecha
- **Sin proveedor**: `proveedor` vacio → listar producto

### Checks de margenes (si hay datos de ventas recientes)
- Leer ultimos reportes en `data/xlsx/Reporte_CroqueteriaGaby_*.xlsx`
- Productos con margen < 0% en ultimas 3 apariciones → **ALERTA CRITICA**
- Productos con margen < 8% consistente → sugerir repreciar

## Output esperado

Imprimir reporte en consola con formato:

```
============================================================
HEALTH CHECK CATALOGO — YYYY-MM-DD
============================================================

CRITICO (accion inmediata):
  - [producto] sin costo registrado (publicacion: MLM...)
  - [producto] margen negativo 3 veces consecutivas

ATENCION (revisar esta semana):
  - [producto] costo no actualizado desde YYYY-MM-DD (XX dias)
  - [producto] sin publicacion ML vinculada

INFO:
  - Total productos: XX
  - Con costo: XX
  - Sin costo: XX
  - Costo actualizado ultimos 7 dias: XX
  - Costo > 30 dias: XX
```

## Frecuencia recomendada
Correr una vez por semana (lunes o viernes) para mantener datos limpios.

## Archivos relevantes
- `scripts/catalogo.py` — funciones `leer_catalogo()` para leer el Sheet
- `scripts/config.py` — `CATALOGO_SHEET_ID`
- `data/xlsx/Reporte_CroqueteriaGaby_*.xlsx` — reportes recientes
