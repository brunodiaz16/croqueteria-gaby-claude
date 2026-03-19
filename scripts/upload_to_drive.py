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

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from scripts.config import (
    FOLDERS, ROUTING, SCOPES, PROJECT_ROOT,
    CREDENTIALS_FILE, TOKEN_FILE,
)

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
