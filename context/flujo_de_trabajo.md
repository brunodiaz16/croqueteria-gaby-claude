# CROQUETERIA GABY - CONTEXTO OPERATIVO Y FINANCIERO

## OBJETIVO
Usar Claude como sistema central para administrar y optimizar Croqueteria Gaby.
- Controlar finanzas diarias
- Analizar ventas y ganancias
- Automatizar reportes
- Generar recomendaciones de negocio
- Optimizar compras a proveedores

Claude actua como: analista financiero + operador de datos + estratega de negocio

## NEGOCIO
Canal principal: Mercado Libre (MX)
Canal secundario: Mercado Shops
Categoria: Alimentos y accesorios para mascotas

## PROVEEDORES
1. Martacan - croquetas genericas (Ganador, Minino, Dog Chow, Perron, Silver Kan)
2. Chapetes - premium (Chapetes, Cat Chow, Lukat, Gatina)
3. Invet - veterinarios (Pro Plan, Royal Canin, Nupec)
4. Costco - (Kirkland, Pedigree, Scoop Away, Maintenance)

## FLUJO DIARIO

OPCION A - Chat directo (recomendado para empezar):
1. Abrir chat con Claude
2. Subir XLSX de ventas ML + fotos de tickets de proveedor
3. Claude procesa, calcula margenes, genera reporte
4. Claude sube output a Drive

OPCION B - Drive como bandeja (para cuando el flujo este estabilizado):
1. Subir XLSX a Drive > 01 - Ventas por Dia > 2026-MM
2. Subir tickets a Drive > 03 - Compras y Proveedores > Proveedor > 2026-MM
3. Decirle a Claude "procesa los archivos de hoy de Drive"

## FUENTES DE DATOS

Ventas ML:
- Archivo XLSX descargado desde Mercado Libre
- Columnas clave: Titulo | Cantidad | Neto a recibir | Por_Unidad | Costo_Unidad

Compras:
- Fotos o PDFs de notas de proveedor (Martacan, Chapetes, Invet)
- Fotos de precios en Costco

## OUTPUT ESPERADO

Reporte diario: Reporte_CroqueteriaGaby_YYYY-MM-DD.xlsx
- Hoja 1: Ventas limpias
- Hoja 2: Costos y margenes por producto
- Hoja 3: Resumen del dia
- Hoja 4: Alertas (productos con margen bajo)

## COMANDOS UTILES PARA CLAUDE
- "Procesa las ventas de hoy" + adjuntar XLSX
- "Registra esta compra de [proveedor]" + adjuntar foto
- "Dame el reporte semanal"
- "Que debo comprar esta semana?"
- "Hay productos vendiendo a perdida?"
- "Genera nota de pedido para Martacan"
- "Guarda el reporte de hoy en Drive"

## META FINAL
Convertir Croqueteria Gaby en un negocio controlado, medible, optimizado y escalable.
