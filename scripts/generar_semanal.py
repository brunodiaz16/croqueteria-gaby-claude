"""Genera Reporte_Semanal_S12_2026.xlsx consolidando datos de la semana 16-20 Mar 2026."""
import sys
from collections import defaultdict
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

sys.stdout.reconfigure(encoding="utf-8")

VERDE  = PatternFill("solid", fgColor="27AE60")
ROJO   = PatternFill("solid", fgColor="E74C3C")
AMARI  = PatternFill("solid", fgColor="F39C12")
HEADER = PatternFill("solid", fgColor="2C3E50")
SUBT   = PatternFill("solid", fgColor="34495E")
ALTROW = PatternFill("solid", fgColor="ECF0F1")
WH     = Font(bold=True, color="FFFFFF")
BLD    = Font(bold=True)
CTR    = Alignment(horizontal="center")


def sem_fill(m):
    if m is None: return PatternFill("solid", fgColor="BDC3C7")
    if m >= 14:   return VERDE
    if m >= 8:    return AMARI
    return ROJO


def sem_txt(m):
    if m is None: return "SIN COSTO"
    if m >= 14:   return f"VERDE {m:.1f}%"
    if m >= 8:    return f"AMARI {m:.1f}%"
    return f"ROJO {m:.1f}%"


def hdr_row(ws, row, cols, fill=HEADER, font=WH):
    for c, v in enumerate(cols, 1):
        cell = ws.cell(row, c, v)
        cell.fill = fill
        cell.font = font
        cell.alignment = CTR


# ── DATOS ──────────────────────────────────────────────────────────────────────

POR_DIA = [
    ("2026-03-17", 5,  4178.55,  793.55,  19.0, "Datos de bitacora (XLSX parcial)"),
    ("2026-03-18", 18, 14528.73, 1345.91,  9.3, "2x Silver Kan SIN COSTO"),
    ("2026-03-19", 14, 8845.96,  240.44,   2.7, "9 productos SIN COSTO - ganancia subestimada"),
    ("2026-03-20", 18, 14920.06, 1691.21, 11.3, "Kan Kan corregido a $380"),
]

# (producto, unidades, neto_total, costo_total, proveedor)
PRODUCTOS_RAW = [
    # 03-17
    ("Chapetes Premium 18kg",          1,  501.19,   410.00, "Chapetes"),
    ("Ganador Premium 20kg",           1, 1164.10,   990.00, "Dartacan"),
    ("Pedigree 20kg Res/Veg",          1,  777.98,   725.00, "Dartacan"),
    # 03-18
    ("Ganador Premium 20kg",           5, 5270.00,  4950.00, "Dartacan"),
    ("Maskottchen Premium 15kg",       2, 1434.00,  1050.00, "Chapetes"),
    ("Chapetes 20kg Amarillos",        2,  864.00,   600.00, "Chapetes"),
    ("LiveClear Gato 3.18kg",          2, 1596.00,  1537.22, "Invet"),
    ("Arena Scoop Away 19kg 2-Pack",   1,  895.97,   798.00, "Costco"),
    ("Pedigree 20kg Res/Veg",          2, 1556.00,  1450.00, "Dartacan"),
    ("Dog Chow Adulto 25kg",           1,  954.75,   900.00, "Dartacan"),
    ("Gatina 15kg",                    1,  523.67,   495.00, "Dartacan"),
    ("6 Latas ProPlan Gastro 380g",    1,  454.00,   418.55, "Invet"),
    ("Silver Kan 25kg",                2, 1966.00,     0.00, "Dartacan"),
    # 03-19
    ("Chapetes Premium 18kg",          1,  501.19,   410.00, "Chapetes"),
    ("Perron Adulto 25kg",             1,  558.00,   535.00, "Dartacan"),
    ("6 Latas ProPlan Gastro 380g",    1,  454.00,   418.55, "Invet"),
    ("Gatina 15kg",                    1,  523.67,   495.00, "Dartacan"),
    ("Ganador Premium 20kg",           1, 1054.00,   990.00, "Dartacan"),
    ("Silver Kan 25kg",                3, 1622.00,     0.00, "Dartacan"),
    ("Chapetes Gato/Varios SIN COSTO", 4, 2887.00,     0.00, "—"),
    ("Minino Sobres 24pz",             1,  224.00,     0.00, "Dartacan"),
    ("Campeon Adulto 25kg",            1,  754.30,     0.00, "Dartacan"),
    # 03-20
    ("Kan Kan 25kg",                   1,  622.51,   380.00, "Dartacan"),
    ("Campeon Adulto 25kg",            3, 2262.90,  2175.00, "Dartacan"),
    ("6 Latas ProPlan Gastro 380g",    1,  478.95,   418.55, "Invet"),
    ("Chapetes Premium 18kg",          1,  501.19,   410.00, "Chapetes"),
    ("Dog Chow Adulto 25kg",           2, 1909.50,  1800.00, "Dartacan"),
    ("Kirkland Salmon/Camote 15.87kg", 2, 2129.24,  1562.30, "Costco"),
    ("Perron X2 Costales 50kg",        4, 4599.04,  4280.00, "Dartacan"),
    ("Gatina 15kg",                    1,  523.67,   495.00, "Dartacan"),
    ("Arena Scoop Away 19kg 2-Pack",   1,  895.97,   798.00, "Costco"),
    ("Chapetes Super Premium Gato 5kg",1,  242.79,   185.00, "Chapetes"),
]

