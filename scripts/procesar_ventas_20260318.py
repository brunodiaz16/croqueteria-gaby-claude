#!/usr/bin/env python3
"""Procesar ventas ML 2026-03-18 + compras Dartacan/Africa/Invet"""
import pandas as pd

FECHA = "2026-03-18"
XLSX_PATH = r"C:/Users/bruno/Desktop/Ventas de ML por dia/18 de Mar de 2026/20260318_Ventas_MX_Mercado_Libre_y_Mercado_Shops_2026-03-18_10-47hs_3068340101.xlsx"

# 1. LEER VENTAS
df = pd.read_excel(XLSX_PATH, header=5)
df.columns = df.columns.str.strip()
titulo_col = [c for c in df.columns if "tulo" in c.lower()][0]
pub_col = [c for c in df.columns if "publicaci" in c.lower() and "#" in c][0]

# 2. CATALOGO DE COSTOS (por publicacion ML)
costos = {
    "MLM2668236083": ("Silver Kan 25kg", None, "SIN COSTO"),
    "MLM4663694700": ("Ganador Premium 20kg", 990, "Dartacan"),
    "MLM4679794046": ("Maskottchen Premium 15kg", 525, "Africa"),
    "MLM4679897714": ("Maskottchen Premium 15kg", 525, "Africa"),
    "MLM2668456003": ("Chapetes 20kg (Amarillos)", 300, "Africa"),
    "MLM2743362281": ("LiveClear Gato 3.18kg (2x1.5)", 768.61, "Invet"),
    "MLM4680298954": ("Arena Scoop Away 19kg 2-Pack", 798, "Por confirmar"),
    "MLM4619784042": ("Pedigree 20kg Res/Veg", 725, "Dartacan"),
    "MLM4663526262": ("Dog Chow 25kg", 900, "Dartacan"),
    "MLM4619796770": ("Gatina 15kg", 495, "Dartacan"),
    "MLM2742754049": ("6 Latas ProPlan Gastro 380g", 420.01, "Invet"),
}

rows = []
for _, r in df.iterrows():
    pub = str(r[pub_col]).strip()
    prod, costo, prov = costos.get(pub, (r[titulo_col], None, "SIN COSTO"))
    neto = float(r["Total (MXN)"])
    qty = int(r["Unidades"])
    if costo is not None:
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
        "Producto": prod,
        "Publicacion": pub,
        "Unidades": qty,
        "Neto_ML": neto,
        "Costo": costo,
        "Ganancia": ganancia,
        "Margen_%": margen,
        "Semaforo": semaforo,
        "Proveedor": prov,
    })

ventas = pd.DataFrame(rows)

# 3. RESUMEN
con_costo = ventas[ventas["Costo"].notna()]
total_neto = ventas["Neto_ML"].sum()
total_costo = con_costo["Costo"].sum()
total_ganancia = con_costo["Ganancia"].sum()
neto_con_costo = con_costo["Neto_ML"].sum()
margen_prom = round(total_ganancia / neto_con_costo * 100, 1) if neto_con_costo > 0 else 0
ordenes = len(ventas)
unidades = int(ventas["Unidades"].sum())

resumen = pd.DataFrame([
    {"Metrica": "Fecha", "Valor": FECHA},
    {"Metrica": "Ordenes", "Valor": ordenes},
    {"Metrica": "Unidades", "Valor": unidades},
    {"Metrica": "Neto ML Total", "Valor": f"${total_neto:,.2f}"},
    {"Metrica": "Costo Total", "Valor": f"${total_costo:,.2f}"},
    {"Metrica": "Ganancia", "Valor": f"${total_ganancia:,.2f}"},
    {"Metrica": "Margen Promedio", "Valor": f"{margen_prom}%"},
    {"Metrica": "Productos SIN COSTO", "Valor": len(ventas[ventas["Semaforo"] == "SIN COSTO"])},
    {"Metrica": "Productos ROJO (<8%)", "Valor": len(ventas[ventas["Semaforo"].isin(["ROJO", "PERDIDA"])])},
    {"Metrica": "Productos AMARILLO (8-14%)", "Valor": len(ventas[ventas["Semaforo"] == "AMARILLO"])},
    {"Metrica": "Productos VERDE (>14%)", "Valor": len(ventas[ventas["Semaforo"] == "VERDE"])},
])

alertas = ventas[ventas["Semaforo"].isin(["ROJO", "PERDIDA", "SIN COSTO"])].copy()

# 4. COMPRAS
compra_dartacan = pd.DataFrame([
    {"Producto": "Ganador Premium Adulto 20kg", "Cantidad": 5, "Precio_Unit": 990, "Total": 4950},
    {"Producto": "Pedigree Adulto 20kg", "Cantidad": 2, "Precio_Unit": 725, "Total": 1450},
    {"Producto": "Dog Chow Adulto R/G 25kg", "Cantidad": 1, "Precio_Unit": 900, "Total": 900},
    {"Producto": "Gatina 15kg", "Cantidad": 1, "Precio_Unit": 495, "Total": 495},
])

