"""
Módulo utilitario para leer/escribir el Catálogo Maestro en Google Sheets.
Fallback a context/costos.md si el Sheet no está disponible.

Uso:
  from scripts.catalogo import leer_catalogo, leer_aliases, actualizar_costo
"""

import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"
TOKEN_FILE = PROJECT_ROOT / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
]

# Se actualiza después de correr crear_catalogo_maestro.py
CATALOGO_SHEET_ID = "1ypPZlGeRp7QgL6Jpj7Oo6p8RfrqqW1MCcxWF8dDwsCc"


def _get_credentials():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"ERROR: No se encontro {CREDENTIALS_FILE}")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())
    return creds


def _get_sheets_service():
    creds = _get_credentials()
    return build("sheets", "v4", credentials=creds)


def leer_catalogo(sheet_id=None):
    """Lee la hoja Productos y retorna dict por publicacion_ml.

    Returns:
        dict: {publicacion_ml: {producto, marca, peso_kg, proveedor,
               costo_actual, categoria, ...}}
    """
    sid = sheet_id or CATALOGO_SHEET_ID
    if not sid:
        print("WARN: CATALOGO_SHEET_ID no configurado, usando fallback markdown")
        return _fallback_costos()

    try:
        service = _get_sheets_service()
        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=sid, range="Productos!A:K")
            .execute()
        )
        rows = result.get("values", [])
        if len(rows) < 2:
            return {}

        headers = rows[0]
        catalogo = {}
        for row in rows[1:]:
            entry = {}
            for i, h in enumerate(headers):
                entry[h] = row[i] if i < len(row) else ""
            # Convertir costo a float
            try:
                entry["costo_actual"] = float(entry.get("costo_actual", 0))
            except (ValueError, TypeError):
                entry["costo_actual"] = None
            # Indexar por cada publicacion ML (pueden ser varias separadas por coma)
            pubs = str(entry.get("publicacion_ml", "")).split(",")
            for pub in pubs:
                pub = pub.strip()
                if pub:
                    catalogo[pub] = entry
        return catalogo
    except Exception as e:
        print(f"WARN: No se pudo leer Sheet: {e}. Usando fallback markdown.")
        return _fallback_costos()


def leer_aliases(sheet_id=None):
    """Lee la hoja Aliases y retorna dict {alias: {producto, proveedor}}.
    """
    sid = sheet_id or CATALOGO_SHEET_ID
    if not sid:
        return {}

    try:
        service = _get_sheets_service()
        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=sid, range="Aliases!A:C")
            .execute()
        )
        rows = result.get("values", [])
        if len(rows) < 2:
            return {}

        aliases = {}
        for row in rows[1:]:
            if len(row) >= 2:
                aliases[row[0]] = {
                    "producto": row[1],
                    "proveedor": row[2] if len(row) > 2 else "",
                }
        return aliases
    except Exception as e:
        print(f"WARN: No se pudo leer aliases: {e}")
        return {}


def actualizar_costo(producto, nuevo_costo, proveedor, fuente, sheet_id=None):
    """Actualiza costo en hoja Productos y agrega entrada al Historial."""
    sid = sheet_id or CATALOGO_SHEET_ID
    if not sid:
        print("ERROR: CATALOGO_SHEET_ID no configurado")
        return False

    try:
        service = _get_sheets_service()

        # Leer productos para encontrar la fila
        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=sid, range="Productos!A:K")
            .execute()
        )
        rows = result.get("values", [])
        headers = rows[0] if rows else []

        col_producto = headers.index("producto") if "producto" in headers else 0
        col_costo = headers.index("costo_actual") if "costo_actual" in headers else 4
        col_anterior = (
            headers.index("costo_anterior") if "costo_anterior" in headers else 5
        )
        col_fecha = headers.index("fecha_costo") if "fecha_costo" in headers else 6

        from datetime import date

        hoy = date.today().isoformat()

        for i, row in enumerate(rows[1:], start=2):
            nombre = row[col_producto] if col_producto < len(row) else ""
            if nombre.lower() == producto.lower():
                costo_ant = row[col_costo] if col_costo < len(row) else ""
                # Actualizar costo_anterior, costo_actual, fecha
                service.spreadsheets().values().update(
                    spreadsheetId=sid,
                    range=f"Productos!{chr(65+col_anterior)}{i}:{chr(65+col_fecha)}{i}",
                    valueInputOption="RAW",
                    body={"values": [[costo_ant, nuevo_costo, hoy]]},
                ).execute()

                # Agregar al historial
                service.spreadsheets().values().append(
                    spreadsheetId=sid,
                    range="Historial_Costos!A:F",
                    valueInputOption="RAW",
                    body={
                        "values": [
                            [hoy, producto, costo_ant, nuevo_costo, proveedor, fuente]
                        ]
                    },
                ).execute()
                print(f"  Catalogo actualizado: {producto} -> ${nuevo_costo}")
                return True

        print(f"  WARN: Producto '{producto}' no encontrado en el Sheet")
        return False
    except Exception as e:
        print(f"ERROR actualizando catalogo: {e}")
        return False


def _fallback_costos():
    """Lee costos desde context/costos.md como fallback."""
    costos_file = PROJECT_ROOT / "context" / "costos.md"
    if not costos_file.exists():
        return {}

    catalogo = {}
    lines = costos_file.read_text(encoding="utf-8").splitlines()
    in_table = False
    for line in lines:
        if line.startswith("| Producto"):
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table and line.startswith("|"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 4:
                producto = parts[0]
                costo_str = parts[1].replace("$", "").replace(",", "").strip()
                proveedor = parts[2]
                try:
                    costo = float(costo_str)
                except ValueError:
                    costo = None
                catalogo[producto] = {
                    "producto": producto,
                    "costo_actual": costo,
                    "proveedor": proveedor,
                }
        elif in_table and not line.startswith("|"):
            in_table = False

    return catalogo


if __name__ == "__main__":
    print("Leyendo catalogo...")
    cat = leer_catalogo()
    if cat:
        for k, v in cat.items():
            print(f"  {k}: {v.get('producto')} -> ${v.get('costo_actual')}")
    else:
        print("  Catalogo vacio o no disponible")
