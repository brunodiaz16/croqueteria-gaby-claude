# REGLAS DE NEGOCIO - CROQUETERIA GABY

## MARGENES OBJETIVO
- ROJO  < 8%  -> repreciar o pausar inmediatamente
- AMARILLO 8-14% -> monitorear, buscar mejora
- VERDE > 14%  -> proteger, no bajar precio

## FORMULAS CLAVE
Margen = (Neto_ML - Costo) / Neto_ML * 100
Precio_Minimo = Costo / (1 - comision_ML - margen_objetivo)
Comision ML estimada = 15%
Margen objetivo minimo = 10%

## ESTRUCTURA XLSX DE MERCADO LIBRE
- Titulo de la publicacion -> nombre del producto
- Cantidad -> unidades vendidas
- Neto a recibir -> ingreso total post-comision ML
- Por_Unidad -> neto por unidad vendida
- Costo_Unidad -> costo del producto (puede estar vacio)

## ALERTAS AUTOMATICAS
- Margen < 0% -> perdida activa, pausar publicacion
  - PERO ANTES verificar envios divididos (ver abajo)
- Margen < 8% con mas de 3 unidades -> repreciar urgente
- Ganancia semanal baja mas de 20% vs semana anterior
- Costo de producto = 0 o vacio -> dato faltante
- SKU con 0 ventas en 7 dias -> revisar si pausar

## ENVIOS DIVIDIDOS Y FLEX
- **Flex**: Bruno entrega personalmente, se queda con ingreso de envio.
  Neto Flex > Neto normal para el mismo producto. Columna: "Transportista" / "Forma de entrega" en XLSX de ML.
- **Envios divididos**: Cuando un cliente compra 2+ unidades y ML separa envios,
  asigna costos de envio desproporcionalmente. Un envio parece perdida pero el margen combinado es correcto.
  Ejemplo: Silver Kan $630.80 + $351.80 = $982.60, promedio $491.30 = neto individual real.
- **Regla**: Antes de alertar perdida, verificar si hay ventas del mismo producto en la misma fecha.
  Si la suma/promedio da el neto individual esperado, reportar margen COMBINADO.

## MULTI-PACKS
Algunos listings venden packs. El catalogo guarda costo unitario, multiplicar:
- "2 Costales..." -> costo x2
- "3 Costales..." -> costo x3
- "24 Sobres..." -> costo x24
- "6 Latas ProPlan Gastro" -> catalogo ya tiene costo del 6-pack, NO multiplicar
Verificar notas del producto en el Sheet para saber si costo es unitario o del pack.

## SKUS PRIORITARIOS
Producto | Margen objetivo | Proveedor
Arena Scoop Away 19kg 2-Pack | 14% | Costco
Chapetes Premium Perro 18kg | 16% | Chapetes
Kirkland Gato Pollo/Arroz 11.3kg 2-Pack | 15% | Costco
Ganador Premium 20kg Med/Grande | 12% | Dartacan
Kirkland Salmon/Camote 15.87kg | 14% | Costco
Chapetes Pet Adultos 20kg | 10% | Chapetes
Pro Plan Liveclear 1.5kg | 12% | Invet
Perron Razas Pequenas 20kg | 12% | Dartacan

## DATOS HISTORICOS (referencia)
- Ventas totales historicas: $575,771 MXN
- Ganancia neta historica: $50,281 MXN (8.7% margen promedio)
- Periodo: ene 22 - feb 17, 2026
- Mejor dia: 16 feb 2026 ($94,872 ventas, 57 ordenes, 8.8% margen)
