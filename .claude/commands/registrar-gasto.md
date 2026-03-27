# /registrar-gasto — Registrar gasto operativo

Registra un gasto operativo del negocio en la hoja "Gastos" del Catalogo_Maestro.

## Categorias validas

| Categoria | Que incluye |
|-----------|-------------|
| gasolina | Combustible para entregas y compras |
| pago_trabajador | Sueldo semanal/quincenal del trabajador |
| transporte_flex | Casetas, estacionamiento para entregas Flex |
| comidas | Comidas durante operacion |
| renta_local | Renta mensual del local |
| servicios_local | Luz, agua, internet del local |
| compra_inventario | Compras fuera del flujo normal proveedor (ej: material empaque) |
| otro | Gastos miscelaneos |

## Como usar

El usuario dice algo como:
- "Registra $500 de gasolina"
- "Gasto de hoy: trabajador $1200, gasolina $400"
- "La renta del mes fue $8000"
- "Pagué caseta $120 para entregar Flex"

## Que hacer

1. Parsear del mensaje: **categoria**, **monto**, **descripcion** (si la da)
2. Si no queda clara la categoria, preguntar
3. Ejecutar `scripts/gastos.py`:

```python
from scripts.gastos import registrar_gasto
registrar_gasto(
    categoria="gasolina",
    monto=500,
    descripcion="Gasolina semana 24-28 mar",
    metodo_pago="efectivo",  # o transferencia, tarjeta
    fecha="2026-03-24",      # default: hoy
)
```

4. Si el usuario da multiples gastos en un mensaje, registrar cada uno por separado
5. Confirmar al usuario que quedo registrado

## Output esperado

```
Gasto registrado:
  Categoria: gasolina
  Monto: $500.00
  Fecha: 2026-03-24
  Descripcion: Gasolina semana

Total gastos del mes: $X,XXX.XX
```

## Multiples gastos de una vez

Si el usuario dice "Registra: gasolina $500, trabajador $1200, comida $150":
- Registrar los 3 en secuencia
- Mostrar tabla resumen al final

## Notas
- Los gastos se guardan en hoja "Gastos" del Google Sheet Catalogo_Maestro
- Se crean automaticamente en la primera ejecucion
- El reporte semanal (`/reporte-semanal`) lee estos gastos para calcular rentabilidad real
- Metodos de pago: efectivo, transferencia, tarjeta
