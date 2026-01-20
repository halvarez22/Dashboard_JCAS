# 🌟 Dashboard Ejecutivo - Proyecto JCAS Chihuahua

## 📊 Sistema de Generación de Energía Solar Fotovoltaica con BESS

Dashboard interactivo profesional para análisis y visualización del proyecto de inversión pública en infraestructura hidráulica para la Junta Central de Agua y Saneamiento (JCAS) de Chihuahua.

---

## ✨ Características

- 🌙 **Modo Oscuro Profesional** - Interfaz moderna y elegante
- 📊 **Análisis Interactivo** - Selección dinámica por JMAS (Juárez, Chihuahua, Cuauhtémoc, Parral)
- ⚡ **Diagnóstico Operativo** - Consumo energético, costos y eficiencia
- ☀️ **Dimensionamiento Solar** - Capacidad instalada y producción energética
- 💰 **Análisis Financiero** - Proyecciones a 15 años, CAPEX, flujo de caja
- 📈 **Comparativo de Escenarios** - Sin proyecto vs Con proyecto
- 🌿 **Impacto Ambiental** - Reducción de emisiones CO₂

---

## 🚀 Instalación Local

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. **Clonar el repositorio:**
```bash
git clone https://github.com/TU_USUARIO/dashboard-jcas-chihuahua.git
cd dashboard-jcas-chihuahua
```

2. **Crear entorno virtual (opcional pero recomendado):**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecutar el dashboard:**
```bash
python dashboard_jcas.py
```

5. **Abrir en navegador:**
```
http://localhost:8050
```

---

## 📦 Dependencias Principales

- **Dash** - Framework web para Python
- **Plotly** - Visualizaciones interactivas
- **Pandas** - Análisis de datos
- **Dash Bootstrap Components** - Componentes UI
- **OpenPyXL** - Lectura de archivos Excel

---

## 📁 Estructura del Proyecto

```
dashboard-jcas-chihuahua/
├── dashboard_jcas.py              # Aplicación principal
├── Área y energía para JCAS Chihuahua vs1.2.xlsx  # Datos del proyecto
├── requirements.txt               # Dependencias Python
├── vercel.json                    # Configuración Vercel
├── .gitignore                     # Archivos ignorados por Git
├── README.md                      # Este archivo
└── Marco Juridico Chihuahua/      # Documentación legal
```

---

## 🌐 Despliegue en Vercel

### Opción 1: Desde GitHub (Recomendado)

1. Sube el proyecto a GitHub
2. Ve a [Vercel](https://vercel.com)
3. Importa tu repositorio de GitHub
4. Vercel detectará automáticamente la configuración
5. ¡Despliega!

### Opción 2: CLI de Vercel

```bash
npm i -g vercel
vercel login
vercel --prod
```

---

## 📊 Datos del Proyecto

### KPIs Principales

- 💰 **Inversión Total:** $2,616 M MXN ($147.8 M USD)
- 💵 **Ahorro 15 años:** $11,055 M MXN
- 📈 **TIR Proyecto:** 18.5%
- ☀️ **Capacidad Solar:** 150.24 MWp + 109.2 MWh BESS

### JMAS Incluidas

1. **JMAS Juárez** - 65.37 MWp
2. **JMAS Chihuahua** - 61.39 MWp
3. **JMAS Cuauhtémoc** - 13.83 MWp
4. **JMAS Parral** - 9.66 MWp

---

## 🎨 Tecnologías

- **Backend:** Python 3.x, Dash, Flask
- **Frontend:** Plotly.js, Bootstrap, CSS3
- **Datos:** Pandas, NumPy, OpenPyXL
- **Despliegue:** Vercel

---

## 📝 Licencia

Este proyecto es confidencial y pertenece a la Junta Central de Agua y Saneamiento (JCAS) de Chihuahua.

---

## 👥 Contacto

Para más información sobre el proyecto, contactar a la JCAS de Chihuahua.

---

## 🔄 Actualizaciones

- **v1.0.0** (Enero 2026) - Lanzamiento inicial con modo oscuro profesional

---

**Desarrollado con ❤️ para JCAS Chihuahua**

