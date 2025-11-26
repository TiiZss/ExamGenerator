# 🎓 ExamGenerator: Generador Avanzado de Exámenes Aleatorios

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-GPL%20v3-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-9.20251125-orange.svg)](https://github.com/TiiZss/ExamGenerator)

Un sistema completo y profesional en Python para generar exámenes aleatorios con múltiples formatos de salida, plantillas personalizables y generación de preguntas asistida por IA.

## 🌟 **Características Principales**

### 📋 **Generador Principal (eg.py)**
- **🎲 Aleatorización Inteligente**: Mezclado de preguntas y opciones con semillas consistentes
- **📄 Múltiples Formatos**: Exportación en TXT, DOCX, o ambos simultáneamente
- **🎨 Sistema de Plantillas**: Soporte completo para plantillas DOCX con 15+ placeholders
- **📁 Organización Automática**: Creación de carpetas organizadas por tema de examen
- **📊 Respuestas Múltiples**: Exportación en Excel, CSV, HTML, y TXT
- **⏱️ Cálculo de Tiempo**: Estimación automática de duración del examen
- **🔧 Configuración Flexible**: Múltiples opciones de personalización

### 🤖 **Generador con IA (qg.py)**
- **🧠 Google Gemini Integration**: Generación automática de preguntas usando IA
- **📑 Múltiples Formatos**: Procesamiento de PDF, DOCX, y PPTX
- **🔍 Extracción Inteligente**: Análisis contextual de contenido
- **🔐 Seguridad**: Gestión segura de API keys

## 🚀 **Instalación y Configuración**

### **Requisitos del Sistema**
- Python 3.8 o superior
- PowerShell (Windows) o Terminal (Linux/macOS)

### **1. Instalación Automática**

#### **🪟 Windows**
```powershell
# Método 1: Script directo
powershell -ExecutionPolicy Bypass -File install.ps1

# Método 2: Si hay problemas de permisos
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install.ps1
```

#### **🐧 Linux / macOS**
```bash
# Método 1: Script completo (recomendado)
chmod +x install.sh
./install.sh

# Método 2: Script rápido
chmod +x quick_install.sh
./quick_install.sh

# Método 3: Con Make
make setup-linux

# Método 4: Script universal
chmod +x setup.sh
./setup.sh
```

### **2. Instalación Manual**

```bash
# Clonar repositorio
git clone https://github.com/TiiZss/ExamGenerator.git
cd ExamGenerator

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows:
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

### **3. Configuración para IA (Opcional)**

```bash
# Windows PowerShell
$env:GOOGLE_API_KEY = "tu-api-key-aqui"

# Linux/macOS
export GOOGLE_API_KEY="tu-api-key-aqui"

# Permanente en Windows
setx GOOGLE_API_KEY "tu-api-key-aqui"

# Permanente en Linux/macOS (añadir a ~/.bashrc o ~/.zshrc)
echo 'export GOOGLE_API_KEY="tu-api-key-aqui"' >> ~/.bashrc
```

## 📖 **Uso Detallado**

### **Generador Principal (eg.py)**

#### **Sintaxis Básica**
```bash
python eg.py <archivo_preguntas> <nombre_base> <num_examenes> <preguntas_por_examen> [formato] [plantilla] [formato_respuestas]
```

#### **Parámetros Disponibles**

| Parámetro | Descripción | Valores | Requerido |
|-----------|-------------|---------|-----------|
| `archivo_preguntas` | Archivo con las preguntas base | .txt | ✅ |
| `nombre_base` | Prefijo para archivos generados | Texto | ✅ |
| `num_examenes` | Cantidad de exámenes a generar | Número entero | ✅ |
| `preguntas_por_examen` | Preguntas por cada examen | Número entero | ✅ |
| `formato` | Formato de salida | `txt`, `docx`, `both` | ❌ (default: txt) |
| `plantilla` | Archivo de plantilla DOCX | .docx | ❌ |
| `formato_respuestas` | Formato de respuestas | `xlsx`, `csv`, `html`, `txt` | ❌ (default: xlsx) |

#### **Ejemplos de Uso**

```bash
# Básico - TXT simple
python eg.py preguntas.txt SOC 30 20

# DOCX con plantilla
python eg.py preguntas.txt "Final_Matematicas" 25 15 docx plantilla_examen.docx

# Múltiples formatos con respuestas en HTML
python eg.py preguntas.txt "Parcial_Historia" 40 12 both plantilla.docx html

# Solo DOCX con respuestas en CSV
python eg.py preguntas.txt "Evaluacion_Ciencias" 15 25 docx "" csv
```

#### **Placeholders para Plantillas**

Las plantillas DOCX pueden usar estos marcadores que serán reemplazados automáticamente:

| Placeholder | Descripción | Ejemplo |
|-------------|-------------|---------|
| `{{EXAM_NAME}}` | Nombre del examen | SOC |
| `{{EXAM_NUMBER}}` | Número del examen | 1, 2, 3... |
| `{{EXAM_TITLE}}` | Título completo | EXAMEN SOC 1 |
| `{{DATE}}` | Fecha actual | 25/11/2025 |
| `{{FULL_DATE}}` | Fecha completa | 25 de Noviembre de 2025 |
| `{{DAY}}` | Día | 25 |
| `{{MONTH}}` | Mes en español | Noviembre |
| `{{YEAR}}` | Año | 2025 |
| `{{NUM_QUESTIONS}}` | Número de preguntas | 20 |
| `{{EXAM_TIME}}` | Tiempo estimado | 20 minutos |
| `{{CONTENT}}` | Punto de inserción | (marca donde van las preguntas) |

### **Generador con IA (qg.py)**

#### **Sintaxis**
```bash
python qg.py <archivo_documento> [--num_preguntas N] [--idioma IDIOMA]
```

#### **Ejemplos**
```bash
# Generar 10 preguntas de un PDF
python qg.py documento.pdf

# Generar 20 preguntas en inglés de un DOCX
python qg.py presentacion.docx --num_preguntas 20 --idioma ingles

# Procesar PowerPoint con 15 preguntas
python qg.py slides.pptx --num_preguntas 15
```

## 📝 **Formato del Archivo de Preguntas**

El archivo de preguntas debe seguir este formato estructurado:

```
1. ¿Cuál es la capital de España?
A) París
B) Londres
C) Madrid
D) Roma
ANSWER: C

