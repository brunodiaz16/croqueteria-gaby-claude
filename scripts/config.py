"""
Configuracion centralizada — Croqueteria Gaby
Unica fuente de verdad para folder IDs, Sheet IDs, y constantes del proyecto.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# --- Google Sheet IDs ---
CATALOGO_SHEET_ID = "1ypPZlGeRp7QgL6Jpj7Oo6p8RfrqqW1MCcxWF8dDwsCc"

# --- Google Drive Folder IDs ---
FOLDERS = {
    "ROOT": "1PKGCW_SxrnPVnzh6Ah5_cg8klPQ735bq",
    "VENTAS_ABRIL": "111MAHZeXpE0zT-sRK2DK_KgLSx0bl5bB",
    "REPORTES_SEMANALES": "1p6yZuGtwD_1nIRHyHJjnK8ah59U89h8J",  # 02 - Reportes Diarios (padre) — ID anterior no existía
    "COMPRAS_CHAPETES": "1y4WRQB7G9mDvNSD65oqNPw44OwbqUfz-",
    "COMPRAS_DARTACAN": "10ihib3toJ3SeO6G1BdkaPcpg36YdVvOc",
    "COMPRAS_INVET": "1bwCiAbVIt3QhJmSclhtX5gIz1ENp81Mj",
    "COMPRAS_COSTCO": "1z4iGSk9-0ym9BV24D0tfHLwzugegJ172",
    "NOTAS_PEDIDO": "1BLwCScqPTmBiW4GPSZFdKKDWANqxlpE2",  # 04 - Notas de Pedido / Abril 2026
    "CATALOGO_PRECIOS": "1uTeqMTUtzK-mLfT_LNEHAkns8Oc14yls",
    "CONTROL_INVENTARIO": "1_xb-szCE1bHVa5_SXq8_CmcFdlEOOBAs",
    "ANALISIS_ESTRATEGIA": "1B50RXBeCLe0LAayEzw4YhvUnA0L6pAAM",
    "GENERADOS_CLAUDE_ABRIL": "1Ge48lFJ0_ItBU3-MsFYN159mqPkiI06N",
    "HISTORICO_PRECIOS": "1WV5mFQEDLsfym3-VQiiTWTMniX7a22lj",
    "LISTAS_PRECIOS_VIGENTES": "1KvJWSDh2xPIEBkfGI1LcB3K-ixsnZzGl",
    "CSVS_INVENTARIO": "1DcZDC9jnt_wvgfjotlmmstskG-FShzCI",
    "REPORTES_HISTORICOS": "1p6yZuGtwD_1nIRHyHJjnK8ah59U89h8J",
}

# --- Ruteo de archivos a carpetas Drive ---
ROUTING = [
    ("Reporte_CroqueteriaGaby_", FOLDERS["GENERADOS_CLAUDE_ABRIL"]),
    ("Historico_de_Precios_", FOLDERS["HISTORICO_PRECIOS"]),
    ("Lista_Precios_Vigentes_", FOLDERS["LISTAS_PRECIOS_VIGENTES"]),
    ("Catalogo_Maestro_", FOLDERS["CATALOGO_PRECIOS"]),
    ("Compra_Dartacan_", FOLDERS["COMPRAS_DARTACAN"]),
    ("Compra_Chapetes_", FOLDERS["COMPRAS_CHAPETES"]),
    ("Compra_Invet_", FOLDERS["COMPRAS_INVET"]),
    ("Compra_Costco_", FOLDERS["COMPRAS_COSTCO"]),
    ("Nota_Pedido_", FOLDERS["NOTAS_PEDIDO"]),
    ("Reporte_Semanal_", FOLDERS["REPORTES_SEMANALES"]),
    ("Inventario_", FOLDERS["CONTROL_INVENTARIO"]),
    ("Analisis_", FOLDERS["ANALISIS_ESTRATEGIA"]),
    ("importar_inventario_", FOLDERS["CSVS_INVENTARIO"]),
]

# --- Rutas locales ---
XLSX_DIR = PROJECT_ROOT / "data" / "xlsx"
DATA_DIR = PROJECT_ROOT / "data"
CONTEXT_DIR = PROJECT_ROOT / "context"
BITACORA_PATH = CONTEXT_DIR / "bitacora.md"
COSTOS_PATH = CONTEXT_DIR / "costos.md"

# --- OAuth ---
CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"
TOKEN_FILE = PROJECT_ROOT / "token.json"
SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
]

# --- Margenes ---
MARGEN_VERDE = 14    # > 14% = verde
MARGEN_AMARILLO = 8  # 8-14% = amarillo
                     # < 8% = rojo
                     # < 0% = perdida

# --- Categorias de gastos operativos ---
CATEGORIAS_GASTOS = [
    "gasolina",
    "pago_trabajador",
    "transporte_flex",
    "comidas",
    "renta_local",
    "servicios_local",
    "compra_inventario",
    "otro",
]
