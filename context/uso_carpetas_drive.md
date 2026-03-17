# USO DE CARPETAS DRIVE — CROQUETERIA GABY
# Quien sube que, cuando, y con que info

## 01 - Ventas por Dia
QUIEN SUBE: Bruno
CUANDO: Cada dia (meta 8-9am, pero flexible segun contratiempos)
QUE: XLSX descargado de Mercado Libre
FORMATO: 20260317_Ventas_MX_Mercado_Libre_...xlsx
NOTA: Si hay ventas fuera de ML (local, WhatsApp, etc), Bruno las registra
      en un archivo aparte o me las pasa en el chat para que las integre

## 02 - Reportes Semanales
QUIEN SUBE: Claude (genera) + Bruno (mueve ahi)
CUANDO: Cada lunes, consolidando la semana anterior
QUE: Reporte_Semanal_S[N]_2026.xlsx con:
     - Ventas totales ML + fuera de ML
     - Costos consolidados
     - Ganancia neta
     - Margen promedio
     - Top/Bottom productos
     - Estado de gastos fijos de la semana
     - Recomendaciones de compra

## 03 - Compras y Proveedores / [Proveedor] / 2026-MM
QUIEN SUBE: Bruno
CUANDO: Cada vez que hace un pedido a un proveedor
QUE: Foto o PDF del ticket/nota de remision
NOTA: Cuando Bruno sube esto, yo actualizo automaticamente el catalogo
      de costos con los nuevos precios

## 04 - Notas de Pedido / 2026-MM
QUIEN SUBE: Claude (genera) + Bruno (archiva)
CUANDO: Cuando Bruno pide "genera nota de pedido para [proveedor]"
QUE: XLSX o PDF con lista de productos a pedir, cantidades, costos estimados

## 05 - Catalogo y Precios / Maestro de Productos
QUIEN SUBE: Bruno (primera vez) + Claude (actualizaciones)
CUANDO: Setup inicial + cada vez que cambian precios de proveedor
QUE: Excel con columnas: Producto | SKU | Costo actual | Proveedor | Fecha actualizacion
PENDIENTE: Bruno necesita crear este archivo (puede ser simple, 2-3 columnas)

## 05 - Catalogo y Precios / Historico
QUIEN SUBE: Claude
CUANDO: Cada vez que se actualiza un costo
QUE: Registro de cambios de precio con fecha, producto, precio anterior, precio nuevo

## 06 - Control de Inventario / 2026-MM
QUIEN SUBE: Claude (genera) + Bruno (valida)
CUANDO: Semanalmente o cuando Bruno pide revision
QUE: Estado estimado de inventario basado en compras vs ventas registradas
NOTA: Es estimado porque no hay conteo fisico integrado aun

## 07 - Analisis y Estrategia
QUIEN SUBE: Claude
CUANDO: A pedido de Bruno o cuando detecta algo importante
QUE: Analisis de margen por producto, oportunidades de precio,
     productos a pausar, sugerencias de catalogo

## 08 - Generados por Claude / 2026-MM
QUIEN SUBE: Claude (genera) + Bruno (mueve ahi temporalmente)
CUANDO: Cada dia despues de procesar ventas
QUE: Reporte_CroqueteriaGaby_YYYY-MM-DD.xlsx
     Incluye: Ventas ML + ventas fuera ML, costos, margenes, alertas

## VENTAS FUERA DE ML (nuevo)
Canal: Ventas directas (local, WhatsApp, pedidos directos)
Como registrarlas: Bruno me las pasa en el chat con formato:
  "Venta directa: [producto] x[cantidad] a $[precio]"
  o como screenshot/foto de la nota
Donde quedan: Se integran al reporte diario con columna "Canal" = Directo/ML
