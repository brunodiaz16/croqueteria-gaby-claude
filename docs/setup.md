# Setup - Croqueteria Gaby

Guia para configurar el sistema en una PC nueva o despues de formatear.

## Requisitos

- Python 3.10+
- Git
- Cuenta Google con acceso al proyecto "Croqueteria Gaby" en Google Cloud Console

## 1. Clonar el repo

```bash
git clone https://github.com/brunodiaz16/croqueteria-gaby-claude.git
cd croqueteria-gaby-claude
```

## 2. Instalar dependencias Python

```bash
pip install pandas openpyxl google-auth google-auth-oauthlib google-api-python-client Pillow
```

Paquetes y para que sirven:
- `pandas` + `openpyxl` — procesar XLSX de ML y generar reportes
- `google-auth` + `google-auth-oauthlib` — autenticacion OAuth2
- `google-api-python-client` — Google Drive y Sheets API
- `Pillow` — generar imagenes PNG de notas de pedido

## 3. Configurar Google Cloud credentials

1. Ir a [Google Cloud Console](https://console.cloud.google.com)
2. Seleccionar proyecto "Croqueteria Gaby"
3. APIs habilitadas: Google Drive API, Google Sheets API
4. Ir a Credenciales > Descargar OAuth 2.0 Client ID como `credentials.json`
5. Copiar `credentials.json` a la raiz del repo: `croqueteria-gaby-claude/credentials.json`

**Primera ejecucion**: Al correr cualquier script, se abre el navegador para autenticar. Despues se genera `token.json` automaticamente.

**Importante**: `credentials.json` y `token.json` estan en `.gitignore`. NO commitear.

## 4. Crear directorios locales

```bash
mkdir -p ~/CroqueteriaGaby/Ventas/2026-03
mkdir -p ~/CroqueteriaGaby/Tickets/2026-03
```

Aqui guardas los XLSX de ML y fotos de tickets antes de procesarlos. Ver `docs/guia_archivos.md` para detalles.

## 5. Verificar que funciona

```bash
# Leer catalogo desde Google Sheet
python scripts/catalogo.py

# Deberia mostrar ~80+ productos con costos
```

Si funciona, el sistema esta listo. Los skills de Claude Code (`.claude/commands/`) funcionan automaticamente.

## 6. Instalar Claude Code (opcional pero recomendado)

```bash
npm install -g @anthropic-ai/claude-code
```

Con Claude Code instalado puedes usar los skills directamente:
- `/procesar-ventas` — procesar ventas del dia
- `/registrar-compra` — registrar compra de proveedor
- `/generar-csv` — generar CSV para app inventario
- `/reporte-semanal` — reporte consolidado semanal
- `/subir-drive` — subir archivos a Google Drive

## Notas

- Los Google Sheet IDs y Drive Folder IDs estan en `scripts/config.py`
- Al cambiar de mes, crear subcarpetas nuevas en Drive y actualizar IDs en `config.py`
- El Sheet Catalogo_Maestro es la fuente de verdad para costos
- `context/costos.md` es backup auto-generado, no editar manualmente
