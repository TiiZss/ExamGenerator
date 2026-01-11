# 🚀 Auto-Inicio de Ollama - Nueva Funcionalidad

## 📝 Descripción

ExamGenerator ahora **inicia automáticamente el servidor Ollama** si no está corriendo, haciendo mucho más fácil el uso de IA local.

## ✨ Cómo Funciona

### Antes (Manual)
```bash
# Tenías que hacer esto primero:
ollama serve

# Y luego en otra terminal:
python qg.py documento.pdf --motor ollama
```

### Ahora (Automático) ⚡
```bash
# Solo ejecuta esto:
python qg.py documento.pdf --motor ollama

# Si Ollama no está corriendo, el script pregunta:
# "¿Quieres que intente iniciar Ollama automáticamente? (s/n):"
# 
# Responde 's' y:
# ✅ Inicia Ollama
# ✅ Espera a que esté listo
# ✅ Continúa automáticamente
```

## 🔧 Detalles Técnicos

### Funciones Añadidas en qg.py

1. **`check_ollama_running(ollama_url)`**
   - Verifica si Ollama responde en la URL especificada
   - Retorna `True` si está corriendo, `False` si no

2. **`start_ollama_server()`**
   - Detecta el sistema operativo (Windows/Linux/macOS)
   - Inicia Ollama usando el método apropiado:
     - **Windows**: Intenta `net start Ollama` o `ollama serve` en nueva consola
     - **Linux/macOS**: Ejecuta `ollama serve` en segundo plano
   - Espera hasta 30 segundos para que el servidor inicie
   - Muestra progreso cada 5 segundos

3. **`ensure_ollama_running(ollama_url)`**
   - Verifica si Ollama está corriendo
   - Si no está, pregunta al usuario si quiere iniciarlo
   - Llama a `start_ollama_server()` si el usuario acepta
   - Retorna `True` si Ollama está disponible, `False` si no

### Integración

La función `generate_questions_with_ollama()` ahora llama a `ensure_ollama_running()` antes de procesar:

```python
def generate_questions_with_ollama(...):
    # ... código de validación ...
    
    # NUEVO: Verificar y asegurar que Ollama esté corriendo
    if not ensure_ollama_running(ollama_url):
        return None
    
    # Continuar con la generación de preguntas
    # ...
```

## 📊 Flujo de Ejecución

```
Usuario ejecuta: python qg.py doc.pdf --motor ollama
                          ↓
        ¿Está Ollama corriendo?
                ↙              ↘
              SÍ               NO
               ↓                ↓
    Continuar normal    Preguntar al usuario
                              ↓
                   ¿Iniciar automáticamente?
                       ↙              ↘
                     SÍ               NO
                      ↓                ↓
              Iniciar Ollama    Mostrar error
                      ↓           y terminar
              Esperar 30s
                      ↓
            ¿Inició correctamente?
                ↙              ↘
              SÍ               NO
               ↓                ↓
    Continuar normal    Mostrar error
                           y terminar
```

## 🎯 Casos de Uso

### Caso 1: Primera Vez (Usuario Nuevo)
```bash
$ python qg.py apuntes.pdf --motor ollama

📄 Extrayendo texto del PDF: apuntes.pdf...
✅ Texto extraído exitosamente (2345 caracteres)
⚠️  Servidor Ollama no detectado en http://localhost:11434
¿Quieres que intente iniciar Ollama automáticamente? (s/n): s
🚀 Intentando iniciar el servidor Ollama...
⏳ Esperando a que Ollama inicie...
   Esperando... (5s)
✅ Servidor Ollama iniciado correctamente

🤖 Enviando texto a Ollama local (llama2)...
# Continúa normalmente...
```

### Caso 2: Ollama Ya Corriendo
```bash
$ python qg.py apuntes.pdf --motor ollama

📄 Extrayendo texto del PDF: apuntes.pdf...
✅ Texto extraído exitosamente (2345 caracteres)
✅ Servidor Ollama ya está corriendo en http://localhost:11434

🤖 Enviando texto a Ollama local (llama2)...
# Continúa normalmente...
```

### Caso 3: Usuario Prefiere Manual
```bash
$ python qg.py apuntes.pdf --motor ollama

📄 Extrayendo texto del PDF: apuntes.pdf...
✅ Texto extraído exitosamente (2345 caracteres)
⚠️  Servidor Ollama no detectado en http://localhost:11434
¿Quieres que intente iniciar Ollama automáticamente? (s/n): n
❌ No se puede continuar sin Ollama
   Inicia Ollama manualmente con: ollama serve
```