agg = defaultdict(lambda: {"u": 0, "neto": 0.0, "costo": 0.0, "prov": ""})
for prod, u, neto, costo, prov in PRODUCTOS_RAW:
    agg[prod]["u"]    += u
    agg[prod]["neto"] += neto
    agg[prod]["costo"] += costo
    if prov != "—":
        agg[prod]["prov"] = prov

total_ordenes = sum(d[1] for d in POR_DIA)
total_neto    = sum(d[2] for d in POR_DIA)
total_gan     = sum(d[3] for d in POR_DIA)
margen_pond   = total_gan / total_neto * 100

# ── WORKBOOK ──────────────────────────────────────────────────────────────────

wb = openpyxl.Workbook()

# ── HOJA 1: RESUMEN ───────────────────────────────────────────────────────────
ws1 = wb.active
ws1.title = "Resumen"
ws1.column_dimensions["A"].width = 30
ws1.column_dimensions["B"].width = 20

ws1.merge_cells("A1:D1")
ws1.merge_cells("A2:D2")
ws1["A1"] = "CROQUETERIA GABY - Reporte Semanal S12 2026"
ws1["A1"].font = Font(bold=True, size=14, color="2C3E50")
ws1["A2"] = "Semana 16 - 20 Marzo 2026  (4 dias con ventas)"
ws1["A2"].font = Font(italic=True, color="7F8C8D")

metricas = [
    ("Ordenes totales",      str(total_ordenes),            None),
    ("Neto total (MXN)",     f"${total_neto:,.2f}",         "27AE60"),
    ("Ganancia minima",      f"${total_gan:,.2f}",          "27AE60"),
    ("Margen minimo pond.",  f"{margen_pond:.1f}%",         "2980B9"),
    ("",                     "",                             None),
    ("NOTA",                 "Ganancia real > mostrada: 9 prods SIN COSTO en 03-19", "E67E22"),
]
for i, (lbl, val, color) in enumerate(metricas, 4):
    ws1.cell(i, 1, lbl).font = BLD
    cell = ws1.cell(i, 2, val)
    if color:
        cell.font = Font(bold=True, color=color)

# ── HOJA 2: POR DIA ───────────────────────────────────────────────────────────
ws2 = wb.create_sheet("Por_Dia")
for col, w in zip("ABCDEF", [14, 10, 16, 16, 12, 44]):
    ws2.column_dimensions[col].width = w

hdr_row(ws2, 1, ["Fecha", "Ordenes", "Neto MXN", "Ganancia", "Margen", "Notas"])
for i, (fecha, ords, neto, gan, marg, nota) in enumerate(POR_DIA, 2):
    ws2.cell(i, 1, fecha)
    ws2.cell(i, 2, ords).alignment = CTR
    ws2.cell(i, 3, f"${neto:,.2f}")
    ws2.cell(i, 4, f"${gan:,.2f}")
    c = ws2.cell(i, 5, f"{marg:.1f}%")
    c.fill = sem_fill(marg)
    c.font = Font(bold=True, color="FFFFFF")
    c.alignment = CTR
    ws2.cell(i, 6, nota).font = Font(italic=True, color="7F8C8D")

r = len(POR_DIA) + 2
hdr_row(ws2, r, [
    "TOTAL", str(total_ordenes),
    f"${total_neto:,.2f}", f"${total_gan:,.2f}",
    f"{margen_pond:.1f}%", "ganancia subestimada por SIN COSTO del 19",
], fill=SUBT)

# ── HOJA 3: TOP PRODUCTOS ─────────────────────────────────────────────────────
ws3 = wb.create_sheet("Top_Productos")
for col, w in zip("ABCDEF", [42, 8, 16, 16, 16, 18]):
    ws3.column_dimensions[col].width = w

hdr_row(ws3, 1, ["Producto", "Units", "Neto Total", "Costo Total", "Ganancia", "Semaforo"])
sorted_prods = sorted(agg.items(), key=lambda x: x[1]["neto"], reverse=True)
for i, (prod, d) in enumerate(sorted_prods, 2):
    n, c = d["neto"], d["costo"]
    gan = n - c if c else None
    m   = gan / n * 100 if gan is not None else None
    fill = ALTROW if i % 2 == 0 else PatternFill()
    ws3.cell(i, 1, prod).fill = fill
    ws3.cell(i, 2, d["u"]).alignment = CTR
    ws3.cell(i, 3, f"${n:,.2f}").fill = fill
    ws3.cell(i, 4, f"${c:,.2f}" if c else "SIN COSTO").fill = fill
    ws3.cell(i, 5, f"${gan:,.2f}" if gan is not None else "—").fill = fill
    cell = ws3.cell(i, 6, sem_txt(m))
    cell.fill = sem_fill(m)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.alignment = CTR

