# BITÁCORA CROQUETERÍA GABY

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
