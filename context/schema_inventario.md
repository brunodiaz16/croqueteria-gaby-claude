# SCHEMA APP INVENTARIO - CROQUETERIA GABY

URL: https://croqueteria-gaby-inventario.vercel.app
Repo: https://github.com/brunodiaz16/croqueteriaGabyInventario
Stack: Next.js App Router + Prisma + PostgreSQL + Vercel

## SECCIONES
- Dashboard: ventas hoy/mes, inventario, ganancia neta
- Productos: CRUD con marca, nombre, SKU, costo, precio
- Ventas: registro con descuento de stock automatico
- Pedidos, Ordenes: historial
- Inventario: entradas de compra y ajustes manuales
- Compras: registro de compras a proveedores
- Estadisticas: vista diaria/semanal/mensual de ventas y margenes
- Importar: carga masiva de productos via CSV

## MODELOS PRISMA
Product: id, marca, nombre, variante, sku, costo, precio
Sale: id, fecha, total, ganancia, notas -> SaleItem[]
SaleItem: cantidad, precioUnitario, costoUnitario, ganancia
Purchase: id, fecha, proveedor, total, notas -> PurchaseItem[]
PurchaseItem: cantidad, costoUnitario, total
InventoryMovement: tipo (COMPRA|VENTA|AJUSTE), cantidad, fecha

## IMPORTACION CSV
Formato: Marca, Nombre, Variante, SKU, Costo, Precio

## DATOS HISTORICOS EN APP
- Ventas totales: $575,771 MXN
- Ganancia neta: $50,281 MXN
- Margen promedio: 8.7%
- Dias con datos: 19 dias (ene 22 - feb 17, 2026)