2. ¿Cuál es el resultado de 2 + 2?
A) 3
B) 4
C) 5
D) 6
ANSWER: B

```

### **Reglas Importantes**
- ✅ Cada pregunta en línea separada
- ✅ Opciones con formato `A)`, `B)`, `C)`, `D)`
- ✅ Respuesta con formato `ANSWER: X`
- ✅ **Línea en blanco** entre cada pregunta
- ✅ Codificación UTF-8

## 📁 **Estructura de Archivos Generados**

```
ExamGenerator/
├── Examenes_NombreExamen/           # Carpeta auto-generada
│   ├── examen_NombreExamen_1.txt    # Exámenes individuales
│   ├── examen_NombreExamen_1.docx
│   ├── respuestas_NombreExamen_completas.xlsx  # Todas las respuestas
│   ├── respuestas_NombreExamen_completas.html
│   └── ...
├── eg.py
├── qg.py
├── preguntas.txt
└── requirements.txt
```

## 🎨 **Características Avanzadas**

### **1. Respuestas en Excel Profesional**
- 📊 Formato tabular transpuesto (exámenes en filas, preguntas en columnas)
- 🎨 Estilos profesionales con colores corporativos
- 📋 Información completa del examen (fecha, tiempo, estadísticas)
- 📐 Ajuste automático de columnas

### **2. Respuestas HTML Responsivas**
- 💻 Diseño responsive para cualquier dispositivo
- 🎨 Interfaz moderna con CSS avanzado
- 📱 Optimizado para impresión y visualización
- 🔍 Tabla interactiva con hover effects

### **3. Sistema de Plantillas Avanzado**
- 📄 Soporte completo para plantillas institucionales
- 🔄 Reemplazo automático de 15+ variables
- 📅 Fechas en español con formato personalizable
- ⏰ Cálculo automático de tiempo de examen

### **4. Organización Inteligente**
- 📁 Creación automática de carpetas organizadas
- 🏷️ Nomenclatura consistente y profesional
- 📋 Un archivo maestro de respuestas por set de exámenes
- 🔄 Preservación de estructura para múltiples ejecuciones

## 🛠️ **Solución de Problemas**

### **Errores Comunes**

#### **Error de Importación - python-docx**
```bash
# Problema: ModuleNotFoundError: No module named 'docx'
pip install python-docx
```

#### **Error de Importación - openpyxl**
```bash
# Problema: No se puede crear Excel
pip install openpyxl
```

#### **Error de API Key - Google AI**
```bash
# Problema: Variable de entorno no configurada
# Windows:
$env:GOOGLE_API_KEY = "tu-api-key-de-google-ai"
# Linux/macOS:
export GOOGLE_API_KEY="tu-api-key-de-google-ai"
```

#### **Error de Política de Ejecución (Windows)**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### **Error de Permisos (Linux)**
```bash
chmod +x install.sh quick_install.sh setup.sh
```

### **Validaciones del Sistema**

El sistema incluye validaciones automáticas para:
- ✅ Formato correcto del archivo de preguntas
- ✅ Existencia de archivos de plantilla
- ✅ Parámetros de línea de comandos válidos
- ✅ Disponibilidad de dependencias opcionales
- ✅ Permisos de escritura en directorio de salida

## 🔧 **Scripts de Instalación Disponibles**

| Script | Plataforma | Descripción |
|--------|------------|-------------|
| `install.ps1` | Windows | Script completo para PowerShell |
| `install.sh` | Linux/macOS | Script completo con detección de distribución |
| `quick_install.sh` | Linux/macOS | Instalación rápida básica |
| `setup.sh` | Universal | Script que detecta el sistema operativo |
| `Makefile` | Linux/macOS | Para usuarios que prefieren make |

## 📊 **Casos de Uso**

### **🎓 Educación Formal**
- Generación masiva de exámenes para universidades
- Múltiples versiones para prevenir copias
- Formatos profesionales para impresión

### **🏢 Corporativo**
- Evaluaciones de capacitación empresarial
- Certificaciones internas
- Tests de competencias técnicas

### **📚 Autoevaluación**
- Generación personalizada para estudio
- Práctica con preguntas aleatorias
- Seguimiento de progreso

### **🔬 Investigación**
- Instrumentos de medición académica
- Estudios longitudinales
- Herramientas de evaluación estandarizada

## 🤝 **Contribuciones**

¡Las contribuciones son bienvenidas! Por favor:

1. 🍴 Fork el repositorio
2. 🌿 Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push a la rama (`git push origin feature/AmazingFeature`)
5. 🔄 Abre un Pull Request

## 📄 **Licencia**

Este proyecto está licenciado bajo la Licencia GPL v3.0 - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 **Autor**

**TiiZss** - [GitHub Profile](https://github.com/TiiZss)

## 🙏 **Agradecimientos**

- Google AI por la API de Gemini
- Comunidad de Python por las excelentes librerías
- Contribuidores y usuarios del proyecto

## 📈 **Estadísticas del Proyecto**

- 🎯 **Versión Actual**: 9.20251125
- 🐍 **Python**: 3.8+
- 📦 **Dependencias**: 6 principales
- 🌟 **Características**: 15+ funcionalidades avanzadas
- 📄 **Formatos Soportados**: 7 tipos diferentes
- 🔧 **Placeholders**: 15+ variables automáticas
- 🛠️ **Scripts de Instalación**: 5 diferentes opciones

---

⭐ **Si este proyecto te ha sido útil, no olvides darle una estrella en GitHub!**
=======
# 🎓 ExamGenerator: Generador Avanzado de Exámenes Aleatorios

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-GPL%20v3-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-9.20251125-orange.svg)](https://github.com/TiiZss/ExamGenerator)

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/donate/?business=AC5N3XX2KGY2S&no_recurring=0&item_name=Seguir+con+el+desarrollo+de+la+herramienta&currency_code=EUR)

Un sistema completo y profesional en Python para generar exámenes aleatorios con múltiples formatos de salida, plantillas personalizables y generación de preguntas asistida por IA.

## 🌟 **Características Principales**

### 📋 **Generador Principal (eg.py)**
- **🎲 Aleatorización Inteligente**: Mezclado de preguntas y opciones con semillas consistentes
- **📄 Múltiples Formatos**: Exportación en TXT, DOCX, o ambos simultáneamente
- **🎨 Sistema de Plantillas**: Soporte completo para plantillas DOCX con 15+ placeholders
- **📁 Organización Automática**: Creación de carpetas organizadas por tema de examen
- **📊 Respuestas Múltiples**: Exportación en Excel, CSV, HTML, y TXT
- **⏱️ Cálculo de Tiempo**: Estimación automática de duración del examen
- **🔧 Configuración Flexible**: Múltiples opciones de personalización

### 🤖 **Generador con IA (qg.py)**
- **🧠 Google Gemini Integration**: Generación automática de preguntas usando IA
- **📑 Múltiples Formatos**: Procesamiento de PDF, DOCX, y PPTX
- **🔍 Extracción Inteligente**: Análisis contextual de contenido
- **🔐 Seguridad**: Gestión segura de API keys

## 🚀 **Instalación y Configuración**

### **Requisitos del Sistema**
- Python 3.8 o superior
- PowerShell (Windows) o Terminal (Linux/macOS)

### **1. Instalación Automática**

#### **🪟 Windows**
```powershell
# Método 1: Script directo
powershell -ExecutionPolicy Bypass -File install.ps1

