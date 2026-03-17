// CREAR CARPETAS DRIVE - CROQUETERIA GABY
// 1. script.google.com -> Nuevo proyecto
// 2. Pegar codigo -> Ejecutar crearEstructura
const ROOT = "1PKGCW_SxrnPVnzh6Ah5_cg8klPQ735bq";
function crearEstructura() {
  const root = DriveApp.getFolderById(ROOT);
  [["01 - Ventas por Dia",["2026-03","2026-04","2026-05"]],["02 - Reportes Semanales",["2026"]],["03 - Compras y Proveedores",[["Martacan",["2026-03","2026-04"]],["Chapetes",["2026-03","2026-04"]],["Invet",["2026-03","2026-04"]],["Costco",["2026-03","2026-04"]]]],["04 - Notas de Pedido",["2026-03","2026-04"]],["05 - Catalogo y Precios",["Maestro de Productos","Actualizaciones de Costos","Historico"]],["08 - Generados por Claude",["Reportes Diarios","Listas de Compra","SOPs y Guias","Dashboards"]]].forEach(([n,h])=>crearRec(root,n,h));
  Logger.log("Listo");
}
function crearRec(p,n,h){const e=p.getFoldersByName(n);const f=e.hasNext()?e.next():p.createFolder(n);if(Array.isArray(h))h.forEach(c=>Array.isArray(c)?crearRec(f,c[0],c[1]):crearRec(f,c,[]));}