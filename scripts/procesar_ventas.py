"""
Procesa ventas diarias de Mercado Libre.
Lee costos desde Google Sheet Catalogo_Maestro (fallback a costos.md).
Genera: Reporte XLSX, Lista Precios XLSX, CSV para app inventario.

Uso: python scripts/procesar_ventas.py <ruta-xlsx> [YYYY-MM-DD]
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.catalogo import leer_catalogo
from scripts.config import XLSX_DIR, DATA_DIR, BITACORA_PATH


def cargar_ventas(xlsx_path):
    """Lee el XLSX de ML (header en fila 6) y retorna DataFrame."""
    df = pd.read_excel(xlsx_path, header=5)
    df.columns = df.columns.str.strip()
    return df


def cruzar_costos(df, catalogo):
    """Cruza cada venta con el catalogo por publicacion ML."""
    titulo_col = next(c for c in df.columns if "tulo" in c.lower())
    pub_col = next(c for c in df.columns if "publicaci" in c.lower() and "#" in c)

    rows = []
    for _, r in df.iterrows():
        pub = str(r[pub_col]).strip()
        neto = float(r["Total (MXN)"])
        qty = int(r["Unidades"])

        info = catalogo.get(pub)
        if info:
            producto = info.get("producto", r[titulo_col])
            costo = info.get("costo_actual")
            proveedor = info.get("proveedor", "")
        else:
            producto = r[titulo_col]
            costo = None
            proveedor = "SIN COSTO"

        if costo is not None and costo > 0:
            ganancia = round(neto - costo, 2)
            margen = round((neto - costo) / neto * 100, 1)
            if margen < 0:
                semaforo = "PERDIDA"
            elif margen < 8:
                semaforo = "ROJO"
            elif margen <= 14:
                semaforo = "AMARILLO"
            else:
                semaforo = "VERDE"
        else:
            ganancia = None
            margen = None
            semaforo = "SIN COSTO"

        rows.append({
            "Producto": producto,
            "Publicacion": pub,
            "Unidades": qty,
            "Neto_ML": neto,
            "Costo": costo,
            "Ganancia": ganancia,
            "Margen_%": margen,
            "Semaforo": semaforo,
            "Proveedor": proveedor,
        })

    return pd.DataFrame(rows)


def generar_resumen(ventas, fecha):
    """Genera DataFrame de resumen."""
    con_costo = ventas[ventas["Costo"].notna() & (ventas["Costo"] > 0)]
    total_neto = ventas["Neto_ML"].sum()
    total_costo = con_costo["Costo"].sum()
    total_ganancia = con_costo["Ganancia"].sum()
    neto_cc = con_costo["Neto_ML"].sum()
    margen = round(total_ganancia / neto_cc * 100, 1) if neto_cc > 0 else 0

    return pd.DataFrame([
        {"Metrica": "Fecha", "Valor": fecha},
        {"Metrica": "Ordenes", "Valor": len(ventas)},
        {"Metrica": "Unidades", "Valor": int(ventas["Unidades"].sum())},
        {"Metrica": "Neto ML Total", "Valor": f"${total_neto:,.2f}"},
        {"Metrica": "Costo Total", "Valor": f"${total_costo:,.2f}"},
        {"Metrica": "Ganancia", "Valor": f"${total_ganancia:,.2f}"},
        {"Metrica": "Margen Promedio", "Valor": f"{margen}%"},
        {"Metrica": "SIN COSTO", "Valor": len(ventas[ventas["Semaforo"] == "SIN COSTO"])},
        {"Metrica": "ROJO (<8%)", "Valor": len(ventas[ventas["Semaforo"].isin(["ROJO", "PERDIDA"])])},
        {"Metrica": "AMARILLO (8-14%)", "Valor": len(ventas[ventas["Semaforo"] == "AMARILLO"])},
        {"Metrica": "VERDE (>14%)", "Valor": len(ventas[ventas["Semaforo"] == "VERDE"])},
    ])


def generar_csv_inventario(ventas, fecha):
    """Genera CSV para importar en la app de inventario."""
    con_costo = ventas[ventas["Costo"].notna() & (ventas["Costo"] > 0)].copy()
    csv_df = pd.DataFrame({
        "Titulo de la publicacion": con_costo["Producto"],
        "Cantidad": con_costo["Unidades"],
        "Neto_a_recibir_MXN": con_costo["Neto_ML"],
        "Por_Unidad": con_costo["Neto_ML"],
        "Costo_Unidad": con_costo["Costo"],
    })
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = DATA_DIR / f"importar_inventario_{fecha}.csv"
    csv_df.to_csv(csv_path, index=False)
    return str(csv_path)


def auto_bitacora(fecha, ventas):
    """Auto-append resumen del dia a context/bitacora.md."""
    con_costo = ventas[ventas["Costo"].notna() & (ventas["Costo"] > 0)]
    total_neto = ventas["Neto_ML"].sum()
    total_ganancia = con_costo["Ganancia"].sum()
    neto_cc = con_costo["Neto_ML"].sum()
    margen = round(total_ganancia / neto_cc * 100, 1) if neto_cc > 0 else 0
    ordenes = len(ventas)
    unidades = int(ventas["Unidades"].sum())

    rojos = ventas[ventas["Semaforo"].isin(["ROJO", "PERDIDA"])]
    sin_costo = ventas[ventas["Semaforo"] == "SIN COSTO"]

    alertas_str = ", ".join(
        f"{r['Producto'][:25]} {r['Margen_%']}%"
        for _, r in rojos.iterrows()
    ) if len(rojos) > 0 else "ninguna"

    pendientes_str = ", ".join(
        r["Producto"][:30] for _, r in sin_costo.iterrows()
    ) if len(sin_costo) > 0 else "ninguno"

    entry = f"""
