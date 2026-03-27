# Croqueteria Gaby — Sistema de Administracion con Claude Code

Sistema automatizado para administrar Croqueteria Gaby (tienda de alimentos y accesorios para mascotas) usando Claude Code como analista financiero, operador de datos y estratega de negocio.

## Que hace

- Procesa ventas diarias de Mercado Libre (XLSX) y calcula margenes por producto
- Registra compras de proveedores desde fotos de tickets
- Genera reportes XLSX con semaforo de margenes (verde/amarillo/rojo)
- Mantiene catalogo de costos actualizado en Google Sheets
- Genera CSVs para importar en la [app de inventario](https://croqueteria-gaby-inventario.vercel.app)
- Sube archivos automaticamente a Google Drive con ruteo por prefijo
- Genera notas de pedido por proveedor como imagenes PNG para WhatsApp

## Skills disponibles (Claude Code)

| Skill | Descripcion |
|-------|-------------|
| `/procesar-ventas` | Procesa XLSX de ML, cruza costos, genera reporte + CSV |
| `/registrar-compra` | Registra compra de proveedor desde foto de ticket |
| `/generar-notas-pedido` | Genera notas de pedido por proveedor para el trabajador |
| `/generar-imagenes-pedido` | Genera PNGs de notas para enviar por WhatsApp |
| `/generar-csv` | Verifica costos y genera CSV para app de inventario |
| `/subir-drive` | Sube archivos generados a Drive y limpia repo |
| `/reporte-semanal` | Consolida ventas de la semana con tendencias |
| `/revisar-catalogo` | Health check semanal del catalogo de costos |
| `/registrar-gasto` | Registra gastos operativos (gasolina, trabajador, renta, etc.) |

## Flujo diario

```
MANANA (8am):
  1. /procesar-ventas <ruta-xlsx>     <- procesa ventas del dia
  2. /generar-notas-pedido            <- notas para el trabajador (WhatsApp)

TARDE (despues de compras):
  3. /registrar-compra <proveedor>    <- foto de ticket, registra costos
  4. /generar-csv                     <- CSV para app inventario
  5. /subir-drive                     <- sube todo a Drive

CUANDO HAY GASTOS:
  /registrar-gasto                    <- gasolina, trabajador, renta, etc.

VIERNES:
  6. /reporte-semanal                 <- consolidado con gastos operativos
```

## Estructura del repo

```
.claude/commands/          <- skills de Claude Code (9 skills)
context/
  bitacora.md              <- registro historico de operaciones (auto-append)
  costos.md                <- backup de costos desde Google Sheet (auto-generado)
  estado_actual.md         <- snapshot de sesion (auto-rewrite)
  reglas_de_negocio.md     <- margenes y SKUs prioritarios
  finanzas_negocio.md      <- estado financiero
scripts/
  procesar_ventas.py       <- procesador de ventas con desglose Flex/Normal
  catalogo.py              <- lee/escribe Google Sheet Catalogo_Maestro
  gastos.py                <- registra/lee gastos operativos (hoja Gastos en Sheet)
  config.py                <- config centralizada (folder IDs, Sheet IDs, categorias)
  upload_to_drive.py       <- sube archivos a Drive con ruteo por prefijo
  generar_notas_imagen.py  <- genera PNGs de notas de pedido
  consolidar_semana.py     <- consolida reportes semanales
docs/
  setup.md                 <- guia de instalacion en PC nueva
  guia_archivos.md         <- donde guardar cada archivo
  guia_skills.md           <- como usar cada skill
CLAUDE.md                  <- contexto completo del negocio (leido automaticamente)
```

## Integraciones

- **Google Sheets**: Catalogo Maestro (fuente de verdad para costos)
- **Google Drive**: Almacenamiento organizado por carpetas mensuales
- **Google Apps Script**: Ruteo automatico de archivos por prefijo
- **App Inventario**: [croqueteria-gaby-inventario.vercel.app](https://croqueteria-gaby-inventario.vercel.app) — importa CSVs generados

## Proveedores

| Proveedor | Productos principales |
|-----------|----------------------|
| Chapetes | Chapetes Premium 18kg, Maskottchen, Cat Chow, Gatina |
| Dartacan | Ganador, Pedigree, Minino, Dog Chow, Perron, Silver Kan |
| Invet | Pro Plan, Royal Canin, Nupec, Vet Diet latas |
| Costco | Kirkland, Scoop Away, Maintenance |

## Setup rapido

```bash
git clone https://github.com/brunodiaz16/croqueteria-gaby-claude.git
pip install pandas openpyxl google-auth google-auth-oauthlib google-api-python-client Pillow
# Copiar credentials.json de Google Cloud Console
python scripts/catalogo.py  # Verificar conexion
```

Ver [docs/setup.md](docs/setup.md) para guia completa.
