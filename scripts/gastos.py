"""
Modulo para registrar y consultar gastos operativos en Google Sheet.
Hoja: "Gastos" en Catalogo_Maestro.

Uso:
  from scripts.gastos import registrar_gasto, leer_gastos_periodo
"""

from datetime import date, datetime

from scripts.catalogo import _get_sheets_service
from scripts.config import CATALOGO_SHEET_ID, CATEGORIAS_GASTOS


HOJA_GASTOS = "Gastos"
HEADERS_GASTOS = ["fecha", "categoria", "descripcion", "monto", "metodo_pago", "notas"]


def _ensure_hoja_gastos(service, sheet_id):
    """Crea la hoja Gastos si no existe."""
    meta = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    hojas = [s["properties"]["title"] for s in meta["sheets"]]
    if HOJA_GASTOS in hojas:
        return

    service.spreadsheets().batchUpdate(
        spreadsheetId=sheet_id,
        body={"requests": [{"addSheet": {"properties": {"title": HOJA_GASTOS}}}]},
    ).execute()

    # Escribir headers
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=f"{HOJA_GASTOS}!A1:F1",
        valueInputOption="RAW",
        body={"values": [HEADERS_GASTOS]},
    ).execute()
    print(f"  Hoja '{HOJA_GASTOS}' creada en Catalogo_Maestro")


def registrar_gasto(categoria, monto, descripcion="", metodo_pago="efectivo",
                    notas="", fecha=None, sheet_id=None):
    """Registra un gasto operativo en la hoja Gastos.

    Args:
        categoria: Una de CATEGORIAS_GASTOS
        monto: Monto en MXN (positivo)
        descripcion: Descripcion corta del gasto
        metodo_pago: efectivo, transferencia, tarjeta
        notas: Notas adicionales
        fecha: YYYY-MM-DD (default: hoy)
        sheet_id: Override del Sheet ID

    Returns:
        True si se registro correctamente
    """
    sid = sheet_id or CATALOGO_SHEET_ID
    if not sid:
        print("ERROR: CATALOGO_SHEET_ID no configurado")
        return False

    if categoria not in CATEGORIAS_GASTOS:
        print(f"ERROR: Categoria '{categoria}' no valida.")
        print(f"  Categorias: {', '.join(CATEGORIAS_GASTOS)}")
        return False

    if monto <= 0:
        print("ERROR: Monto debe ser positivo")
        return False

    fecha_str = fecha or date.today().isoformat()

    try:
        service = _get_sheets_service()
        _ensure_hoja_gastos(service, sid)

        row = [fecha_str, categoria, descripcion, monto, metodo_pago, notas]
        service.spreadsheets().values().append(
            spreadsheetId=sid,
            range=f"{HOJA_GASTOS}!A:F",
            valueInputOption="RAW",
            body={"values": [row]},
        ).execute()

        print(f"  Gasto registrado: {categoria} ${monto:,.2f} ({descripcion})")
        return True
    except Exception as e:
        print(f"ERROR registrando gasto: {e}")
        return False


def leer_gastos_periodo(fecha_inicio, fecha_fin=None, sheet_id=None):
    """Lee gastos de un periodo.

    Args:
        fecha_inicio: YYYY-MM-DD
        fecha_fin: YYYY-MM-DD (default: hoy)
        sheet_id: Override del Sheet ID

    Returns:
        list[dict]: Lista de gastos con keys de HEADERS_GASTOS
    """
    sid = sheet_id or CATALOGO_SHEET_ID
    if not sid:
        return []

    fecha_fin = fecha_fin or date.today().isoformat()

    try:
        service = _get_sheets_service()
        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=sid, range=f"{HOJA_GASTOS}!A:F")
            .execute()
        )
        rows = result.get("values", [])
        if len(rows) < 2:
            return []

        gastos = []
        for row in rows[1:]:
            if len(row) < 4:
                continue
            fecha_gasto = row[0]
            if fecha_gasto < fecha_inicio or fecha_gasto > fecha_fin:
                continue
            entry = {}
            for i, h in enumerate(HEADERS_GASTOS):
                entry[h] = row[i] if i < len(row) else ""
            try:
                entry["monto"] = float(entry["monto"])
            except (ValueError, TypeError):
                entry["monto"] = 0
            gastos.append(entry)

        return gastos
    except Exception as e:
        print(f"WARN: No se pudieron leer gastos: {e}")
        return []


def resumen_gastos(gastos):
    """Genera resumen por categoria.

    Args:
        gastos: Lista de dicts (output de leer_gastos_periodo)

    Returns:
        dict: {categoria: total_monto}, con key "TOTAL" para el total general
    """
    por_cat = {}
    total = 0
    for g in gastos:
        cat = g.get("categoria", "otro")
        monto = g.get("monto", 0)
        por_cat[cat] = por_cat.get(cat, 0) + monto
        total += monto

    por_cat["TOTAL"] = total
    return por_cat


if __name__ == "__main__":
    print("Categorias de gastos disponibles:")
    for c in CATEGORIAS_GASTOS:
        print(f"  - {c}")

    print("\nLeyendo gastos del mes...")
    hoy = date.today()
    inicio_mes = hoy.replace(day=1).isoformat()
    gastos = leer_gastos_periodo(inicio_mes)
    if gastos:
        res = resumen_gastos(gastos)
        print(f"\nGastos {inicio_mes} a {hoy.isoformat()}:")
        for cat, total in sorted(res.items()):
            if cat != "TOTAL":
                print(f"  {cat:20s}: ${total:,.2f}")
        print(f"  {'TOTAL':20s}: ${res['TOTAL']:,.2f}")
    else:
        print("  Sin gastos registrados este mes")