## 🔍 Detección por Sistema Operativo

### Windows
1. Intenta iniciar el servicio Windows: `net start Ollama`
2. Si falla, ejecuta `ollama serve` en nueva ventana de consola
3. Verifica cada segundo si el servidor responde

### Linux/macOS
1. Ejecuta `ollama serve` en segundo plano
2. Redirige stdout/stderr a /dev/null
3. Verifica cada segundo si el servidor responde

## ⚠️ Manejo de Errores

### Ollama No Instalado
```
❌ Error: Ollama no está instalado o no está en PATH
   Descarga Ollama desde: https://ollama.ai
```

### Timeout (30 segundos)
```
⚠️  Ollama no respondió en 30 segundos
```

### Error Durante Inicio
```
❌ Error al intentar iniciar Ollama: [detalles del error]
```

## 🛠️ Configuración Avanzada

### Servidor Remoto
Si usas Ollama en otra máquina, el auto-inicio no se ejecuta:

```bash
python qg.py doc.pdf --motor ollama --ollama_url http://192.168.1.100:11434
```

En este caso, el script solo verifica si el servidor remoto está disponible.

### Timeout Personalizable
Puedes modificar el timeout en el código (por defecto 30 segundos):

```python
# En start_ollama_server()
for i in range(30):  # <-- Cambiar este número
    time.sleep(1)
    if check_ollama_running(...):
        return True
```

## 📦 Dependencias Nuevas

```python
import subprocess  # Para ejecutar comandos del sistema
import time        # Para esperar a que Ollama inicie
import sys         # Para control de flujo
import platform    # Para detectar el SO
```

Todas estas son librerías estándar de Python, **no requieren instalación adicional**.

## 🧪 Testing

### Probar Auto-Inicio
```bash
# 1. Asegurarte de que Ollama NO esté corriendo
# Windows:
net stop Ollama

# Linux/macOS:
pkill ollama

# 2. Ejecutar qg.py
python qg.py documento.pdf --motor ollama

# 3. Responder 's' cuando pregunte
# 4. Verificar que inicie correctamente
```

### Probar Detección
```bash
# 1. Iniciar Ollama manualmente
ollama serve

# 2. En otra terminal, ejecutar
python qg.py documento.pdf --motor ollama

# 3. Debe detectar que ya está corriendo
# Salida esperada: "✅ Servidor Ollama ya está corriendo..."
```

## 📚 Archivos Modificados

1. **qg.py**
   - Añadidas 3 nuevas funciones
   - Modificada `generate_questions_with_ollama()`
   - Añadidos imports: `subprocess`, `time`, `sys`, `platform`

2. **test_setup.py**
   - Actualizado mensaje cuando Ollama no está corriendo
   - Añadido hint sobre auto-inicio

3. **OLLAMA_SETUP.md**
   - Nueva sección "⚡ Inicio Automático"
   - Actualizada sección de solución de problemas

4. **.github/copilot-instructions.md**
   - Documentada funcionalidad de auto-inicio
   - Actualizada arquitectura de Ollama

## 💡 Mejores Prácticas

1. **Primera vez**: Dejar que el script inicie Ollama automáticamente
2. **Uso frecuente**: Considerar dejar Ollama corriendo como servicio
3. **Desarrollo**: Iniciar Ollama manualmente para ver logs
4. **Producción**: Configurar Ollama como servicio del sistema

## 🎓 Ventajas

✅ **Experiencia de usuario mejorada** - Un comando menos que recordar
✅ **Menos fricción** - Especialmente útil para usuarios nuevos
✅ **Multiplataforma** - Funciona en Windows, Linux y macOS
✅ **Seguro** - Pregunta antes de iniciar, no lo hace sin permiso
✅ **Informativo** - Muestra progreso y mensajes claros
✅ **Robusto** - Maneja errores y timeouts correctamente

## 🔄 Compatibilidad

- ✅ Retrocompatible: Si prefieres iniciar Ollama manualmente, sigue funcionando
- ✅ No invasivo: Solo actúa si Ollama NO está corriendo
- ✅ Respeta configuración: Usa la URL personalizada si se proporciona
- ✅ No requiere dependencias extra: Solo librerías estándar de Python

---

**Versión**: 10.20260111.2
**Fecha**: 11 Enero 2026
**Característica**: Auto-inicio de Ollama
