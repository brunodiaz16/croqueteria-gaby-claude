# FINANZAS COMPLETAS — CROQUETERIA GABY
# Claude lleva control de INGRESOS y GASTOS completos del negocio

## INGRESOS
1. Ventas ML (Mercado Libre + Mercado Shops)
   - Fuente: XLSX diario exportado de ML
   - Neto: despues de comision y cargos ML
2. Ventas directas (fuera de ML)
   - Local fisico, WhatsApp, pedidos directos
   - Bruno las registra en el chat o en un archivo

## GASTOS FIJOS (Bruno alimenta cuando ocurren)
Categoria | Como me los pasa Bruno
Renta del local | Monto + fecha + "renta [mes]"
Sueldos empleados | Nombre + monto + periodo
Materiales de empaque | Ticket/foto o texto con monto
Servicios (luz, internet, etc) | Monto + mes
Gasolina/transporte | Monto aproximado semanal
Otros gastos operativos | Descripcion + monto

## GASTOS VARIABLES
- Compras a proveedores (ya trackeado via tickets)
- Publicidad ML (aparece en el XLSX como "Venta por publicidad")
- Cualquier gasto imprevisto que Bruno registre

## COMO REGISTRAR UN GASTO
Bruno me dice en el chat:
  "Gasto: renta marzo $8,500"
  "Gasto: sueldo Juan febrero $6,000"
  "Gasto: empaques $450"
Y yo lo registro en el reporte del dia/semana.

## ESTADO FINANCIERO MENSUAL (meta)
Claude genera cada fin de mes:
- Ingresos totales (ML + directo)
- Costo de mercancias vendidas
- Ganancia bruta
- Gastos operativos (renta, sueldos, empaques, etc)
- Utilidad neta del mes
- Comparativa vs mes anterior
- % de ganancia real sobre ventas

## GASTOS CONOCIDOS (llenar con Bruno)
Renta local: $ [pendiente]
Empleados: [pendiente - nombres y sueldos]
Materiales empaque estimado mensual: $ [pendiente]

## REPORTE FINANCIERO SEMANAL COMPLETO
Incluye:
- Ventas brutas ML
- Ventas directas
- Costo mercancias
- Margen bruto
- Gastos fijos prorrateados de la semana
- Utilidad neta real de la semana
