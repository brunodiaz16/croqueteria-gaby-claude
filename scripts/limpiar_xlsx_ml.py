# limpiar_xlsx_ml.py
# Uso: python limpiar_xlsx_ml.py ventas.xlsx
import sys, pandas as pd
from datetime import datetime
def run(path):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()
    df = df.rename(columns={"Titulo de la publicacion":"titulo","Cantidad":"qty","Neto a recibir":"neto","Por_Unidad":"neto_u","Costo_Unidad":"costo_u"})
    df["qty"] = pd.to_numeric(df.get("qty",0),errors="coerce").fillna(0)
    df["neto_u"] = pd.to_numeric(df.get("neto_u",0),errors="coerce").fillna(0)
    df["costo_u"] = pd.to_numeric(df.get("costo_u",0),errors="coerce").fillna(0)
    df["ganancia"] = (df["neto_u"]-df["costo_u"])*df["qty"]
    df["margen"] = df.apply(lambda r: round((r["neto_u"]-r["costo_u"])/r["neto_u"]*100,1) if r["neto_u"]>0 else 0,axis=1)
    df["alerta"] = df["margen"].apply(lambda m: "PERDIDA" if m<0 else ("BAJO" if m<8 else "OK"))
    out = f"Reporte_CroqueteriaGaby_{datetime.now().strftime(chr(37)+chr(89)+chr(45)+chr(37)+chr(109)+chr(45)+chr(37)+chr(100))}.xlsx"
    with pd.ExcelWriter(out) as w:
        df.to_excel(w,"Ventas",index=False)
        df.sort_values("margen").to_excel(w,"Margenes",index=False)
        df[df["margen"]<8].to_excel(w,"Alertas",index=False)
    print(f"Generado: {out}")
if __name__=="__main__": run(sys.argv[1])
