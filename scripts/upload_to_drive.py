"""
Sube archivos a Google Drive — Croquetería Gaby
Usa OAuth 2.0 (credentials.json de app de escritorio)

Uso:
  python scripts/upload_to_drive.py                     # sube todos los .xlsx/.csv de la raíz
  python scripts/upload_to_drive.py archivo1.xlsx ...   # sube archivos específicos
"""

import os
import sys
import glob
import shutil
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# --- Config ---
SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
]
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"
TOKEN_FILE = PROJECT_ROOT / "token.json"

# --- Folder IDs (mismo ruteo que SubirArchivoDrive.gs) ---
FOLDERS = {
    "ROOT": "1PKGCW_SxrnPVnzh6Ah5_cg8klPQ735bq",
    "VENTAS_MARZO": "1ID04u87lSj1bfyE02mfO3AqbYdORZRP7",
    "REPORTES_SEMANALES": "1Lwa_15i5wtn4Ro5b4mq1ZHTYcSRRNVGH",
    "COMPRAS_CHAPETES": "1y4WRQB7G9mDvNSD65oqNPw44OwbqUfz-",
    "COMPRAS_DARTACAN": "10ihib3toJ3SeO6G1BdkaPcpg36YdVvOc",
    "COMPRAS_INVET": "1bwCiAbVIt3QhJmSclhtX5gIz1ENp81Mj",
    "COMPRAS_COSTCO": "1z4iGSk9-0ym9BV24D0tfHLwzugegJ172",
    "NOTAS_PEDIDO": "1y0i3xMuzm_AX_75KTx8ovdiImRoOAiee",
    "CATALOGO_PRECIOS": "1uTeqMTUtzK-mLfT_LNEHAkns8Oc14yls",
    "CONTROL_INVENTARIO": "1_xb-szCE1bHVa5_SXq8_CmcFdlEOOBAs",
    "ANALISIS_ESTRATEGIA": "1B50RXBeCLe0LAayEzw4YhvUnA0L6pAAM",
    "GENERADOS_CLAUDE_MARZO": "1m4V3HZutVZ5nzRxwwWwnrREgIIGWEgvT",
    "HISTORICO_PRECIOS": "1WV5mFQEDLsfym3-VQiiTWTMniX7a22lj",
    "LISTAS_PRECIOS_VIGENTES": "1KvJWSDh2xPIEBkfGI1LcB3K-ixsnZzGl",
    "CSVS_INVENTARIO": "1DcZDC9jnt_wvgfjotlmmstskG-FShzCI",
}

ROUTING = [
    ("Reporte_CroqueteriaGaby_", FOLDERS["GENERADOS_CLAUDE_MARZO"]),
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

MIME_TYPES = {
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xls": "application/vnd.ms-excel",
    ".csv": "text/csv",
    ".pdf": "application/pdf",
    ".json": "application/json",
}


def resolve_folder(filename: str) -> str:
    for prefix, folder_id in ROUTING:
        if filename.startswith(prefix):
            return folder_id
    return FOLDERS["ROOT"]


def get_credentials() -> Credentials:
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"ERROR: No se encontró {CREDENTIALS_FILE}")
                print("Sigue los pasos en credentials_setup.md")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())
    return creds


def upload_file(service, filepath: str) -> dict:
    filename = os.path.basename(filepath)
    folder_id = resolve_folder(filename)
    ext = os.path.splitext(filename)[1].lower()
    mime_type = MIME_TYPES.get(ext, "application/octet-stream")

    # Buscar y reemplazar si ya existe en la carpeta
    query = f"name='{filename}' and '{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id)").execute()
    for old in results.get("files", []):
        service.files().delete(fileId=old["id"]).execute()
        print(f"  Reemplazando archivo existente...")

    file_metadata = {"name": filename, "parents": [folder_id]}
    media = MediaFileUpload(filepath, mimetype=mime_type)
    created = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id,name,webViewLink")
        .execute()
    )
    return created


def main():
    clean_after = "--clean" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--clean"]

    # Determinar archivos a subir
    if args:
        files = args
    else:
        files = sorted(
            glob.glob(str(PROJECT_ROOT / "data" / "xlsx" / "*.xlsx"))
            + glob.glob(str(PROJECT_ROOT / "data" / "*.csv"))
            + glob.glob(str(PROJECT_ROOT / "*.xlsx"))  # fallback raiz
        )

    if not files:
        print("No se encontraron archivos para subir.")
        print("  Busque en: data/xlsx/*.xlsx, data/*.csv, *.xlsx")
        sys.exit(0)

    print("Autenticando con Google Drive...")
    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)

    print(f"\nSubiendo {len(files)} archivo(s):\n")
    subidos = []
    for filepath in files:
        filename = os.path.basename(filepath)
        folder_id = resolve_folder(filename)
        print(f"  {filename} -> carpeta {folder_id[:8]}...")
        try:
            result = upload_file(service, filepath)
            print(f"    OK: {result['webViewLink']}")
            subidos.append(filepath)
        except Exception as e:
            print(f"    ERROR: {e}")

    # Limpiar archivos subidos exitosamente
    if clean_after and subidos:
        print(f"\nLimpiando {len(subidos)} archivo(s) del repo...")
        for fp in subidos:
            os.remove(fp)
            print(f"  Borrado: {os.path.basename(fp)}")

    print(f"\n{len(subidos)}/{len(files)} subidos correctamente.")


if __name__ == "__main__":
    main()
