# Guia de Skills - Croqueteria Gaby

## Que son las Skills?

Las skills son **prompts guardados** que Claude Code ejecuta cuando escribes un comando. En vez de escribir "procesa las ventas de hoy, lee el xlsx, cruza costos, genera reporte..." cada vez, solo escribes:

```
/procesar-ventas C:\ruta\al\archivo.xlsx
```

Y Claude ya sabe exactamente que hacer porque las instrucciones estan escritas en un archivo `.md`.

## Donde viven?

```
.claude/commands/
  procesar-ventas.md
  registrar-compra.md
  reporte-semanal.md
  subir-drive.md
```

Cada archivo `.md` es una skill. El nombre del archivo = el nombre del comando.

## Como se usan?

**IMPORTANTE**: Las skills funcionan desde el **CLI de Claude Code** (la terminal), NO desde la extension de VSCode.

```bash
# 1. Abre terminal en el proyecto
cd C:\Users\bruno\Desktop\Projects\croqueteria-gaby-claude

# 2. Inicia Claude Code
claude

# 3. Escribe / y ve los comandos disponibles
/procesar-ventas
/registrar-compra
/reporte-semanal
/subir-drive
```

## Las 4 Skills del Proyecto

### /procesar-ventas

**Que hace**: Procesa el XLSX de ventas de Mercado Libre del dia.

**Ejemplo**:
```
/procesar-ventas C:\Users\bruno\Desktop\Ventas de ML por dia\18 de Mar de 2026\archivo.xlsx
```

**Lo que genera**:
- `Reporte_CroqueteriaGaby_2026-03-18.xlsx` (ventas + margenes + alertas)
- `data/importar_inventario_2026-03-18.csv` (para subir a la app)
- `Lista_Precios_Vigentes_2026-03-18.xlsx`

**Automaticamente**: Lee costos del Google Sheet, calcula margenes, aplica semaforo (verde/amarillo/rojo), actualiza bitacora, sube a Drive, commitea.

---

### /registrar-compra

**Que hace**: Registra una compra de proveedor desde foto de ticket.

**Ejemplo**:
```
/registrar-compra Dartacan
```
(Y adjuntas la foto del ticket)

**Lo que genera**:
- `Compra_Dartacan_2026-03-18.xlsx`
- Actualiza costos en Google Sheet y en CLAUDE.md

---

### /reporte-semanal

**Que hace**: Consolida los ultimos 7 dias de ventas.

**Ejemplo**:
```
/reporte-semanal
```

**Lo que genera**:
- `Reporte_Semanal_S12_2026.xlsx` con rankings, tendencias, recomendaciones de compra

---

### /subir-drive

**Que hace**: Sube los archivos XLSX/CSV generados a Google Drive.

**Ejemplo**:
```
/subir-drive
```

Los archivos se van automaticamente a la carpeta correcta de Drive segun el prefijo del nombre.

---

## Skill Creator (Avanzado)

Ya tienes instalado el **skill-creator** de Anthropic como plugin global. Es una skill que te ayuda a:

- **Crear skills nuevas** desde cero
- **Mejorar skills existentes** (analiza y sugiere mejoras)
- **Evaluar skills** (prueba si funcionan bien con diferentes prompts)
- **Optimizar triggers** (mejora la descripcion para que Claude la active correctamente)

Para usarlo, desde el CLI de Claude Code escribe:
```
/skill-creator
```

### Ejemplo: Crear una skill nueva
```
/skill-creator crea una skill que genere notas de pedido para proveedores
```

### Ejemplo: Mejorar una skill existente
```
/skill-creator mejora la skill procesar-ventas para que tambien genere un dashboard
```

---

## Como se estructura una skill?

Cada skill es un archivo markdown con esta estructura:

```markdown
---
description: Descripcion corta (lo que aparece en el menu de /)
---

## Argumentos
$ARGUMENTS
- Que recibe como input

## Contexto
- Datos que Claude necesita saber

## Instrucciones
1. Paso 1
2. Paso 2
3. ...

## Reglas
- Restricciones importantes
```

La **description** en el frontmatter es clave: es lo que Claude usa para decidir cuando activar la skill.

---

## Tips para mejorar skills

1. **Se especifico**: Mientras mas detalladas las instrucciones, mas consistente el resultado
2. **Incluye ejemplos**: Mostrar el output esperado ayuda mucho
3. **Define reglas claras**: Que hacer con casos especiales (producto sin costo, etc.)
4. **Itera**: Si algo no sale bien, edita la skill y prueba de nuevo
5. **Usa skill-creator**: Deja que Claude analice y mejore tus skills automaticamente