# Método 2: Si hay problemas de permisos
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install.ps1
```

#### **🐧 Linux / macOS**
```bash
# Método 1: Script completo (recomendado)
chmod +x install.sh
./install.sh

# Método 2: Script rápido
chmod +x quick_install.sh
./quick_install.sh

# Método 3: Con Make
make setup-linux

# Método 4: Script universal
chmod +x setup.sh
./setup.sh
```

### **2. Instalación Manual**

```bash
# Clonar repositorio
git clone https://github.com/TiiZss/ExamGenerator.git
cd ExamGenerator

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows:
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

### **3. Configuración para IA (Opcional)**

```bash
# Windows PowerShell
$env:GOOGLE_API_KEY = "tu-api-key-aqui"

# Linux/macOS
export GOOGLE_API_KEY="tu-api-key-aqui"

# Permanente en Windows
setx GOOGLE_API_KEY "tu-api-key-aqui"

# Permanente en Linux/macOS (añadir a ~/.bashrc o ~/.zshrc)
echo 'export GOOGLE_API_KEY="tu-api-key-aqui"' >> ~/.bashrc
```

## 📖 **Uso Detallado**

### **Generador Principal (eg.py)**

#### **Sintaxis Básica**
```bash
python eg.py <archivo_preguntas> <nombre_base> <num_examenes> <preguntas_por_examen> [formato] [plantilla] [formato_respuestas]
```

