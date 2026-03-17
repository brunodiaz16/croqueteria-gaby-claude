# APRENDIZAJES — ITERACION 1 (17 Mar 2026)

## ESTRUCTURA REAL DEL DRIVE
La carpeta 08 - Generados por Claude tiene subcarpeta "2026-03 Marzo" (no "Reportes Diarios").
Rutas correctas confirmadas:
- Reportes diarios -> 08 - Generados por Claude > 2026-03 Marzo

## PROBLEMA: Claude sube archivos a "Mi unidad"
Causa: Claude genera el XLSX localmente y Drive lo toma como upload a raiz de Mi unidad.
Solucion temporal: Bruno mueve manualmente via Drive (Recientes > Organizar > Mover)
Solucion ideal: conectar Google Drive MCP para que Claude mueva el archivo automaticamente.

## FORMATO XLSX DE MERCADO LIBRE (corregido)
- Encabezados reales en FILA 6 (no fila 1, hay texto de presentacion arriba)
- Ingresos brutos: "Ingresos por productos (MXN)"
- Neto despues de comision: "Total (MXN)" <- este es el que importa
- Estado en corte de madrugada: "Etiqueta lista para imprimir" (aun no entregado)
- La columna "Costo_Unidad" NO existe en el XLSX de ML exportado
  Los costos hay que cruzarlos desde el catalogo o la app de inventario

## COSTOS — REGLA CRITICA
Los costos NO vienen en el XLSX de ML. Claude los cruza desde:
1. catalogo_79skus_croqueteria.xlsx (en el proyecto)
2. App de inventario (https://croqueteria-gaby-inventario.vercel.app)
3. Archivo maestro de costos que Bruno mantiene actualizado (PENDIENTE crear)

IMPORTANTE: Los costos cambian con cada compra a proveedor.
Cuando Bruno sube un ticket, Claude actualiza el catalogo de costos.
Sin costo actualizado = margen incorrecto = decisiones equivocadas.

## COSTOS USADOS EN ITERACION 1 (verificar con Bruno)
- Chapetes Premium 18kg: $410 MXN
- Ganador Premium 20kg aprox: $895 MXN
- Pedigree 20kg Res/Vegetales: $840 MXN <- REVISAR, este da perdida

## ALERTA ACTIVA — Pedigree 20kg Res/Vegetales
Precio lista: $1,190 | Neto ML: $778 | Costo: $840
Margen: -8% (PERDIDA de $62 por unidad)
Precio minimo para 10pct de margen: ~$988 lista
ACCION REQUERIDA: repreciar o pausar publicacion

## PENDIENTES DE BRUNO PARA FLUJO SMOOTH
1. Crear archivo maestro de costos: producto -> costo actual
   Subirlo a: 05 - Catalogo y Precios > Maestro de Productos
   Actualizarlo cada vez que hay cambio de precio con proveedor
2. Confirmar hora exacta de descarga del XLSX (meta: 8-9am hora Guadalajara)
3. Decidir si mueve reportes manualmente o conectamos Drive MCP

## FLUJO CONFIRMADO (Opcion A — Chat directo)
1. Bruno descarga XLSX de ML idealmente a las 8-9am
2. Bruno adjunta el XLSX en el chat
3. Claude procesa, cruza costos, genera XLSX con 3 hojas: Ventas, Resumen, Alertas
4. Bruno descarga el reporte y lo mueve a 08 - Generados por Claude > 2026-03 Marzo

## DRIVE — ESTRUCTURA REAL CONFIRMADA (difiere del plan)
Mi unidad > Businesses > Croqueteria Gaby >
- 01 - Ventas por Dia
- 02 - Reportes Semanales
- 03 - Compras y Proveedores
- 04 - Notas de Pedido
- 05 - Catalogo y Precios
- 06 - Control de Inventario
- 07 - Analisis y Estrategia
- 08 - Generados por Claude
  - 2026-03 Marzo  <- aqui van los reportes diarios de marzo
- First Context Files (carpeta de contexto inicial)
- Historico de Precios
- Listas de Precios Vigentes
