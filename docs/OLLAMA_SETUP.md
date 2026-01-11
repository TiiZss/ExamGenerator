# 🤖 Guía de Configuración de Ollama para ExamGenerator

## 📋 Descripción

ExamGenerator ahora soporta **dos motores de IA** para generar preguntas automáticamente:

1. **Google Gemini** (Nube) - Requiere API key y conexión a internet
2. **Ollama** (Local) - IA completamente local, privada y gratuita

## 🚀 Configuración Rápida de Ollama

### Paso 1: Instalar Ollama

#### Windows
```powershell
# Descargar desde https://ollama.ai y ejecutar el instalador
# O usar winget:
winget install Ollama.Ollama
```

#### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### macOS
```bash
# Descargar desde https://ollama.ai
# O usar brew:
brew install ollama
```

### Paso 2: Iniciar el Servidor

```bash
ollama serve
```

El servidor se iniciará en `http://localhost:11434`

### Paso 3: Descargar Modelos

```bash
# Modelo recomendado para empezar (rápido y eficiente)
ollama pull llama2

# Otros modelos excelentes:
ollama pull mistral      # Muy bueno para análisis de texto
ollama pull codellama    # Especializado en contenido técnico
ollama pull llama2:13b   # Más preciso pero más pesado
```

### Paso 4: Verificar Instalación

```bash
# Listar modelos instalados
ollama list

# Probar un modelo
ollama run llama2 "Hola, ¿cómo estás?"
```

## 📖 Uso con ExamGenerator

### ⚡ Inicio Automático (NUEVO)

**ExamGenerator ahora puede iniciar Ollama automáticamente** si no está corriendo. Simplemente ejecuta:

```bash
python qg.py documento.pdf --motor ollama
```

Si Ollama no está corriendo, el script te preguntará:
```
⚠️  Servidor Ollama no detectado en http://localhost:11434
¿Quieres que intente iniciar Ollama automáticamente? (s/n):
```

Responde `s` y el script:
1. ✅ Iniciará Ollama automáticamente
2. ✅ Esperará a que esté listo
3. ✅ Continuará con la generación de preguntas

### Sintaxis Completa

```bash
python qg.py <archivo> [opciones]

Opciones:
  --num_preguntas N     Número de preguntas a generar (default: 10)
  --idioma IDIOMA       Idioma (default: español)
  --motor MOTOR         Motor: gemini u ollama (default: gemini)
  --modelo MODELO       Modelo específico
  --ollama_url URL      URL del servidor Ollama (default: http://localhost:11434)
```

### Ejemplos Prácticos

#### Ejemplo 1: Uso Básico
```bash
# Generar 10 preguntas de un PDF usando Ollama
python qg.py documento.pdf --motor ollama
```

#### Ejemplo 2: Especificar Modelo
```bash
# Usar Mistral para mejor calidad
python qg.py apuntes.pdf --motor ollama --modelo mistral --num_preguntas 15
```

#### Ejemplo 3: Procesar PowerPoint
```bash
# Generar preguntas de una presentación
python qg.py presentacion.pptx --motor ollama --modelo llama2 --num_preguntas 20
```

#### Ejemplo 4: Servidor Ollama Remoto
```bash
# Conectar a un servidor Ollama en otra máquina
python qg.py documento.pdf --motor ollama --ollama_url http://192.168.1.100:11434
```

#### Ejemplo 5: Comparar Motores
```bash
# Con Gemini (nube)
python qg.py tema.pdf --motor gemini --num_preguntas 10

# Con Ollama (local)
python qg.py tema.pdf --motor ollama --num_preguntas 10
```

## 🎯 Modelos Recomendados por Caso de Uso

| Caso de Uso | Modelo Recomendado | Comando |
|-------------|-------------------|---------|
| General / Rápido | `llama2` | `ollama pull llama2` |
| Mejor Calidad | `mistral` | `ollama pull mistral` |
| Contenido Técnico | `codellama` | `ollama pull codellama` |
| Más Precisión | `llama2:13b` | `ollama pull llama2:13b` |
| Multilingüe | `mixtral` | `ollama pull mixtral` |

## ⚙️ Requisitos del Sistema

### Para Ollama
- **RAM**: Mínimo 8GB (recomendado 16GB)
- **Espacio en Disco**: 
  - llama2: ~4GB
  - mistral: ~4GB
  - llama2:13b: ~8GB
- **CPU/GPU**: Funciona con CPU, GPU acelera la generación

### Para ExamGenerator
```bash
pip install requests>=2.31.0
```

## 🔧 Solución de Problemas

### Error: "No se puede conectar a Ollama"

