# Croqueteria Gaby - Claude Context Repo

Sistema de administracion de negocio usando Claude como analista financiero y operador de datos.

## Que es esto

Este repo contiene el contexto operativo, prompts y scripts que permiten a Claude administrar Croqueteria Gaby de forma inteligente entre conversaciones.

Al inicio de cada chat nuevo con Claude pega esto:
"Contexto: soy Bruno de Croqueteria Gaby. Lee el repo brunodiaz16/croqueteria-gaby-claude para tener el contexto completo del negocio."

## Estructura

- context/flujo_de_trabajo.md      -> Como trabajamos dia a dia
- context/reglas_de_negocio.md     -> Margenes, proveedores, SKUs clave
- context/schema_inventario.md     -> Estructura de la app de inventario
- prompts/procesar_ventas.md       -> Prompt para ventas diarias XLSX de ML
- prompts/registrar_compra.md      -> Prompt para tickets de proveedor
- prompts/reporte_semanal.md       -> Prompt para reporte semanal
- prompts/lista_de_compra.md       -> Prompt para sugerencia de compras
- scripts/CrearCarpetasDrive.gs    -> Google Apps Script para Drive
- scripts/limpiar_xlsx_ml.py       -> Parser del XLSX de Mercado Libre
- docs/app_inventario.md           -> Documentacion de la app en Vercel

## Flujo diario

1. Abre chat con Claude
2. Adjunta el XLSX de ventas de ML y fotos de tickets
3. Di "Procesa las ventas y compras de hoy"
4. Claude genera reporte y lo guarda en Drive

## Links

- App inventario: https://croqueteria-gaby-inventario.vercel.app
- Repo inventario: https://github.com/brunodiaz16/croqueteriaGabyInventario
- Drive: https://drive.google.com/drive/folders/1PKGCW_SxrnPVnzh6Ah5_cg8klPQ735bq
