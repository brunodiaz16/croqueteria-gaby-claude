"""
Crea el Google Sheet 'Catalogo_Maestro' en Drive y lo puebla con datos iniciales.
Correr UNA VEZ. Después anotar el Sheet ID en CLAUDE.md y catalogo.py.

Uso: python scripts/crear_catalogo_maestro.py
"""

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
    "https://www.googleapis.com/auth/spreadsheets",
]

FOLDER_CATALOGO = "1uTeqMTUtzK-mLfT_LNEHAkns8Oc14yls"  # 05 - Catalogo y Precios


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


def main():
    creds = get_credentials()
    sheets_service = build("sheets", "v4", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)

    # 1. Crear el Sheet
    print("Creando Google Sheet 'Catalogo_Maestro'...")
    spreadsheet = (
        sheets_service.spreadsheets()
        .create(
            body={
                "properties": {"title": "Catalogo_Maestro"},
                "sheets": [
                    {"properties": {"title": "Productos"}},
                    {"properties": {"title": "Aliases"}},
                    {"properties": {"title": "Historial_Costos"}},
                ],
            }
        )
        .execute()
    )
    sheet_id = spreadsheet["spreadsheetId"]
    print(f"Sheet creado: {sheet_id}")

    # 2. Mover a la carpeta correcta en Drive
    file_info = drive_service.files().get(fileId=sheet_id, fields="parents").execute()
    prev_parents = ",".join(file_info.get("parents", []))
    drive_service.files().update(
        fileId=sheet_id,
        addParents=FOLDER_CATALOGO,
        removeParents=prev_parents,
        fields="id, parents",
    ).execute()
    print(f"Movido a carpeta 05 - Catalogo y Precios")

    # 3. Poblar hoja Productos
    productos_data = [
        [
            "producto",
            "marca",
            "peso_kg",
            "proveedor",
            "costo_actual",
            "costo_anterior",
            "fecha_costo",
            "publicacion_ml",
            "categoria",
            "activo",
            "notas",
        ],
        [
            "Chapetes 20kg (Amarillos)",
            "Chapetes",
            20,
            "Chapetes",
            300,
            "",
            "2026-03-18",
            "MLM2668456003",
            "perro",
            "TRUE",
            "Alias: Amarillos",
        ],
        [
            "Chapetes Premium 18kg",
            "Chapetes",
            18,
            "Chapetes",
            410,
            "",
            "2026-03-17",
            "",
            "perro",
            "TRUE",
            "REGLA: siempre 18kg, nunca 19kg",
        ],
        [
            "Maskottchen Premium 15kg",
            "Maskottchen",
            15,
            "Chapetes",
            525,
            "",
            "2026-03-18",
            "MLM4679794046,MLM4679897714",
            "perro",
            "TRUE",
            "Alias: Meskuten cubito pm",
        ],
        [
            "Ganador Premium Adulto 20kg",
            "Ganador",
            20,
            "Dartacan",
            990,
            895,
            "2026-03-17",
            "MLM4663694700",
            "perro",
            "TRUE",
            "Antes $895 estimado",
        ],
        [
            "Pedigree Adulto Res/Veg 20kg",
            "Pedigree",
            20,
            "Dartacan",
            725,
            840,
            "2026-03-17",
            "MLM4619784042",
            "perro",
            "TRUE",
            "Antes $840 estimado",
        ],
        [
            "Perron Adulto 25kg",
            "Perron",
            25,
            "Dartacan",
            535,
            "",
            "2026-03-17",
            "",
            "perro",
            "TRUE",
            "",
        ],
        [
            "Dog Chow Adulto R/G 25kg",
            "Dog Chow",
            25,
            "Dartacan",
            900,
            "",
            "2026-03-18",
            "MLM4663526262",
            "perro",
            "TRUE",
            "",
        ],
        [
            "Gatina 15kg",
            "Gatina",
            15,
            "Dartacan",
            495,
            "",
            "2026-03-18",
            "MLM4619796770",
            "gato",
            "TRUE",
            "",
        ],
        [
            "LiveClear Gato 1.5kg (x2=3.18kg)",
            "Pro Plan",
            3.18,
            "Invet",
            768.61,
            "",
            "2026-03-18",
            "MLM2743362281",
            "gato",
            "TRUE",
            "Costo = 2x $331.30 + IVA",
        ],
        [
            "Vet Diet Lata Canine Gastro 380g",
            "Pro Plan",
            0.38,
            "Invet",
            70.00,
            "",
            "2026-03-18",
            "",
            "perro",
            "TRUE",
            "Costo con IVA. Listing: 6 latas",
        ],
        [
            "6 Latas ProPlan Gastro 380g",
            "Pro Plan",
            2.28,
            "Invet",
            420.01,
            "",
            "2026-03-18",
            "MLM2742754049",
            "perro",
            "TRUE",
            "6x $70 c/u con IVA",
        ],
        [
            "Arena Scoop Away 19kg 2-Pack",
            "Scoop Away",
            38,
            "Costco",
            798,
            "",
            "2026-03-18",
            "MLM4680298954",
            "gato",
            "TRUE",
            "2-pack",
        ],
        [
            "Silver Kan 25kg",
            "Silver Kan",
            25,
            "",
            "",
            "",
            "",
            "MLM2668236083",
            "perro",
            "TRUE",
            "SIN COSTO - pendiente",
        ],
    ]

    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range="Productos!A1",
        valueInputOption="RAW",
        body={"values": productos_data},
    ).execute()
    print(f"Productos: {len(productos_data)-1} filas")

    # 4. Poblar hoja Aliases
    aliases_data = [
        ["alias", "producto", "proveedor"],
        ["Naranjas", "Chapetes Premium 18kg", "Chapetes"],
        ["Amarillos", "Chapetes 20kg (Amarillos)", "Chapetes"],
        ["Meskuten cubito pm", "Maskottchen Premium 15kg", "Chapetes"],
        ["20x0192x5", "Ganador Premium Adulto 20kg", "Dartacan"],
        ["20x0068x5", "Pedigree Adulto Res/Veg 20kg", "Dartacan"],
    ]

    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range="Aliases!A1",
        valueInputOption="RAW",
        body={"values": aliases_data},
    ).execute()
    print(f"Aliases: {len(aliases_data)-1} filas")

    # 5. Poblar hoja Historial_Costos
    historial_data = [
        ["fecha", "producto", "costo_anterior", "costo_nuevo", "proveedor", "fuente"],
        ["2026-03-17", "Ganador Premium Adulto 20kg", 895, 990, "Dartacan", "Nota Dartacan #363"],
        ["2026-03-17", "Pedigree Adulto Res/Veg 20kg", 840, 725, "Dartacan", "Nota Dartacan #363"],
        ["2026-03-17", "Perron Adulto 25kg", "", 535, "Dartacan", "Nota Dartacan #363"],
        ["2026-03-18", "Chapetes 20kg (Amarillos)", "", 300, "Chapetes", "Nota Chapetes (libreta Africa)"],
        ["2026-03-18", "Maskottchen Premium 15kg", "", 525, "Chapetes", "Nota Chapetes (libreta Africa)"],
        ["2026-03-18", "Dog Chow Adulto R/G 25kg", "", 900, "Dartacan", "Nota Dartacan #371"],
        ["2026-03-18", "Gatina 15kg", "", 495, "Dartacan", "Nota Dartacan #371"],
        ["2026-03-18", "LiveClear Gato 1.5kg (x2=3.18kg)", "", 768.61, "Invet", "Factura Invet #309372"],
        ["2026-03-18", "Vet Diet Lata Canine Gastro 380g", "", 70.00, "Invet", "Factura Invet #309372"],
        ["2026-03-18", "Arena Scoop Away 19kg 2-Pack", "", 798, "Costco", "Confirmado por Bruno"],
    ]

    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range="Historial_Costos!A1",
        valueInputOption="RAW",
        body={"values": historial_data},
    ).execute()
    print(f"Historial: {len(historial_data)-1} filas")

    # 6. Borrar hoja default "Sheet1" si existe
    try:
        sheet_metadata = sheets_service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        for s in sheet_metadata.get("sheets", []):
            if s["properties"]["title"] == "Sheet1":
                sheets_service.spreadsheets().batchUpdate(
                    spreadsheetId=sheet_id,
                    body={"requests": [{"deleteSheet": {"sheetId": s["properties"]["sheetId"]}}]},
                ).execute()
    except Exception:
        pass

    print()
    print("=" * 60)
    print("CATALOGO MAESTRO CREADO")
    print(f"Sheet ID: {sheet_id}")
    print(f"URL: https://docs.google.com/spreadsheets/d/{sheet_id}")
    print()
    print("SIGUIENTE PASO:")
    print(f"  1. Actualizar CATALOGO_SHEET_ID en scripts/catalogo.py")
    print(f"  2. Agregar Sheet ID a CLAUDE.md")
    print("=" * 60)


if __name__ == "__main__":
    main()
