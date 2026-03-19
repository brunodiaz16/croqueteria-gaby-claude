# Guia de Archivos - Croqueteria Gaby

## Donde guardar cada cosa

### Archivos fuente (tu input)

```
C:\Users\bruno\CroqueteriaGaby\
  Ventas\
    2026-03\     <- XLSX descargados de Mercado Libre
    2026-04\     <- crear cada mes nuevo
  Tickets\
    2026-03\     <- fotos de tickets de proveedores
    2026-04\
```

**Regla**: Guardar el XLSX de ML y las fotos de tickets aqui ANTES de procesarlos.
Asi siempre tienes el original guardado y organizado por mes.

### Archivos generados (output de Claude)

```
croqueteria-gaby-claude\
  data\
    xlsx\        <- reportes XLSX temporales (se borran al subir a Drive)
    *.csv        <- CSVs de inventario temporales (se borran al subir a Drive)
```

Estos archivos son **temporales**. Despues de `/subir-drive --clean` se borran.
Los originales quedan en Google Drive en sus carpetas correspondientes.

### Archivos permanentes (contexto del negocio)

```
croqueteria-gaby-claude\
  context\
    bitacora.md    <- auto-generada por procesar_ventas.py
    costos.md      <- auto-generado desde Google Sheet
  CLAUDE.md        <- contexto principal del negocio
```

Estos SI se commitean al repo y persisten.

---

## Flujo diario recomendado

1. **Mañana (8am)**: Baja XLSX de ML -> guardalo en `CroqueteriaGaby\Ventas\2026-03\`
2. **Procesa**: `/procesar-ventas C:\Users\bruno\CroqueteriaGaby\Ventas\2026-03\archivo.xlsx`
3. **Sube**: `/subir-drive` (archivos se borran del repo)
4. **Si llegan Flex**: Baja XLSX actualizado, corre `/procesar-ventas` de nuevo (sobreescribe)
5. **Tickets**: Guarda fotos en `CroqueteriaGaby\Tickets\2026-03\`, corre `/registrar-compra`

---

## Portabilidad (mover a otra PC)

1. `git clone https://github.com/brunodiaz16/croqueteria-gaby-claude.git`
2. `pip install pandas openpyxl google-auth google-auth-oauthlib google-api-python-client`
3. Copiar `credentials.json` del proyecto de Google Cloud
4. Crear directorios: `mkdir -p CroqueteriaGaby/Ventas CroqueteriaGaby/Tickets`
5. Correr cualquier script -> se abre navegador para autenticar

Todo lo demas (Sheet, Drive, skills) funciona igual en cualquier PC.