#### **Parámetros Disponibles**

| Parámetro | Descripción | Valores | Requerido |
|-----------|-------------|---------|-----------|
| `archivo_preguntas` | Archivo con las preguntas base | .txt | ✅ |
| `nombre_base` | Prefijo para archivos generados | Texto | ✅ |
| `num_examenes` | Cantidad de exámenes a generar | Número entero | ✅ |
| `preguntas_por_examen` | Preguntas por cada examen | Número entero | ✅ |
| `formato` | Formato de salida | `txt`, `docx`, `both` | ❌ (default: txt) |
| `plantilla` | Archivo de plantilla DOCX | .docx | ❌ |
| `formato_respuestas` | Formato de respuestas | `xlsx`, `csv`, `html`, `txt` | ❌ (default: xlsx) |

#### **Ejemplos de Uso**

```bash
# Básico - TXT simple
python eg.py preguntas.txt SOC 30 20

# DOCX con plantilla
python eg.py preguntas.txt "Final_Matematicas" 25 15 docx plantilla_examen.docx

# Múltiples formatos con respuestas en HTML
python eg.py preguntas.txt "Parcial_Historia" 40 12 both plantilla.docx html

# Solo DOCX con respuestas en CSV
python eg.py preguntas.txt "Evaluacion_Ciencias" 15 25 docx "" csv
```