compra_africa = pd.DataFrame([
    {"Producto": "Chapetes 20kg (Amarillos)", "Cantidad": 2, "Precio_Unit": 300, "Total": 600},
    {"Producto": "Maskottchen Premium 15kg (Meskuten cubito pm)", "Cantidad": 2, "Precio_Unit": 525, "Total": 1050},
])

compra_invet = pd.DataFrame([
    {"Producto": "Vet Diet Lata Canine Gastro 380g", "Cantidad": 6, "Precio_Unit": 70.00, "Total": 420.01},
])

# 5. GENERAR XLSX
reporte_path = f"Reporte_CroqueteriaGaby_{FECHA}.xlsx"
with pd.ExcelWriter(reporte_path, engine="openpyxl") as w:
    ventas.to_excel(w, sheet_name="Ventas", index=False)
    resumen.to_excel(w, sheet_name="Resumen", index=False)
    alertas.to_excel(w, sheet_name="Alertas", index=False)
    compra_dartacan.to_excel(w, sheet_name="Compra_Dartacan", index=False)
    compra_africa.to_excel(w, sheet_name="Compra_Africa", index=False)
    compra_invet.to_excel(w, sheet_name="Compra_Invet", index=False)
print(f"Generado: {reporte_path}")

dart_path = f"Compra_Dartacan_{FECHA}.xlsx"
with pd.ExcelWriter(dart_path, engine="openpyxl") as w:
    meta = pd.DataFrame([
        {"Campo": "Proveedor", "Valor": "Dartacan"},
        {"Campo": "Nota", "Valor": "#371"},
        {"Campo": "Fecha", "Valor": FECHA},
        {"Campo": "Total", "Valor": "$7,795.00"},
    ])
    meta.to_excel(w, sheet_name="Info", index=False)
    compra_dartacan.to_excel(w, sheet_name="Detalle", index=False)
print(f"Generado: {dart_path}")

precios = pd.DataFrame([
    {"Producto": "Chapetes 20kg (Amarillos)", "Costo": 300, "Proveedor": "Africa", "Actualizado": FECHA},
    {"Producto": "Chapetes Premium 18kg", "Costo": 410, "Proveedor": "Chapetes", "Actualizado": "2026-03-17"},
    {"Producto": "Maskottchen Premium 15kg", "Costo": 525, "Proveedor": "Africa", "Actualizado": FECHA},
    {"Producto": "Ganador Premium 20kg", "Costo": 990, "Proveedor": "Dartacan", "Actualizado": "2026-03-17"},
    {"Producto": "Pedigree 20kg Res/Veg", "Costo": 725, "Proveedor": "Dartacan", "Actualizado": "2026-03-17"},
    {"Producto": "Perron Adulto 25kg", "Costo": 535, "Proveedor": "Dartacan", "Actualizado": "2026-03-17"},
    {"Producto": "Dog Chow Adulto R/G 25kg", "Costo": 900, "Proveedor": "Dartacan", "Actualizado": FECHA},
    {"Producto": "Gatina 15kg", "Costo": 495, "Proveedor": "Dartacan", "Actualizado": FECHA},
    {"Producto": "LiveClear Gato 1.5kg (x2=3.18kg)", "Costo": 768.61, "Proveedor": "Invet", "Actualizado": FECHA},
    {"Producto": "Vet Diet Lata Canine Gastro 380g", "Costo": 70.00, "Proveedor": "Invet", "Actualizado": FECHA},
    {"Producto": "Arena Scoop Away 19kg 2-Pack", "Costo": 798, "Proveedor": "Por confirmar", "Actualizado": FECHA},
    {"Producto": "Silver Kan 25kg", "Costo": "SIN COSTO", "Proveedor": "???", "Actualizado": ""},
])
precios_path = f"Lista_Precios_Vigentes_{FECHA}.xlsx"
precios.to_excel(precios_path, index=False)
print(f"Generado: {precios_path}")

# 6. PRINT SUMMARY
print()
print("=" * 60)
print(f"RESUMEN VENTAS {FECHA}")
print("=" * 60)
print(f"Ordenes: {ordenes} | Unidades: {unidades}")
print(f"Neto ML:  ${total_neto:,.2f}")
print(f"Costo:    ${total_costo:,.2f}")
print(f"Ganancia: ${total_ganancia:,.2f}")
print(f"Margen:   {margen_prom}%")
print()
print("DETALLE POR VENTA:")
for _, v in ventas.iterrows():
    c = v["Costo"] if v["Costo"] is not None else "???"
    g = f"${v['Ganancia']:,.2f}" if v["Ganancia"] is not None else "???"
    m = f"{v['Margen_%']}%" if v["Margen_%"] is not None else "???"
    print(f"  {v['Semaforo']:10s} | {v['Producto']:35s} | Neto ${v['Neto_ML']:,.2f} | Costo {c} | Gan {g} | {m}")
print()
print("COMPRAS HOY:")
print(f"  Dartacan #371: $7,795.00")
print(f"  Africa:        $1,650.00")
print(f"  Invet #309372: $420.01")
print(f"  Total compras: $9,865.01")
