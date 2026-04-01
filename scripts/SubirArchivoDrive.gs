// ============================================================
// SUBIR ARCHIVO A DRIVE — CROQUETERÍA GABY
// ============================================================
// SETUP:
//   1. script.google.com → Nuevo proyecto
//   2. Pegar este código
//   3. Implementar → Nueva implementación → App web
//      - Ejecutar como: Yo
//      - Quién tiene acceso: Cualquier persona (o solo tú)
//   4. Copiar la URL del web app
//   5. Usar esa URL para subir archivos vía POST
// ============================================================

// --- FOLDER IDs (de drive_folder_ids.md) ---
var FOLDERS = {
  ROOT:                    "1PKGCW_SxrnPVnzh6Ah5_cg8klPQ735bq",
  VENTAS_ABRIL:            "111MAHZeXpE0zT-sRK2DK_KgLSx0bl5bB",
  REPORTES_SEMANALES:      "1p6yZuGtwD_1nIRHyHJjnK8ah59U89h8J",
  COMPRAS_CHAPETES:        "1y4WRQB7G9mDvNSD65oqNPw44OwbqUfz-",
  COMPRAS_DARTACAN:        "10ihib3toJ3SeO6G1BdkaPcpg36YdVvOc",
  COMPRAS_INVET:           "1bwCiAbVIt3QhJmSclhtX5gIz1ENp81Mj",
  COMPRAS_COSTCO:          "1z4iGSk9-0ym9BV24D0tfHLwzugegJ172",
  NOTAS_PEDIDO:            "1BLwCScqPTmBiW4GPSZFdKKDWANqxlpE2",
  CATALOGO_PRECIOS:        "1uTeqMTUtzK-mLfT_LNEHAkns8Oc14yls",
  CONTROL_INVENTARIO:      "1_xb-szCE1bHVa5_SXq8_CmcFdlEOOBAs",
  ANALISIS_ESTRATEGIA:     "1B50RXBeCLe0LAayEzw4YhvUnA0L6pAAM",
  GENERADOS_CLAUDE_ABRIL:  "1Ge48lFJ0_ItBU3-MsFYN159mqPkiI06N",
  HISTORICO_PRECIOS:        "1WV5mFQEDLsfym3-VQiiTWTMniX7a22lj",
  LISTAS_PRECIOS_VIGENTES: "1KvJWSDh2xPIEBkfGI1LcB3K-ixsnZzGl"
};

// --- RUTEO POR PREFIJO (de drive_folder_ids.md → Convención de Nombres) ---
var ROUTING = [
  { prefix: "Reporte_CroqueteriaGaby_",  folderId: FOLDERS.GENERADOS_CLAUDE_ABRIL },
  { prefix: "Historico_de_Precios_",      folderId: FOLDERS.HISTORICO_PRECIOS },
  { prefix: "Lista_Precios_Vigentes_",    folderId: FOLDERS.LISTAS_PRECIOS_VIGENTES },
  { prefix: "Catalogo_Maestro_",          folderId: FOLDERS.CATALOGO_PRECIOS },
  { prefix: "Compra_Dartacan_",           folderId: FOLDERS.COMPRAS_DARTACAN },
  { prefix: "Compra_Chapetes_",           folderId: FOLDERS.COMPRAS_CHAPETES },
  { prefix: "Compra_Invet_",              folderId: FOLDERS.COMPRAS_INVET },
  { prefix: "Compra_Costco_",             folderId: FOLDERS.COMPRAS_COSTCO },
  { prefix: "Nota_Pedido_",               folderId: FOLDERS.NOTAS_PEDIDO },
  { prefix: "Reporte_Semanal_",           folderId: FOLDERS.REPORTES_SEMANALES },
  { prefix: "Inventario_",                folderId: FOLDERS.CONTROL_INVENTARIO },
  { prefix: "Analisis_",                  folderId: FOLDERS.ANALISIS_ESTRATEGIA }
];

// ============================================================
// WEB APP — POST endpoint
// ============================================================
// Recibe JSON con:
//   fileName:  nombre del archivo (ej: "Reporte_CroqueteriaGaby_2026-03-17.xlsx")
//   content:   contenido en base64
//   mimeType:  (opcional) MIME type, default application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
//   folderId:  (opcional) forzar carpeta destino, ignora ruteo automático
// ============================================================

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var fileName = data.fileName;
    var contentB64 = data.content;
    var mimeType = data.mimeType || detectMimeType(fileName);
    var forcedFolderId = data.folderId || null;

    if (!fileName || !contentB64) {
      return jsonResponse(400, { error: "Faltan campos: fileName y content son requeridos" });
    }

    // Determinar carpeta destino
    var targetFolderId = forcedFolderId || resolveFolder(fileName);
    var folder = DriveApp.getFolderById(targetFolderId);

    // Decodificar y crear archivo
    var blob = Utilities.newBlob(Utilities.base64Decode(contentB64), mimeType, fileName);

    // Si ya existe un archivo con ese nombre, reemplazarlo
    var existing = folder.getFilesByName(fileName);
    if (existing.hasNext()) {
      var oldFile = existing.next();
      oldFile.setTrashed(true);
    }

    var file = folder.createFile(blob);

    return jsonResponse(200, {
      ok: true,
      fileId: file.getId(),
      fileName: file.getName(),
      folder: folder.getName(),
      folderId: targetFolderId,
      url: file.getUrl()
    });

  } catch (err) {
    return jsonResponse(500, { error: err.message });
  }
}

