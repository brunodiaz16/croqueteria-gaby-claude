"""
Lee reportes historicos de Drive, extrae productos y enriquece el Catalogo Maestro.
Usa el costo MAS RECIENTE como referencia cuando hay fluctuacion.

Uso: python scripts/enriquecer_catalogo.py
"""

import io
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"
TOKEN_FILE = PROJECT_ROOT / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
]

FOLDER_REPORTES = "1p6yZuGtwD_1nIRHyHJjnK8ah59U89h8J"
CATALOGO_SHEET_ID = "1ypPZlGeRp7QgL6Jpj7Oo6p8RfrqqW1MCcxWF8dDwsCc"


def get_credentials():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())
    return creds


def listar_archivos_recursivo(drive_service, folder_id, depth=0):
    """Lista todos los archivos en una carpeta de Drive, recursivamente."""
    archivos = []
    query = f"'{folder_id}' in parents and trashed=false"
    results = (
        drive_service.files()
        .list(q=query, fields="files(id, name, mimeType, createdTime, modifiedTime)", pageSize=100)
        .execute()
    )
    for f in results.get("files", []):
        if f["mimeType"] == "application/vnd.google-apps.folder":
            print(f"{'  ' * depth}[Carpeta] {f['name']}")
            archivos.extend(
                listar_archivos_recursivo(drive_service, f["id"], depth + 1)
            )
        else:
            print(f"{'  ' * depth}{f['name']} ({f['mimeType'][:30]}...)")
            archivos.append(f)
    return archivos


