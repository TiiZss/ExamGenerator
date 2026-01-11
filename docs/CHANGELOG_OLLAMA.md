# ✨ Nueva Funcionalidad: Soporte para IA Local con Ollama

## 📝 Resumen de Cambios

Se ha añadido soporte completo para **Ollama**, permitiendo generar preguntas usando IA local sin necesidad de conexión a internet ni API keys de pago.

## 🎯 Archivos Modificados

### 1. `qg.py` - Generador con IA
**Cambios principales:**
- ✅ Eliminados conflictos de merge (`<<<<<<< HEAD`)
- ✅ Añadida función `generate_questions_with_gemini()` - Motor Google Gemini
- ✅ Añadida función `generate_questions_with_ollama()` - Motor Ollama local
- ✅ Nuevos argumentos de línea de comandos:
  - `--motor`: Elegir entre `gemini` u `ollama`
  - `--modelo`: Especificar modelo (llama2, mistral, gemini-1.5-pro, etc.)
  - `--ollama_url`: URL personalizada del servidor Ollama
- ✅ Imports condicionales para mejor manejo de dependencias
- ✅ Mensajes de error mejorados en español

### 2. `requirements.txt` - Dependencias
**Cambios:**
- ✅ Añadido `requests>=2.31.0` para comunicación con Ollama
- ✅ Eliminados conflictos de merge

### 3. `.github/copilot-instructions.md` - Instrucciones para IA
**Nuevas secciones:**
- ✅ Documentación de arquitectura dual (Gemini + Ollama)
- ✅ Explicación de modelo de selección
- ✅ Ejemplos de uso de ambos motores
- ✅ Patrones de manejo de errores específicos de Ollama

### 4. `OLLAMA_SETUP.md` - Guía de Configuración (NUEVO)
**Contenido:**
- ✅ Guía completa de instalación de Ollama
- ✅ Instrucciones paso a paso por sistema operativo
- ✅ Ejemplos prácticos de uso
- ✅ Comparación Gemini vs Ollama
- ✅ Solución de problemas comunes
- ✅ Mejores prácticas

## 🚀 Cómo Usar las Nuevas Funcionalidades

### Opción 1: Google Gemini (Como antes)
```bash
# Configurar API key
$env:GOOGLE_API_KEY = "tu-api-key"

# Usar
python qg.py documento.pdf --num_preguntas 10
```

### Opción 2: Ollama Local (NUEVO)
```bash
# 1. Instalar Ollama desde https://ollama.ai

# 2. Iniciar servidor
ollama serve

# 3. Descargar modelo
ollama pull llama2

# 4. Usar con ExamGenerator
python qg.py documento.pdf --motor ollama --num_preguntas 10
```

## 🎨 Ejemplos Avanzados

### Comparar ambos motores
```bash
# Mismo documento con ambos motores
python qg.py tema.pdf --motor gemini --num_preguntas 10
python qg.py tema.pdf --motor ollama --modelo mistral --num_preguntas 10
```

### Usar modelo específico
```bash
# Gemini Pro (más preciso)
python qg.py doc.pdf --motor gemini --modelo gemini-1.5-pro

# Mistral (excelente para texto)
python qg.py doc.pdf --motor ollama --modelo mistral
```

### Servidor Ollama remoto
```bash
python qg.py doc.pdf --motor ollama --ollama_url http://192.168.1.100:11434
```

## 📊 Ventajas de Ollama

✅ **100% Privado** - Datos nunca salen de tu computadora
✅ **Gratuito** - Sin límites ni costos de API
✅ **Sin Internet** - Funciona completamente offline
✅ **Múltiples Modelos** - llama2, mistral, codellama, etc.
✅ **Open Source** - Transparencia total

## ⚠️ Consideraciones

### Ollama requiere:
- 8GB RAM mínimo (recomendado 16GB)
- 4-8GB de espacio en disco por modelo
- CPU moderna (GPU opcional pero acelera)

### Google Gemini requiere:
- Conexión a internet
- API key de Google AI
- Posibles costos según uso

## 🔧 Instalación de Dependencias

Si ya tienes el proyecto instalado, solo necesitas actualizar:

```bash
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # Linux/macOS

# Instalar nueva dependencia
pip install requests>=2.31.0

# O reinstalar todo
pip install -r requirements.txt
```

## 📚 Documentación

- **Guía de Ollama**: Ver `OLLAMA_SETUP.md`
- **Instrucciones AI**: Ver `.github/copilot-instructions.md`
- **README principal**: Ver `README.md` (sección qg.py)

## 🐛 Solución de Problemas

### Error: "No se puede conectar a Ollama"
```bash
# Asegurarse de que Ollama esté corriendo
ollama serve
```

### Error: "Modelo no encontrado"
```bash
# Descargar el modelo
ollama pull llama2
```

### Error: "Module 'requests' not found"
```bash
# Instalar requests
pip install requests
```

## 🎯 Próximos Pasos Recomendados

1. **Probar con Gemini** (si ya tienes API key):
   ```bash
   python qg.py preguntas.txt --motor gemini --num_preguntas 5
   ```

2. **Instalar y probar Ollama**:
   - Descargar desde https://ollama.ai
   - Seguir guía en `OLLAMA_SETUP.md`

3. **Comparar resultados** de ambos motores con el mismo documento

4. **Actualizar README.md** si quieres añadir más ejemplos

## 📝 Notas de Implementación

- **Compatibilidad**: Código retrocompatible, funciona sin cambios si solo usas Gemini
- **Imports condicionales**: El código verifica dependencias antes de importar
- **Manejo de errores**: Mensajes claros en español para ambos motores
- **Timeout**: 5 minutos para Ollama (configurable en código)
- **Default**: Gemini sigue siendo el motor por defecto para no romper scripts existentes

## 🔄 Migración desde Versión Anterior

Si usabas qg.py antes, **no necesitas cambiar nada**. Seguirá funcionando igual:

```bash
# Esto sigue funcionando exactamente igual
python qg.py documento.pdf --num_preguntas 10
```

Para usar Ollama, solo añade `--motor ollama`:

```bash
# Versión con Ollama
python qg.py documento.pdf --motor ollama --num_preguntas 10
```

---

**Versión**: 10.20260111 (11 Enero 2026)
**Autor**: Actualización por TiiZss
**Licencia**: GPL v3