#### **Placeholders para Plantillas**

Las plantillas DOCX pueden usar estos marcadores que serán reemplazados automáticamente:

| Placeholder | Descripción | Ejemplo |
|-------------|-------------|---------|
| `{{EXAM_NAME}}` | Nombre del examen | SOC |
| `{{EXAM_NUMBER}}` | Número del examen | 1, 2, 3... |
| `{{EXAM_TITLE}}` | Título completo | EXAMEN SOC 1 |
| `{{DATE}}` | Fecha actual | 25/11/2025 |
| `{{FULL_DATE}}` | Fecha completa | 25 de Noviembre de 2025 |
| `{{DAY}}` | Día | 25 |
| `{{MONTH}}` | Mes en español | Noviembre |
| `{{YEAR}}` | Año | 2025 |
| `{{NUM_QUESTIONS}}` | Número de preguntas | 20 |
| `{{EXAM_TIME}}` | Tiempo estimado | 20 minutos |
| `{{CONTENT}}` | Punto de inserción | (marca donde van las preguntas) |

### **Generador con IA (qg.py)**

#### **Sintaxis**
```bash
python qg.py <archivo_documento> [--num_preguntas N] [--idioma IDIOMA]
```

#### **Ejemplos**
```bash
# Generar 10 preguntas de un PDF
python qg.py documento.pdf

# Generar 20 preguntas en inglés de un DOCX
python qg.py presentacion.docx --num_preguntas 20 --idioma ingles

# Procesar PowerPoint con 15 preguntas
python qg.py slides.pptx --num_preguntas 15
```

## 📝 **Formato del Archivo de Preguntas**

El archivo de preguntas debe seguir este formato estructurado:

```
1. ¿Cuál es la capital de España?
A) París
B) Londres
C) Madrid
D) Roma
ANSWER: C

2. ¿Cuál es el resultado de 2 + 2?
A) 3
B) 4
C) 5
D) 6
ANSWER: B

```

### **Reglas Importantes**
- ✅ Cada pregunta en línea separada
- ✅ Opciones con formato `A)`, `B)`, `C)`, `D)`
- ✅ Respuesta con formato `ANSWER: X`
- ✅ **Línea en blanco** entre cada pregunta
- ✅ Codificación UTF-8

## 📁 **Estructura de Archivos Generados**

```
ExamGenerator/
├── Examenes_NombreExamen/           # Carpeta auto-generada
│   ├── examen_NombreExamen_1.txt    # Exámenes individuales
│   ├── examen_NombreExamen_1.docx
│   ├── respuestas_NombreExamen_completas.xlsx  # Todas las respuestas
│   ├── respuestas_NombreExamen_completas.html
│   └── ...
├── eg.py
├── qg.py
├── preguntas.txt
└── requirements.txt
```

## 🎨 **Características Avanzadas**

### **1. Respuestas en Excel Profesional**
- 📊 Formato tabular transpuesto (exámenes en filas, preguntas en columnas)
- 🎨 Estilos profesionales con colores corporativos
- 📋 Información completa del examen (fecha, tiempo, estadísticas)
- 📐 Ajuste automático de columnas

### **2. Respuestas HTML Responsivas**
- 💻 Diseño responsive para cualquier dispositivo
- 🎨 Interfaz moderna con CSS avanzado
- 📱 Optimizado para impresión y visualización
- 🔍 Tabla interactiva con hover effects