## {fecha} - Reporte del dia
- {ordenes} ordenes, {unidades} unidades, ${total_neto:,.2f} neto, ${total_ganancia:,.2f} ganancia, margen {margen}%
- Alertas: {alertas_str}
- Pendientes sin costo: {pendientes_str}
"""

    if BITACORA_PATH.exists():
        content = BITACORA_PATH.read_text(encoding="utf-8")
        # Insertar despues del titulo
        marker = "# BITACORA CROQUETERIA GABY"
        if marker in content:
            content = content.replace(marker, marker + "\n" + entry, 1)
        else:
            content = entry + "\n" + content
        BITACORA_PATH.write_text(content, encoding="utf-8")
    else:
        BITACORA_PATH.write_text(f"# BITACORA CROQUETERIA GABY\n{entry}", encoding="utf-8")

    print(f"Bitacora actualizada: {fecha}")


def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/procesar_ventas.py <ruta-xlsx> [YYYY-MM-DD]")
        sys.exit(1)

    xlsx_path = sys.argv[1]
    fecha = sys.argv[2] if len(sys.argv) > 2 else date.today().isoformat()

    print(f"Procesando ventas: {fecha}")
    print(f"XLSX: {xlsx_path}")

    # 1. Leer catalogo
    print("\nLeyendo catalogo de costos...")
    catalogo = leer_catalogo()
    if catalogo:
        print(f"  {len(catalogo)} productos en catalogo")
    else:
        print("  WARN: Catalogo vacio, todos los productos saldran como SIN COSTO")

    # 2. Leer ventas
    print("\nLeyendo XLSX de ML...")
    df = cargar_ventas(xlsx_path)
    print(f"  {len(df)} ordenes encontradas")

    # 3. Cruzar costos
    ventas = cruzar_costos(df, catalogo)
    resumen = generar_resumen(ventas, fecha)
    alertas = ventas[ventas["Semaforo"].isin(["ROJO", "PERDIDA", "SIN COSTO"])]

    # 4. Generar Reporte XLSX
    XLSX_DIR.mkdir(parents=True, exist_ok=True)
    reporte_path = XLSX_DIR / f"Reporte_CroqueteriaGaby_{fecha}.xlsx"

    # Idempotencia: verificar si ya existe
    if reporte_path.exists():
        print(f"\nWARN: {reporte_path.name} ya existe.")
        resp = input("Sobreescribir? (s/N): ").strip().lower()
        if resp != "s":
            print("Cancelado.")
            return
    with pd.ExcelWriter(str(reporte_path), engine="openpyxl") as w:
        ventas.to_excel(w, sheet_name="Ventas", index=False)
        resumen.to_excel(w, sheet_name="Resumen", index=False)
        alertas.to_excel(w, sheet_name="Alertas", index=False)
    print(f"\nGenerado: {reporte_path.name}")

    # 5. Generar Lista Precios
    precios_rows = []
    seen = set()
    for _, v in ventas.iterrows():
        key = v["Producto"]
        if key not in seen:
            seen.add(key)
            precios_rows.append({
                "Producto": v["Producto"],
                "Costo": v["Costo"],
                "Proveedor": v["Proveedor"],
                "Actualizado": fecha,
            })
    precios_path = XLSX_DIR / f"Lista_Precios_Vigentes_{fecha}.xlsx"
    pd.DataFrame(precios_rows).to_excel(str(precios_path), index=False)
    print(f"Generado: {precios_path.name}")

    # 6. Generar CSV inventario
    csv_path = generar_csv_inventario(ventas, fecha)
    print(f"Generado: {Path(csv_path).name}")

    # 7. Imprimir resumen
    con_costo = ventas[ventas["Costo"].notna() & (ventas["Costo"] > 0)]
    total_neto = ventas["Neto_ML"].sum()
    total_ganancia = con_costo["Ganancia"].sum()
    neto_cc = con_costo["Neto_ML"].sum()
    margen = round(total_ganancia / neto_cc * 100, 1) if neto_cc > 0 else 0

    print()
    print("=" * 60)
    print(f"RESUMEN VENTAS {fecha}")
    print("=" * 60)
    print(f"Ordenes: {len(ventas)} | Unidades: {int(ventas['Unidades'].sum())}")
    print(f"Neto ML:  ${total_neto:,.2f}")
    print(f"Ganancia: ${total_ganancia:,.2f}")
    print(f"Margen:   {margen}%")
    print()

    if len(alertas) > 0:
        print("ALERTAS:")
        for _, a in alertas.iterrows():
            c = a["Costo"] if a["Costo"] is not None else "???"
            print(f"  {a['Semaforo']:10s} | {a['Producto'][:35]:35s} | Neto ${a['Neto_ML']:,.2f} | Costo {c}")
        print()

    # 8. Auto-append bitacora
    auto_bitacora(fecha, ventas)


if __name__ == "__main__":
    main()
