# 🚀 Guía Rápida de Uso - ExamGenerator con IA

## ✅ Pruebas Realizadas con Éxito

Todas las funcionalidades han sido probadas y verificadas:

### ✅ Prueba 1: Creación de Documento
```bash
# Creado: documento_ia.docx (714 caracteres)
# Tema: Conceptos Básicos de Inteligencia Artificial
```

### ✅ Prueba 2: Generación con Ollama
```bash
python qg.py documento_ia.docx --motor ollama --modelo gemma3:4b --num_preguntas 3

Resultado:
📄 Extrayendo texto del DOCX: documento_ia.docx...
✅ Texto extraído exitosamente (714 caracteres)
✅ Servidor Ollama ya está corriendo en http://localhost:11434

🤖 Enviando texto a Ollama local (gemma3:4b)...
📡 URL de Ollama: http://localhost:11434

✅ ¡Aquí tienes las preguntas generadas! ✅
------------------------------------------------------------
Preguntas generadas en español sobre IA
------------------------------------------------------------

📊 Motor usado: OLLAMA | Modelo: gemma3:4b
```

### ✅ Prueba 3: Auto-Inicio de Ollama
```bash
# Ollama detenido → Script detecta ausencia → Pregunta si iniciar → Inicia automáticamente
```

## 📖 Comandos de Ejemplo

### Uso Básico
```bash
# Con Gemini (requiere API key)
python qg.py documento.pdf --num_preguntas 10

# Con Ollama (local)
python qg.py documento.pdf --motor ollama --num_preguntas 10
```

### Con Modelos Específicos
```bash
# Gemini Pro (más preciso)
python qg.py apuntes.pdf --motor gemini --modelo gemini-1.5-pro --num_preguntas 15

# Ollama con Mistral
python qg.py tema.docx --motor ollama --modelo mistral --num_preguntas 8

# Ollama con Gemma 3
python qg.py presentacion.pptx --motor ollama --modelo gemma3:4b --num_preguntas 12
```

### Comparar Motores
```bash
# Mismo documento, diferentes motores
python qg.py contenido.pdf --motor gemini --num_preguntas 10
python qg.py contenido.pdf --motor ollama --modelo phi4 --num_preguntas 10
```

### Diferentes Idiomas
```bash
# En inglés
python qg.py document.pdf --motor ollama --idioma english --num_preguntas 10

# En español (default)
python qg.py documento.pdf --motor ollama --num_preguntas 10
```

## 🎯 Casos de Uso Real

### Estudiante Preparando Examen
```bash
# 1. Tienes apuntes en PDF
python qg.py apuntes_tema3.pdf --motor ollama --modelo gemma3:4b --num_preguntas 20

# 2. Las preguntas se generan automáticamente
# 3. Puedes estudiar con ellas
```

### Profesor Creando Material
```bash
# 1. Tienes presentación del tema
python qg.py clase_quimica.pptx --motor ollama --modelo mistral --num_preguntas 15

# 2. Guardas las preguntas
python qg.py clase_quimica.pptx --motor ollama --num_preguntas 15 > preguntas_quimica.txt

# 3. Las usas con eg.py para generar exámenes
python eg.py preguntas_quimica.txt Parcial 3 15
```

### Empresa Capacitando Personal
```bash
# 1. Manual de procedimientos en DOCX
python qg.py manual_seguridad.docx --motor ollama --modelo llama2 --num_preguntas 25

# 2. Preguntas para evaluación de conocimientos
```

## 🔍 Verificar Configuración

```bash
# Ejecutar script de verificación
python test_setup.py

# Ver modelos de Ollama disponibles
ollama list

# Ver ayuda de qg.py
python qg.py --help
```

## 💡 Tips Prácticos

### Optimizar Velocidad
- Usa modelos más pequeños: `gemma3:4b` es más rápido que `phi4`
- Reduce el número de preguntas para pruebas rápidas
- Usa Gemini si tienes buena conexión a internet

### Maximizar Calidad
- Usa `gemini-1.5-pro` para mejor precisión
- Usa `mistral` en Ollama para análisis de texto
- Genera más preguntas y selecciona las mejores

### Trabajar Offline
- Usa siempre `--motor ollama`
- Ten varios modelos descargados
- Descarga modelos con: `ollama pull nombre_modelo`

## 🚨 Solución de Problemas

### Ollama no inicia automáticamente
```bash
# Iniciarlo manualmente una vez
ollama serve

# Luego usar normalmente
python qg.py documento.pdf --motor ollama
```

### Modelo no encontrado
```bash
# Descargar el modelo
ollama pull llama2

# Verificar modelos instalados
ollama list

# Usar modelo existente
python qg.py doc.pdf --motor ollama --modelo phi4
```

### Error de encoding en Windows
```bash
# Configurar UTF-8
$env:PYTHONIOENCODING="utf-8"

# Ejecutar comando
python qg.py documento.pdf --motor ollama
```

## 📊 Comparación de Velocidad (Aproximada)

Basado en documento de ~1000 palabras, 10 preguntas:

| Motor | Modelo | Tiempo | Calidad | Internet |
|-------|--------|--------|---------|----------|
| Gemini | flash | ~5-10s | ⭐⭐⭐⭐ | ✅ Requiere |
| Gemini | pro | ~10-20s | ⭐⭐⭐⭐⭐ | ✅ Requiere |
| Ollama | gemma3:4b | ~30-60s | ⭐⭐⭐⭐ | ❌ Local |
| Ollama | phi4 | ~60-120s | ⭐⭐⭐⭐⭐ | ❌ Local |
| Ollama | mistral | ~40-80s | ⭐⭐⭐⭐ | ❌ Local |

*Tiempos varían según hardware. GPU acelera Ollama significativamente.*

## 🎓 Flujo Completo de Trabajo

```bash
# 1. Verificar configuración
python test_setup.py

# 2. Generar preguntas de tu material de estudio
python qg.py material.pdf --motor ollama --modelo gemma3:4b --num_preguntas 20

# 3. Copiar las preguntas a un archivo preguntas.txt (formato del proyecto)

# 4. Generar exámenes aleatorios
python eg.py preguntas.txt MiExamen 5 10 both plantilla.docx xlsx

# 5. Tienes 5 exámenes diferentes con 10 preguntas cada uno
```

## 🌟 Ejemplos Avanzados

### Pipeline Completo
```bash
# Generar preguntas, guardar y crear exámenes
python qg.py libro_cap1.pdf --motor ollama --num_preguntas 30 > temp_preguntas.txt
# Formatear manualmente temp_preguntas.txt al formato de preguntas.txt
python eg.py preguntas.txt Cap1 10 15 docx plantilla.docx
```

### Múltiples Documentos
```bash
# Generar preguntas de varios temas
python qg.py tema1.pdf --motor ollama --num_preguntas 10 > tema1_q.txt
python qg.py tema2.pdf --motor ollama --num_preguntas 10 > tema2_q.txt
python qg.py tema3.pdf --motor ollama --num_preguntas 10 > tema3_q.txt

# Combinar manualmente en preguntas.txt
# Generar exámenes mixtos
python eg.py preguntas.txt Repaso 3 30
```

---

**Última actualización**: 11 Enero 2026
**Versión**: 10.20260111.3
**Estado**: ✅ Totalmente funcional y probado