def descargar_xlsx(drive_service, file_info):
    """Descarga un archivo XLSX de Drive y retorna un DataFrame."""
    file_id = file_info["id"]
    name = file_info["name"]
    mime = file_info["mimeType"]

    try:
        if "spreadsheet" in mime:
            # Es un Google Sheet - exportar como XLSX
            request = drive_service.files().export_media(
                fileId=file_id,
                mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            # Es un archivo normal - descargar
            request = drive_service.files().get_media(fileId=file_id)

        buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(buffer, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

        buffer.seek(0)
        # Intentar leer con diferentes headers
        for header_row in [5, 0, 1, 4]:
            try:
                df = pd.read_excel(buffer, header=header_row)
                df.columns = df.columns.str.strip()
                # Buscar columnas clave
                has_pub = any("publicaci" in c.lower() for c in df.columns)
                has_titulo = any("tulo" in c.lower() or "producto" in c.lower() for c in df.columns)
                has_total = any("total" in c.lower() or "neto" in c.lower() or "costo" in c.lower() for c in df.columns)
                if has_titulo and (has_total or has_pub):
                    return df
                buffer.seek(0)
            except Exception:
                buffer.seek(0)
                continue

        # Ultimo intento sin header especifico
        buffer.seek(0)
        return pd.read_excel(buffer)
    except Exception as e:
        print(f"  WARN: No se pudo leer {name}: {e}")
        return None


def extraer_productos(df, source_name):
    """Extrae productos unicos de un DataFrame de reporte."""
    productos = []

    # Buscar columnas relevantes
    cols = df.columns.tolist()
    pub_col = next((c for c in cols if "publicaci" in c.lower() and "#" in c), None)
    titulo_col = next(
        (c for c in cols if "tulo" in c.lower()),
        next((c for c in cols if "producto" in c.lower()), None),
    )
    total_col = next(
        (c for c in cols if c.strip() == "Total (MXN)"),
        next((c for c in cols if "neto" in c.lower()), None),
    )
    costo_col = next((c for c in cols if "costo" in c.lower()), None)
    qty_col = next(
        (c for c in cols if "unidades" in c.lower()),
        next((c for c in cols if "cantidad" in c.lower()), None),
    )

    if not titulo_col:
        return productos

    for _, r in df.iterrows():
        titulo = str(r.get(titulo_col, "")).strip()
        if not titulo or titulo == "nan":
            continue

        pub = str(r.get(pub_col, "")).strip() if pub_col else ""
        if pub == "nan":
            pub = ""

        neto = None
        if total_col:
            try:
                neto = float(r[total_col])
            except (ValueError, TypeError):
                pass

        costo = None
        if costo_col:
            try:
                costo = float(r[costo_col])
                if pd.isna(costo):
                    costo = None
            except (ValueError, TypeError):
                pass

        productos.append({
            "publicacion_ml": pub,
            "titulo": titulo,
            "neto": neto,
            "costo": costo,
            "fuente": source_name,
        })

    return productos


def consolidar_productos(todos_productos):
    """Consolida productos por publicacion_ml, usando el costo mas reciente."""
    por_pub = defaultdict(list)
    sin_pub = []

    for p in todos_productos:
        if p["publicacion_ml"]:
            por_pub[p["publicacion_ml"]].append(p)
        else:
            sin_pub.append(p)

    consolidado = {}
    for pub, entries in por_pub.items():
        # Usar el ultimo (mas reciente) que tenga costo
        con_costo = [e for e in entries if e["costo"] is not None]
        if con_costo:
            best = con_costo[-1]  # Ultimo = mas reciente
        else:
            best = entries[-1]
        consolidado[pub] = best

    return consolidado


def actualizar_sheet(sheets_service, catalogo_actual, productos_nuevos):
    """Agrega productos nuevos al Sheet y actualiza pub IDs faltantes."""
    # Leer productos actuales del sheet
    result = (
        sheets_service.spreadsheets()
        .values()
        .get(spreadsheetId=CATALOGO_SHEET_ID, range="Productos!A:K")
        .execute()
    )
    rows = result.get("values", [])
    headers = rows[0] if rows else []

    # Mapear pub IDs existentes
    pub_idx = headers.index("publicacion_ml") if "publicacion_ml" in headers else 7
    prod_idx = headers.index("producto") if "producto" in headers else 0
    costo_idx = headers.index("costo_actual") if "costo_actual" in headers else 4

    pubs_existentes = set()
    productos_existentes = {}
    for i, row in enumerate(rows[1:], start=2):
        pubs = row[pub_idx].split(",") if pub_idx < len(row) and row[pub_idx] else []
        for p in pubs:
            pubs_existentes.add(p.strip())
        nombre = row[prod_idx] if prod_idx < len(row) else ""
        productos_existentes[nombre.lower()] = i  # row number in sheet

    # Encontrar productos que necesitan pub ID actualizado
    actualizaciones_pub = []
    nuevos = []

    for pub, info in productos_nuevos.items():
        if pub in pubs_existentes:
            continue  # Ya existe

        # Buscar si el producto existe por nombre (sin pub ID)
        titulo_lower = info["titulo"].lower()
        matched = False
        for nombre, row_num in productos_existentes.items():
            if any(
                keyword in titulo_lower
                for keyword in nombre.lower().split()[:2]
                if len(keyword) > 3
            ):
                # Producto existe pero sin este pub ID - agregar
                actualizaciones_pub.append((row_num, pub, nombre))
                matched = True
                break

        if not matched:
            nuevos.append((pub, info))

    # Aplicar actualizaciones de pub IDs
    for row_num, pub, nombre in actualizaciones_pub:
        current_row = rows[row_num - 1] if row_num - 1 < len(rows) else []
        current_pubs = current_row[pub_idx] if pub_idx < len(current_row) else ""
        if current_pubs:
            new_pubs = f"{current_pubs},{pub}"
        else:
            new_pubs = pub
        sheets_service.spreadsheets().values().update(
            spreadsheetId=CATALOGO_SHEET_ID,
            range=f"Productos!{chr(65 + pub_idx)}{row_num}",
            valueInputOption="RAW",
            body={"values": [[new_pubs]]},
        ).execute()
        print(f"  Pub ID agregado: {pub} -> {nombre}")

    # Agregar productos completamente nuevos
    if nuevos:
        new_rows = []
        for pub, info in nuevos:
            titulo = info["titulo"]
            costo = info["costo"] if info["costo"] else ""
            # Intentar extraer marca y peso del titulo
            marca = titulo.split()[0] if titulo else ""
            new_rows.append([
                titulo,        # producto
                marca,         # marca
                "",            # peso_kg
                "",            # proveedor
                costo,         # costo_actual
                "",            # costo_anterior
                "2026-03-18",  # fecha_costo
                pub,           # publicacion_ml
                "perro",       # categoria (default)
                "TRUE",        # activo
                f"Importado de {info['fuente']}",  # notas
            ])

        sheets_service.spreadsheets().values().append(
            spreadsheetId=CATALOGO_SHEET_ID,
            range="Productos!A:K",
            valueInputOption="RAW",
            body={"values": new_rows},
        ).execute()
        print(f"  {len(new_rows)} productos nuevos agregados al Sheet")

    return len(actualizaciones_pub), len(nuevos)


def main():
    print("Autenticando...")
    creds = get_credentials()
    drive_service = build("drive", "v3", credentials=creds)
    sheets_service = build("sheets", "v4", credentials=creds)

    # 1. Listar archivos en carpeta de reportes historicos
    print(f"\nListando archivos en carpeta de reportes historicos...")
    archivos = listar_archivos_recursivo(drive_service, FOLDER_REPORTES)
    print(f"\nTotal archivos encontrados: {len(archivos)}")

    # 2. Tambien leer reportes locales
    todos_productos = []

    locales = list(PROJECT_ROOT.glob("Reporte_CroqueteriaGaby_*.xlsx"))
    print(f"\nReportes locales: {len(locales)}")
    for f in locales:
        df = pd.read_excel(str(f), sheet_name="Ventas")
        prods = extraer_productos(df, f.name)
        todos_productos.extend(prods)
        print(f"  {f.name}: {len(prods)} ventas")

    # 3. Descargar y procesar archivos de Drive
    xlsx_types = [
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel",
        "application/vnd.google-apps.spreadsheet",
    ]
    for archivo in archivos:
        if archivo["mimeType"] in xlsx_types or archivo["name"].endswith((".xlsx", ".xls")):
            print(f"\nProcesando: {archivo['name']}...")
            df = descargar_xlsx(drive_service, archivo)
            if df is not None:
                prods = extraer_productos(df, archivo["name"])
                todos_productos.extend(prods)
                print(f"  Extraidos: {len(prods)} productos")

    # 4. Consolidar
    print(f"\nTotal productos extraidos: {len(todos_productos)}")
    consolidado = consolidar_productos(todos_productos)
    print(f"Productos unicos por pub ID: {len(consolidado)}")

    for pub, info in sorted(consolidado.items()):
        c = f"${info['costo']}" if info["costo"] else "SIN COSTO"
        print(f"  {pub}: {info['titulo'][:50]} | {c}")

    # 5. Actualizar Sheet
    print(f"\nActualizando Catalogo Maestro...")
    n_actualizados, n_nuevos = actualizar_sheet(sheets_service, None, consolidado)

    print(f"\n{'='*60}")
    print(f"RESULTADO")
    print(f"{'='*60}")
    print(f"Productos analizados: {len(todos_productos)}")
    print(f"Publicaciones ML unicas: {len(consolidado)}")
    print(f"Pub IDs agregados a existentes: {n_actualizados}")
    print(f"Productos nuevos agregados: {n_nuevos}")


if __name__ == "__main__":
    main()
