
## 2026-03-19 - Reporte del dia
- 14 ordenes, 14 unidades, $8,845.96 neto, $240.44 ganancia, margen 7.8%
- Alertas: Perron Adulto 25kg 4.2%, 6 Latas ProPlan Gastro 38 7.4%, Gatina 15kg 5.5%, Ganador Premium Adulto 20 6.0%
- Pendientes sin costo: Alimento Seco Silver Kan Para , Alimento Seco Chapetes Super P, 2 Costales De Croquetas Chapet, 24 Sobres Minino Plus Sabores , Alimento Seco Silver Kan Para , 3 Costales Croquetas Perro Adu, Silver Kan 25kg, Silver Kan 25kg, Campeón Recetas Caseras Alimen

# BITÁCORA CROQUETERÍA GABY

## 2026-03-18 — Sistema automatizado + catalogo enriquecido
- Catalogo Maestro en Google Sheet: 83 productos (13 base + 70 de historicos)
- Fuente historica: 20 Google Sheets en Drive (ene 22 - feb 17, 2026), 382 registros de ventas
- 131 productos unicos encontrados, 70 nuevos agregados al catalogo con costos
- Pub IDs agregados: MLM2668276953 (Perron 25kg), MLM2668264237 (Chapetes 18kg)
- Silver Kan 25kg: costo historico encontrado = $450 (Chapetes)
- Scope Drive ampliado a readonly para acceder reportes historicos
- Skills creadas: /procesar-ventas, /registrar-compra, /reporte-semanal, /subir-drive
- Script procesar_ventas.py generico reemplaza scripts ad-hoc por fecha
- Script catalogo.py lee/escribe Google Sheet con fallback a markdown
- Corregido: Africa no es proveedor, es Chapetes (marca de la libreta)

## 2026-03-18 — Reporte del día
- 18 órdenes, 19 unidades, $14,528.73 neto, $1,345.91 ganancia, margen 9.9%
- Compra Dartacan #371: 5 Ganador + 2 Pedigree + 1 Dog Chow + 1 Gatina = $7,795
- Compra Chapetes (libreta Africa): 2 Chapetes 20kg (Amarillos) + 2 Maskottchen 15kg = $1,650
- Compra Invet #309372: 6 latas Vet Diet Gastro = $420.01
- Total compras: $9,865.01
- Nuevos costos registrados: Dog Chow 25kg $900, Gatina 15kg $495, Maskottchen 15kg $525, Chapetes 20kg $300, LiveClear 3.18kg $768.61, Lata Gastro $70
- Chapetes tambien vende: Chapetes 20kg (Amarillos) y Maskottchen 15kg (libreta marca Africa)
- Aliases nuevos: Amarillos=Chapetes 20kg, Meskuten cubito pm=Maskottchen Premium 15kg
- Alertas: Ganador 6.0%, Pedigree 6.8%, Dog Chow 5.7%, Gatina 5.5%, LiveClear 3.6% — todos en rojo
- Pendiente: costo Silver Kan 25kg (1 venta hoy, sin costo registrado)
- Pendiente: confirmar proveedor de Arena Scoop Away ($798 por 2-pack)

## 2026-03-17 — Cierre del día
- Flujo completo automatizado funcionando: procesa ventas → genera archivos → sube Drive → commit
- Nuevo costo confirmado: Perrón Adulto 25kg = $535 (Dartacan)
- CSV de importación a app funcionando — se importa directo sin abrir Sheets
- Script subir_drive.py creado con OAuth2
- Google Cloud proyecto "Croqueteria Gaby" creado, Drive API habilitada
- Pendiente: agregar brunodiazb16@gmail.com como usuario de prueba en OAuth consent screen
- Archivos generados hoy: Reporte, Dashboard, Catálogo, Histórico, Lista Precios, Compra Dartacan
- Ventas del día: 5 órdenes, $4,178 neto, margen ~13%
- Costos vigentes: Chapetes 18kg $410, Ganador 20kg $990, Pedigree 20kg $725, Perrón Adulto 25kg $535

## 2026-03-17 (corte vespertino)
- 5 ventas, $4,178.55 neto, $793.55 ganancia, margen 19.0%
- Nuevo costo: Perron Adulto 25kg $535 (Dartacan)
- Compra Dartacan ticket #363: Ganador $990 + Pedigree $725 = $1,715
- Alerta: Pedigree 20kg margen 6.8% 🔴 en envío correo (absorbe $161.50 envío)
- Archivos: Reporte, Compra_Dartacan, Lista_Precios — todos 2026-03-17

## 2026-03-17 (setup inicial)
- Setup inicial completo: Drive mapeado, Apps Script activo con trigger horario
- Aliases confirmados: Naranjas=Chapetes 18kg, 20x0192x5=Ganador, 20x0068x5=Pedigree
- Costos reales confirmados desde nota Dartacan #363
- Alerta activa: Pedigree 20kg margen 6.8% — considerar repreciar a ~$970 lista
- CLAUDE.md creado — Claude Code ya conoce todo el negocio