**Problema**: `❌ Error: No se puede conectar a Ollama en http://localhost:11434`

**Solución Automática** (NUEVO):
```bash
# El script te preguntará si quieres iniciar Ollama automáticamente
# Solo responde 's' cuando aparezca el mensaje
python qg.py documento.pdf --motor ollama
```

**Solución Manual**:
```bash
# Verificar que Ollama esté ejecutándose
ollama serve

# En otra terminal, verificar que responde
curl http://localhost:11434/api/tags
```

### Error: "Modelo no encontrado"

**Problema**: El modelo especificado no existe

**Solución**:
```bash
# Listar modelos disponibles
ollama list

# Descargar el modelo necesario
ollama pull llama2
```

### Timeout / Muy Lento

**Problema**: La generación toma demasiado tiempo

**Soluciones**:
1. Usar un modelo más pequeño: `llama2` en lugar de `llama2:13b`
2. Reducir el tamaño del documento fuente
3. Usar menos preguntas: `--num_preguntas 5`
4. Considerar usar GPU si está disponible

## 📊 Comparación: Gemini vs Ollama

| Característica | Google Gemini | Ollama |
|----------------|---------------|--------|
| **Ubicación** | Nube | Local |
| **Privacidad** | Datos en Google | 100% Privado |
| **Internet** | Requerido | No necesario |
| **Costo** | API Key (puede tener costo) | Gratuito |
| **Velocidad** | Muy rápida | Depende del hardware |
| **Calidad** | Excelente | Muy buena |
| **Instalación** | Solo API key | Requiere software |
| **Recursos** | Ninguno local | RAM y CPU/GPU |

## 🎓 Mejores Prácticas

1. **Para Documentos Pequeños** (<10 páginas):
   ```bash
   python qg.py doc.pdf --motor ollama --modelo llama2
   ```

2. **Para Documentos Grandes** (>50 páginas):
   ```bash
   # Usar Gemini (más rápido) o dividir el documento
   python qg.py doc.pdf --motor gemini --num_preguntas 20
   ```

3. **Para Máxima Privacidad**:
   ```bash
   # Siempre usar Ollama
   python qg.py confidencial.pdf --motor ollama
   ```

4. **Para Mejor Calidad**:
   ```bash
   # Usar Mistral o Gemini Pro
   python qg.py examen.pdf --motor ollama --modelo mistral
   # O
   python qg.py examen.pdf --motor gemini --modelo gemini-1.5-pro
   ```

## 🔗 Enlaces Útiles

- **Ollama**: https://ollama.ai
- **Modelos Disponibles**: https://ollama.ai/library
- **Documentación Ollama**: https://github.com/ollama/ollama
- **Google Gemini**: https://ai.google.dev/

## 💡 Tips Adicionales

1. **Mantener Ollama actualizado**:
   ```bash
   # Windows: Reinstalar desde ollama.ai
   # Linux:
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Liberar espacio eliminando modelos**:
   ```bash
   ollama rm nombre_modelo
   ```

3. **Ver uso de recursos**:
   ```bash
   ollama ps  # Ver modelos en ejecución
   ```

4. **Ejecutar Ollama en segundo plano**:
   ```bash
   # Linux/macOS:
   ollama serve &
   
   # Windows: El servicio se instala automáticamente
   ```

## ⚠️ Warnings Comunes (Normales)

### "Phi SWA is currently disabled"

**¿Qué significa?** Phi SWA (Sliding Window Attention) es una optimización avanzada que no está habilitada en llama.cpp.

**¿Afecta la calidad?** ❌ **NO** - El modelo funciona perfectamente. Este es solo un aviso técnico.

**Acción:** Ignorar. Si quieres evitarlo, usa `gemma2:2b` o `llama3.2:1b` en lugar de `phi3:mini`.

### "n_ctx_seq (4096) < n_ctx_train (131072)"

**¿Qué significa?** El modelo fue entrenado con contexto de 131K tokens, pero Ollama usa 4K por defecto.

**¿Afecta la calidad?** ❌ **NO para documentos normales** - 4096 tokens ≈ 3000 palabras, suficiente para generar 10-20 preguntas.

**Solo afecta si:** Procesas documentos **muy largos** (100+ páginas).

**Aumentar contexto (si necesario):**
```bash
# Temporal (una ejecución)
ollama run phi3:mini --ctx-size 8192

# Permanente: Editar docker-compose.yml
ollama:
  environment:
    OLLAMA_NUM_CTX: 8192  # Requiere más RAM (~8GB)
```

---

**¿Necesitas ayuda?** Abre un issue en https://github.com/TiiZss/ExamGenerator