### **3. Sistema de Plantillas Avanzado**
- 📄 Soporte completo para plantillas institucionales
- 🔄 Reemplazo automático de 15+ variables
- 📅 Fechas en español con formato personalizable
- ⏰ Cálculo automático de tiempo de examen

### **4. Organización Inteligente**
- 📁 Creación automática de carpetas organizadas
- 🏷️ Nomenclatura consistente y profesional
- 📋 Un archivo maestro de respuestas por set de exámenes
- 🔄 Preservación de estructura para múltiples ejecuciones

## 🛠️ **Solución de Problemas**

### **Errores Comunes**

#### **Error de Importación - python-docx**
```bash
# Problema: ModuleNotFoundError: No module named 'docx'
pip install python-docx
```

#### **Error de Importación - openpyxl**
```bash
# Problema: No se puede crear Excel
pip install openpyxl
```

#### **Error de API Key - Google AI**
```bash
# Problema: Variable de entorno no configurada
# Windows:
$env:GOOGLE_API_KEY = "tu-api-key-de-google-ai"
# Linux/macOS:
export GOOGLE_API_KEY="tu-api-key-de-google-ai"
```

#### **Error de Política de Ejecución (Windows)**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### **Error de Permisos (Linux)**
```bash
chmod +x install.sh quick_install.sh setup.sh
```

### **Validaciones del Sistema**

El sistema incluye validaciones automáticas para:
- ✅ Formato correcto del archivo de preguntas
- ✅ Existencia de archivos de plantilla
- ✅ Parámetros de línea de comandos válidos
- ✅ Disponibilidad de dependencias opcionales
- ✅ Permisos de escritura en directorio de salida

## 🔧 **Scripts de Instalación Disponibles**

| Script | Plataforma | Descripción |
|--------|------------|-------------|
| `install.ps1` | Windows | Script completo para PowerShell |
| `install.sh` | Linux/macOS | Script completo con detección de distribución |
| `quick_install.sh` | Linux/macOS | Instalación rápida básica |
| `setup.sh` | Universal | Script que detecta el sistema operativo |
| `Makefile` | Linux/macOS | Para usuarios que prefieren make |

## 📊 **Casos de Uso**

### **🎓 Educación Formal**
- Generación masiva de exámenes para universidades
- Múltiples versiones para prevenir copias
- Formatos profesionales para impresión

### **🏢 Corporativo**
- Evaluaciones de capacitación empresarial
- Certificaciones internas
- Tests de competencias técnicas

### **📚 Autoevaluación**
- Generación personalizada para estudio
- Práctica con preguntas aleatorias
- Seguimiento de progreso

### **🔬 Investigación**
- Instrumentos de medición académica
- Estudios longitudinales
- Herramientas de evaluación estandarizada

## 🤝 **Contribuciones**

¡Las contribuciones son bienvenidas! Por favor:

1. 🍴 Fork el repositorio
2. 🌿 Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push a la rama (`git push origin feature/AmazingFeature`)
5. 🔄 Abre un Pull Request

## 📄 **Licencia**

Este proyecto está licenciado bajo la Licencia GPL v3.0 - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 **Autor**

**TiiZss** - [GitHub Profile](https://github.com/TiiZss)

## 🙏 **Agradecimientos**

- Google AI por la API de Gemini
- Comunidad de Python por las excelentes librerías
- Contribuidores y usuarios del proyecto

## 📈 **Estadísticas del Proyecto**

- 🎯 **Versión Actual**: 9.20251125
- 🐍 **Python**: 3.8+
- 📦 **Dependencias**: 6 principales
- 🌟 **Características**: 15+ funcionalidades avanzadas
- 📄 **Formatos Soportados**: 7 tipos diferentes
- 🔧 **Placeholders**: 15+ variables automáticas
- 🛠️ **Scripts de Instalación**: 5 diferentes opciones

---

⭐ **Si este proyecto te ha sido útil, no olvides darle una estrella en GitHub!**
