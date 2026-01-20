# 🚀 Guía de Despliegue - Dashboard JCAS Chihuahua

## 📋 Tabla de Contenidos
1. [Preparación](#preparación)
2. [Subir a GitHub](#subir-a-github)
3. [Desplegar en Vercel](#desplegar-en-vercel)
4. [Verificación](#verificación)
5. [Solución de Problemas](#solución-de-problemas)

---

## ✅ Preparación

### Archivos Creados Automáticamente

El proyecto ya incluye todos los archivos necesarios:

- ✅ `requirements.txt` - Dependencias de Python
- ✅ `vercel.json` - Configuración de Vercel
- ✅ `.gitignore` - Archivos a ignorar en Git
- ✅ `README.md` - Documentación del proyecto
- ✅ `dashboard_jcas.py` - Aplicación principal (configurada para producción)

### 🔑 Credenciales Necesarias

**¡BUENAS NOTICIAS!** Este proyecto **NO requiere credenciales** de servicios externos:

- ❌ No usa APIs externas
- ❌ No requiere bases de datos externas
- ❌ No necesita servicios de autenticación
- ❌ No usa almacenamiento en la nube

✅ **Todo funciona con datos locales del archivo Excel**

---

## 📤 Subir a GitHub

### Paso 1: Inicializar Git (si no está inicializado)

```bash
cd c:\chihuahua
git init
```

### Paso 2: Crear repositorio en GitHub

1. Ve a https://github.com
2. Click en "New repository"
3. Nombre sugerido: `dashboard-jcas-chihuahua`
4. Descripción: "Dashboard Ejecutivo - Proyecto JCAS Chihuahua - Sistema Solar Fotovoltaico"
5. **Importante:** Deja el repositorio como **Privado** (datos confidenciales)
6. NO inicialices con README (ya lo tenemos)
7. Click "Create repository"

### Paso 3: Conectar y subir

```bash
# Agregar todos los archivos
git add .

# Crear commit inicial
git commit -m "Initial commit: Dashboard JCAS Chihuahua con modo oscuro"

# Conectar con GitHub (reemplaza TU_USUARIO y TU_REPO)
git remote add origin https://github.com/TU_USUARIO/dashboard-jcas-chihuahua.git

# Subir a GitHub
git branch -M main
git push -u origin main
```

### 🔒 Archivos Sensibles

El `.gitignore` ya está configurado para **NO subir**:
- Archivos temporales de Python
- Backups del código
- Archivos temporales de Excel
- Logs

**NOTA:** El archivo Excel con los datos **SÍ se subirá** porque es necesario para el dashboard.

---

## 🌐 Desplegar en Vercel

### Opción 1: Desde la Web (Recomendado)

#### Paso 1: Crear cuenta en Vercel

1. Ve a https://vercel.com
2. Click "Sign Up"
3. Usa tu cuenta de GitHub para registrarte
4. Autoriza a Vercel a acceder a tus repositorios

#### Paso 2: Importar Proyecto

1. En el dashboard de Vercel, click "Add New..."
2. Selecciona "Project"
3. Click "Import Git Repository"
4. Busca `dashboard-jcas-chihuahua`
5. Click "Import"

#### Paso 3: Configurar Proyecto

Vercel detectará automáticamente:
- ✅ Framework: Python
- ✅ Build Command: (automático)
- ✅ Output Directory: (automático)

**No necesitas configurar variables de entorno** (no hay credenciales)

#### Paso 4: Desplegar

1. Click "Deploy"
2. Espera 2-3 minutos
3. ¡Listo! Vercel te dará una URL como: `https://dashboard-jcas-chihuahua.vercel.app`

---

### Opción 2: Desde CLI

```bash
# Instalar Vercel CLI
npm i -g vercel

# Login
vercel login

# Desplegar
vercel --prod
```

---

## ⚠️ IMPORTANTE: Limitación de Vercel con Archivos Excel

### 🚨 Problema Potencial

Vercel tiene un límite de **50MB por archivo** y **100MB total** para el proyecto. El archivo Excel podría causar problemas si es muy grande.

### ✅ Soluciones Alternativas

Si Vercel rechaza el archivo Excel:

#### Solución 1: Convertir Excel a CSV/JSON (Recomendado)

Puedo crear un script que convierta el Excel a archivos JSON más pequeños que se cargarán más rápido.

#### Solución 2: Usar otro servicio

- **Render.com** - Sin límite de tamaño de archivos
- **Railway.app** - Más flexible con archivos
- **Heroku** - Clásico y confiable

#### Solución 3: Almacenar Excel externamente

- Google Drive + API
- AWS S3
- Dropbox

**¿Quieres que implemente alguna de estas soluciones ahora?**

---

## ✅ Verificación

Después del despliegue, verifica:

1. ✅ Dashboard carga correctamente
2. ✅ Modo oscuro activo
3. ✅ Dropdown de JMAS funciona
4. ✅ Todos los gráficos cargan
5. ✅ Navegación entre tabs funciona
6. ✅ Datos se muestran correctamente

---

## 🔧 Solución de Problemas

### Error: "Module not found"

**Solución:** Verifica que `requirements.txt` esté en la raíz del proyecto.

### Error: "File too large"

**Solución:** El archivo Excel es muy grande. Usa una de las soluciones alternativas mencionadas arriba.

### Error: "Application error"

**Solución:** 
1. Revisa los logs en Vercel Dashboard
2. Verifica que `server = app.server` esté en el código
3. Asegúrate que `vercel.json` esté configurado correctamente

### Dashboard carga pero sin datos

**Solución:** 
1. Verifica que el archivo Excel se haya subido a GitHub
2. Revisa la ruta del archivo en `cargar_datos_excel()`
3. Checa los logs de Vercel para errores de lectura

---

## 📊 Monitoreo

Vercel proporciona:
- 📈 Analytics de tráfico
- 🐛 Logs de errores en tiempo real
- ⚡ Métricas de rendimiento
- 🔄 Historial de despliegues

Accede desde: https://vercel.com/dashboard

---

## 🔄 Actualizaciones Futuras

Para actualizar el dashboard:

```bash
# Hacer cambios en el código
git add .
git commit -m "Descripción de cambios"
git push

# Vercel desplegará automáticamente
```

---

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs en Vercel Dashboard
2. Consulta la documentación de Vercel: https://vercel.com/docs
3. Verifica que todos los archivos estén en GitHub

---

**¡Buena suerte con el despliegue! 🚀**

