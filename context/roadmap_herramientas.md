# ROADMAP DE HERRAMIENTAS Y AMBIENTE
# De donde venimos, hacia donde vamos

## ESTADO ACTUAL (Mar 2026)
- Claude in Chrome: funciona pero LENTO, requiere que yo navegue manualmente
- Chat directo: el flujo principal por ahora (Bruno adjunta archivos en el chat)
- GitHub repo: contexto persistente entre sesiones
- Drive: organizacion de archivos, Claude no puede escribir directo aun

## SIGUIENTE NIVEL — CLAUDE EN TERMINAL (instalado por Bruno)
Ventajas vs Chrome:
- Claude puede ejecutar scripts directamente sin navegar la UI
- git push/pull sin abrir Codespace en el browser
- Procesar archivos locales sin subirlos al chat
- Mucho mas rapido que Chrome

Para el repo: Bruno puede dar acceso con:
  gh auth login  (si usa GitHub CLI)
  o generar un Personal Access Token en github.com/settings/tokens
  con permisos: repo (full), workflow

Claude Code en terminal puede entonces:
  - Leer y escribir archivos del repo directamente
  - Hacer commits y push automaticamente
  - Ejecutar scripts Python de procesamiento

## SIGUIENTE NIVEL — GOOGLE DRIVE MCP
Cuando este configurado:
- Claude mueve los reportes a la carpeta correcta AUTOMATICAMENTE
- Claude puede leer archivos directamente de Drive sin que Bruno los adjunte
- El flujo seria: Bruno descarga XLSX -> lo sube a Drive -> Claude lo procesa solo

Como configurar: conectar en claude.ai > Configuracion > Integraciones > Google Drive
(ya esta conectado parcialmente, necesitamos permisos de escritura)

## SIGUIENTE NIVEL — VENTAS DIRECTAS AUTOMATIZADAS
Opciones:
A) Bruno llena un Google Sheet simple con ventas del dia (producto, cantidad, precio)
   Claude lo lee cada manana y lo integra al reporte
B) Formulario de Google Forms para registrar ventas rapido desde el celular
C) Integracion con WhatsApp Business API (mas avanzado, fase posterior)

## SIGUIENTE NIVEL — ESTADO FINANCIERO AUTOMATICO
Con Drive MCP + terminal:
- Claude lee XLSX de ventas de Drive
- Claude lee registro de gastos de un Google Sheet
- Claude genera reporte completo sin intervencion manual
- Bruno solo revisa y aprueba el reporte

## PRIORIDAD DE SETUP (en orden)
1. INMEDIATO: Crear archivo maestro de costos (Bruno, 15 min)
2. ESTA SEMANA: Configurar permisos de terminal para Claude Code
3. ESTA SEMANA: Registrar gastos fijos (renta, sueldos) para el primer mes completo
4. PROXIMAS 2 SEMANAS: Google Drive MCP con permisos de escritura
5. PROXIMO MES: Sheet de ventas directas para canal local/WhatsApp

## FLEXIBILIDAD EN EL REPORTE DIARIO
El reporte del dia es VIVO hasta el cierre:
- Corte de madrugada: version preliminar (pocas ventas)
- Corte de 8-9am: version principal del dia anterior
- Cierre del dia: version final con TODO incluido:
  * Ventas ML del dia
  * Ventas directas del dia
  * Gastos del dia si los hubo
  * Compras a proveedores si las hubo
Bruno puede actualizarme con info adicional a lo largo del dia
y yo regenero el reporte con la version mas completa

## SOBRE TERMINAL VS CHROME
Terminal (Claude Code):
+ Rapido, no requiere navegar UI
+ Puede ejecutar codigo directamente
+ git integrado
- Bruno necesita tener Claude Code instalado y configurado
- Necesita Personal Access Token de GitHub

Chrome (Claude in Chrome):
+ Ya funciona
+ Puede interactuar con cualquier pagina web
- Lento por la navegacion visual
- Depende de que Chrome este abierto

RECOMENDACION: usar terminal para todo lo de repo/codigo,
Chrome solo cuando necesitemos interactuar con Drive o ML directamente.
