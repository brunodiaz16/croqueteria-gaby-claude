# Cómo obtener credentials.json desde Google Cloud Console

## 1. Crear un proyecto

1. Ve a [console.cloud.google.com](https://console.cloud.google.com/)
2. Haz clic en el selector de proyectos (arriba a la izquierda) → **Nuevo proyecto**
3. Nombre: `CroqueteriaGaby` (o el que prefieras) → **Crear**
4. Asegúrate de tener seleccionado el proyecto recién creado

## 2. Habilitar la API de Google Drive

1. Ve a **APIs y servicios** → **Biblioteca**
2. Busca **Google Drive API**
3. Haz clic en **Habilitar**

## 3. Configurar pantalla de consentimiento OAuth

1. Ve a **APIs y servicios** → **Pantalla de consentimiento OAuth**
2. Selecciona **Externo** → **Crear**
3. Llena los campos obligatorios:
   - Nombre de la app: `CroqueteriaGaby`
   - Correo de asistencia: tu correo
   - Correo del desarrollador: tu correo
4. Haz clic en **Guardar y continuar**
5. En **Permisos**, agrega el scope: `https://www.googleapis.com/auth/drive.file`
6. **Guardar y continuar** hasta terminar
7. En **Usuarios de prueba**, agrega tu correo de Gmail → **Guardar**

## 4. Crear credenciales OAuth 2.0

1. Ve a **APIs y servicios** → **Credenciales**
2. Haz clic en **+ Crear credenciales** → **ID de cliente OAuth**
3. Tipo de aplicación: **App de escritorio**
4. Nombre: `CroqueteriaGaby Desktop`
5. Haz clic en **Crear**
6. En el diálogo que aparece, haz clic en **Descargar JSON**
7. Renombra el archivo descargado a `credentials.json`

## 5. Colocar el archivo

Mueve `credentials.json` a la raíz de este proyecto:

```
croqueteria-gaby-claude/
├── credentials.json   ← aquí
├── scripts/
├── data/
└── ...
```

> **Importante:** `credentials.json` contiene secretos. Asegúrate de que esté en `.gitignore` y nunca lo subas al repositorio.

## 6. Primera ejecución

La primera vez que ejecutes un script que use estas credenciales:

1. Se abrirá una ventana del navegador pidiendo autorización
2. Inicia sesión con la cuenta de Gmail que agregaste como usuario de prueba
3. Acepta los permisos
4. Se generará un archivo `token.json` automáticamente (tampoco debe subirse a git)