// ============================================================
// GET endpoint — status / test
// ============================================================

function doGet(e) {
  var action = (e && e.parameter && e.parameter.action) ? e.parameter.action : "status";

  if (action === "status") {
    return jsonResponse(200, {
      ok: true,
      service: "Croquetería Gaby — Drive Upload",
      folders: Object.keys(FOLDERS).length,
      routes: ROUTING.length
    });
  }

  if (action === "list") {
    var folderId = e.parameter.folderId || FOLDERS.ROOT;
    var folder = DriveApp.getFolderById(folderId);
    var files = folder.getFiles();
    var result = [];
    while (files.hasNext()) {
      var f = files.next();
      result.push({ name: f.getName(), id: f.getId(), url: f.getUrl() });
    }
    return jsonResponse(200, { ok: true, folder: folder.getName(), files: result });
  }

  return jsonResponse(400, { error: "Acción no reconocida: " + action });
}

// ============================================================
// FUNCIONES AUXILIARES
// ============================================================

/** Determina la carpeta destino según el prefijo del nombre */
function resolveFolder(fileName) {
  for (var i = 0; i < ROUTING.length; i++) {
    if (fileName.indexOf(ROUTING[i].prefix) === 0) {
      return ROUTING[i].folderId;
    }
  }
  // Si no matchea ningún prefijo → carpeta raíz
  return FOLDERS.ROOT;
}

/** Detecta MIME type por extensión */
function detectMimeType(fileName) {
  var ext = fileName.split(".").pop().toLowerCase();
  var types = {
    xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    xls:  "application/vnd.ms-excel",
    csv:  "text/csv",
    pdf:  "application/pdf",
    json: "application/json",
    png:  "image/png",
    jpg:  "image/jpeg",
    jpeg: "image/jpeg"
  };
  return types[ext] || "application/octet-stream";
}

/** Respuesta JSON estándar */
function jsonResponse(code, payload) {
  return ContentService
    .createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON);
}

// ============================================================
// FUNCIÓN MANUAL — Para subir desde Apps Script directamente
// ============================================================
// Útil para testing o para llamar desde otro script.
// Ejemplo:
//   subirArchivo("Reporte_CroqueteriaGaby_2026-03-17.xlsx", blob);
// ============================================================

function subirArchivo(fileName, blob, forcedFolderId) {
  var targetFolderId = forcedFolderId || resolveFolder(fileName);
  var folder = DriveApp.getFolderById(targetFolderId);

  // Reemplazar si existe
  var existing = folder.getFilesByName(fileName);
  if (existing.hasNext()) {
    existing.next().setTrashed(true);
  }

  var file = folder.createFile(blob.setName(fileName));
  Logger.log("Subido: " + file.getName() + " → " + folder.getName() + " | " + file.getUrl());
  return file;
}

// ============================================================
// TEST — Ejecutar para verificar que los folder IDs son válidos
// ============================================================

function testFolders() {
  var errors = [];
  var keys = Object.keys(FOLDERS);
  for (var i = 0; i < keys.length; i++) {
    try {
      var folder = DriveApp.getFolderById(FOLDERS[keys[i]]);
      Logger.log("OK: " + keys[i] + " → " + folder.getName());
    } catch (err) {
      errors.push(keys[i] + ": " + err.message);
      Logger.log("ERROR: " + keys[i] + " → " + err.message);
    }
  }
  if (errors.length === 0) {
    Logger.log("Todos los folders OK");
  } else {
    Logger.log(errors.length + " errores encontrados");
  }
}

// ============================================================
// TEST — Subir archivo de prueba
// ============================================================

function testUpload() {
  var testContent = "Archivo de prueba - " + new Date().toISOString();
  var blob = Utilities.newBlob(testContent, "text/plain", "test_upload.txt");
  var file = subirArchivo("test_upload.txt", blob);
  Logger.log("Test OK: " + file.getUrl());
  // Limpiar
  file.setTrashed(true);
  Logger.log("Archivo de prueba eliminado");
}