# ── HOJA 4: ALERTAS ───────────────────────────────────────────────────────────
ws4 = wb.create_sheet("Alertas")
for col, w in zip("ABCDEFG", [42, 8, 12, 12, 12, 14, 38]):
    ws4.column_dimensions[col].width = w

hdr_row(ws4, 1, ["Producto", "Units", "Neto/u", "Costo/u", "Margen", "Proveedor", "Accion sugerida"])

acciones = {
    "Campeon Adulto 25kg":        "Repreciar a ~$1,000 lista urgente",
    "LiveClear Gato 3.18kg":      "Repreciar a ~$1,090 lista urgente",
    "Gatina 15kg":                "Repreciar a ~$700 lista",
    "Perron Adulto 25kg":         "Repreciar a ~$735 lista",
    "Dog Chow Adulto 25kg":       "Repreciar a ~$1,230 lista",
    "Pedigree 20kg Res/Veg":      "Repreciar a ~$980 lista",
    "Ganador Premium 20kg":       "Repreciar a ~$1,350 lista",
    "Perron X2 Costales 50kg":    "Revisar precio paquete x2",
    "6 Latas ProPlan Gastro 380g":"Monitorear (margen limite)",
}

rojos = [
    (p, d) for p, d in agg.items()
    if d["costo"] > 0 and d["neto"] > 0
    and (d["neto"] - d["costo"]) / d["neto"] * 100 < 8
]
rojos.sort(key=lambda x: (x[1]["neto"] - x[1]["costo"]) / x[1]["neto"])

for i, (prod, d) in enumerate(rojos, 2):
    nu = d["neto"] / d["u"]
    cu = d["costo"] / d["u"]
    m  = (nu - cu) / nu * 100
    ws4.cell(i, 1, prod).font = BLD
    ws4.cell(i, 2, d["u"]).alignment = CTR
    ws4.cell(i, 3, f"${nu:,.2f}")
    ws4.cell(i, 4, f"${cu:,.2f}")
    c = ws4.cell(i, 5, f"{m:.1f}%")
    c.fill = ROJO
    c.font = Font(bold=True, color="FFFFFF")
    c.alignment = CTR
    ws4.cell(i, 6, d["prov"])
    ws4.cell(i, 7, acciones.get(prod, "Revisar precio")).font = Font(italic=True, color="C0392B")

# ── HOJA 5: COMPRAS SUGERIDAS ─────────────────────────────────────────────────
ws5 = wb.create_sheet("Compras_Sugeridas")
for col, w in zip("ABCD", [42, 12, 14, 42]):
    ws5.column_dimensions[col].width = w

hdr_row(ws5, 1, ["Producto", "Vendidos/sem", "Costo unit", "Notas"])

notas_r = {
    "Ganador Premium 20kg":        "7 vendidos - restock urgente (repreciar primero)",
    "Perron X2 Costales 50kg":     "4 paquetes - revisar margen antes de comprar",
    "Campeon Adulto 25kg":         "4 vendidos - margen critico 3.9% - REPRECIAR PRIMERO",
    "Chapetes Premium 18kg":       "3 vendidos - buen margen 18.2% - mantener stock",
    "Pedigree 20kg Res/Veg":       "3 vendidos - repreciar antes de restock",
    "Gatina 15kg":                 "3 vendidos - repreciar antes de restock",
    "Dog Chow Adulto 25kg":        "3 vendidos - repreciar antes de restock",
    "Maskottchen Premium 15kg":    "2 vendidos - buen margen 26.8%",
    "Kirkland Salmon/Camote 15.87kg": "2 vendidos Flex - buen margen 26.6%",
    "Arena Scoop Away 19kg 2-Pack":"2 vendidos - margen 10.9% ok",
    "LiveClear Gato 3.18kg":       "2 vendidos - margen critico 3.7% - REPRECIAR PRIMERO",
    "Silver Kan 25kg":             "5 vendidos SIN COSTO confirmado - registrar costo",
}

restock = [(p, d) for p, d in agg.items() if d["costo"] > 0]
restock.sort(key=lambda x: x[1]["u"], reverse=True)

for i, (prod, d) in enumerate(restock, 2):
    cu = d["costo"] / d["u"]
    ws5.cell(i, 1, prod)
    ws5.cell(i, 2, d["u"]).alignment = CTR
    ws5.cell(i, 3, f"${cu:,.2f}")
    nota = notas_r.get(prod, "Monitorear")
    c = ws5.cell(i, 4, nota)
    c.font = Font(italic=True, color="2C3E50")
    if "REPRECIAR" in nota or "critico" in nota:
        c.font = Font(italic=True, bold=True, color="C0392B")

# ── GUARDAR ───────────────────────────────────────────────────────────────────
out = Path("data/xlsx/Reporte_Semanal_S12_2026.xlsx")
out.parent.mkdir(parents=True, exist_ok=True)
wb.save(str(out))
print(f"Generado: {out}")
print(f"  {len(POR_DIA)} dias | {total_ordenes} ordenes | ${total_neto:,.2f} neto | ${total_gan:,.2f} ganancia minima | {margen_pond:.1f}% margen")
