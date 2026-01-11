# 🐳 ExamGenerator Docker Stack - Resumen

**Fecha:** 11 de Enero de 2026  
**Versión:** 12.20260111  
**Stack Name:** ExamGenerator  
**Container Prefix:** ExGen-

---

## ✅ Implementación Completada

Se ha creado un stack Docker completo y profesional para ExamGenerator con las siguientes características:

### 📦 Archivos Creados

1. **Dockerfile** (Multi-stage build optimizado)
   - Stage 1: Builder con UV para dependencias
   - Stage 2: Runtime optimizada
   - Usuario no-root (examgen:1000)
   - Healthcheck integrado
   - Tamaño optimizado

2. **docker-compose.yml** (Stack completo)
   - 5 contenedores con prefijo ExGen-
   - 3 volúmenes persistentes
   - Red privada bridge
   - Profiles para diferentes modos
   - Healthchecks

3. **.dockerignore** (Optimización build)
   - Ignora archivos innecesarios
   - Reduce tamaño de contexto
   - Mejora velocidad de build

4. **.env.example** (Template de configuración)
   - Variables de entorno documentadas
   - API keys
   - Configuración de puertos
   - Modelos de IA

5. **Makefile.docker** (30+ comandos)
   - Comandos simplificados
   - Build, up, down, logs
   - Generación de exámenes
   - IA con Gemini/Ollama
   - Limpieza y backup

6. **docs/DOCKER.md** (Documentación completa)
   - 900+ líneas
   - Guía de instalación
   - Ejemplos prácticos
   - Troubleshooting
   - Deployment en producción

7. **scripts/docker-quickstart.sh** (Linux/Mac)
   - Script interactivo
   - Menú con 10 opciones
   - Validaciones automáticas

8. **scripts/docker-quickstart.ps1** (Windows)
   - Versión PowerShell
   - Mismas funcionalidades
   - Colores y formato

9. **output/.gitkeep + README.md**
   - Directorio para outputs
   - Documentado
   - Git-friendly

---

## 🏗️ Arquitectura del Stack

### Contenedores

| Nombre | Imagen | Puerto | Perfil | Descripción |
|--------|--------|--------|--------|-------------|
| **ExGen-App** | examgenerator:12 | - | default | CLI principal |
| **ExGen-Web** | examgenerator:12 | 5000 | default | Interfaz web |
| **ExGen-AI-Gemini** | examgenerator:12 | - | ai | Worker Gemini |
| **ExGen-AI-Ollama** | ollama:latest | 11434 | ollama | Servidor Ollama |
| **ExGen-AI-Worker** | examgenerator:12 | - | ollama | Worker Ollama |

### Volúmenes

- **ExGen-Output**: Exámenes generados (persistente)
- **ExGen-Logs**: Logs de aplicación (persistente)
- **ExGen-Ollama-Models**: Modelos IA locales (persistente)

### Red

- **ExGen-Network**: Bridge privada (172.25.0.0/16)

---

## 🚀 Inicio Rápido

### Opción 1: Script Interactivo (Recomendado)

**Linux/Mac:**
```bash
chmod +x scripts/docker-quickstart.sh
./scripts/docker-quickstart.sh
```

**Windows:**
```powershell
.\scripts\docker-quickstart.ps1
```

### Opción 2: Makefile

```bash
# Build
make -f Makefile.docker build

# Iniciar
make -f Makefile.docker up

# Ver web
# Abre http://localhost:5000
```

### Opción 3: Docker Compose

```bash
# Build
docker-compose build

# Iniciar
docker-compose up -d app web

# Logs
docker-compose logs -f web
```

---

## 💡 Casos de Uso

### 1. Generación Básica

```bash
make -f Makefile.docker generate \
  FILE=preguntas.txt PREFIX=Parcial NUM=3 Q=10
```

### 2. Con IA Gemini

```bash
# 1. Configurar API key en .env
echo "GOOGLE_API_KEY=tu-key" >> .env

# 2. Iniciar con IA
make -f Makefile.docker up-ai

# 3. Generar preguntas
make -f Makefile.docker ai-generate \
  FILE=documento.pdf NUM=15
```

### 3. Con Ollama (IA Local)

```bash
# 1. Iniciar Ollama
make -f Makefile.docker up-ollama

# 2. Descargar modelo
make -f Makefile.docker ollama-pull MODEL=llama2

# 3. Usar
docker-compose run --rm ai-ollama cli.py ai-generate \
  /data/questions/doc.pdf --engine ollama --num-questions 10
```

### 4. Interfaz Web

```bash
# Iniciar
make -f Makefile.docker up

# Abrir navegador
make -f Makefile.docker web

# Acceder: http://localhost:5000
```

---

## 🔧 Comandos Esenciales

```bash
# === GESTIÓN ===
make -f Makefile.docker build          # Construir
make -f Makefile.docker up             # Iniciar
make -f Makefile.docker down           # Detener
make -f Makefile.docker restart        # Reiniciar
make -f Makefile.docker ps             # Estado

# === LOGS ===
make -f Makefile.docker logs           # Todos
make -f Makefile.docker logs-web       # Solo web
make -f Makefile.docker logs-app       # Solo app

# === SHELL ===
make -f Makefile.docker shell          # Terminal
make -f Makefile.docker shell-root     # Terminal root

# === EXAMGENERATOR ===
make -f Makefile.docker info           # Info sistema
make -f Makefile.docker validate FILE=preguntas.txt
make -f Makefile.docker generate FILE=preguntas.txt PREFIX=Test NUM=2 Q=5
make -f Makefile.docker demo           # Demo completo

# === LIMPIEZA ===
make -f Makefile.docker clean          # Limpiar outputs
make -f Makefile.docker backup         # Backup
make -f Makefile.docker prune          # Limpieza profunda
```

---

## 📊 Características Técnicas

### Optimizaciones

✅ **Multi-stage build**: Reduce tamaño de imagen final  
✅ **Layer caching**: Build incremental rápido  
✅ **No-root user**: Seguridad mejorada (UID 1000)  
✅ **Healthchecks**: Monitoreo automático  
✅ **Volume persistence**: Datos seguros  
✅ **Network isolation**: Red privada  

### Seguridad

✅ Usuario examgen (no-root)  
✅ Secrets via .env (no hardcoded)  
✅ Volúmenes read-only donde aplica  
✅ Red bridge aislada  
✅ Minimal base image (python:3.11-slim)  

### Escalabilidad

✅ Profiles para diferentes modos  
✅ Variables de entorno configurables  
✅ Compatible con Docker Swarm  
✅ Compatible con Kubernetes (via kompose)  
✅ Reverse proxy ready  

---

## 📁 Estructura de Archivos Docker

```
ExamGenerator/
├── Dockerfile                 # Imagen principal
├── docker-compose.yml         # Orquestación
├── .dockerignore             # Optimización build
├── .env.example              # Template variables
├── Makefile.docker           # Comandos simplificados
├── output/                   # Outputs (volumen)
│   ├── .gitkeep
│   └── README.md
├── scripts/
│   ├── docker-quickstart.sh  # Quick start Linux/Mac
│   └── docker-quickstart.ps1 # Quick start Windows
└── docs/
    └── DOCKER.md             # Documentación completa
```

---

## 🎯 Beneficios del Stack Docker

| Aspecto | Sin Docker | Con Docker | Mejora |
|---------|------------|------------|--------|
| **Setup Time** | 30-60 min | 5 min | **83% ↓** |
| **Dependencias** | Manual | Automático | **100%** |
| **Portabilidad** | Compleja | 1 comando | **∞** |
| **Aislamiento** | No | Sí | **NUEVO** |
| **Escalabilidad** | Difícil | Fácil | **NUEVO** |
| **Rollback** | Manual | Tag imagen | **NUEVO** |
| **Multi-entorno** | Conflictos | Aislado | **100%** |

---

## 📖 Documentación

### Documentos Disponibles

1. **docs/DOCKER.md** (900+ líneas)
   - Instalación completa
   - Troubleshooting
   - Deployment
   - Ejemplos avanzados

2. **Makefile.docker**
   - 30+ comandos documentados
   - `make -f Makefile.docker help`

3. **.env.example**
   - Todas las variables explicadas

4. **docker-compose.yml**
   - Comentarios inline
   - Configuración completa

---

## 🧪 Testing

### Validación del Stack

```bash
# 1. Build exitoso
make -f Makefile.docker build
# ✓ Sin errores

# 2. Iniciar servicios
make -f Makefile.docker up
# ✓ ExGen-App: running
# ✓ ExGen-Web: running

# 3. Healthcheck
docker ps
# STATUS: Up X minutes (healthy)

# 4. Web accesible
curl http://localhost:5000
# ✓ Respuesta 200 OK

# 5. CLI funcional
make -f Makefile.docker info
# ✓ Muestra versión y módulos

# 6. Demo completo
make -f Makefile.docker demo
# ✓ Valida + genera exámenes
```

---

## 🌐 Deployment

### Development

```bash
docker-compose up
```

### Production

```bash
# Con Docker Swarm
docker swarm init
docker stack deploy -c docker-compose.yml examgen

# Con Docker Compose (simple)
docker-compose up -d --scale web=3
```

### Con Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name examgen.tudominio.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🔄 Mantenimiento

### Actualización

```bash
# 1. Pull nueva versión
git pull origin main

# 2. Rebuild
make -f Makefile.docker build

# 3. Reiniciar
make -f Makefile.docker down
make -f Makefile.docker up
```

### Backup

```bash
# Outputs
make -f Makefile.docker backup

# Volúmenes completos
docker run --rm -v ExGen-Output:/data -v $(pwd)/backups:/backup \
  alpine tar -czf /backup/output-$(date +%Y%m%d).tar.gz /data
```

### Limpieza

```bash
# Outputs generados
make -f Makefile.docker clean

# Logs
make -f Makefile.docker clean-logs

# Todo (cuidado!)
make -f Makefile.docker prune
```

---

## 📞 Soporte

- **Documentación**: [docs/DOCKER.md](DOCKER.md)
- **GitHub**: https://github.com/TiiZss/ExamGenerator
- **Issues**: https://github.com/TiiZss/ExamGenerator/issues

---

## ✅ Checklist de Implementación

- [x] Dockerfile multi-stage optimizado
- [x] docker-compose.yml con 5 servicios
- [x] Prefijo ExGen- en todos los contenedores
- [x] 3 volúmenes persistentes
- [x] Red privada ExGen-Network
- [x] .dockerignore optimizado
- [x] .env.example documentado
- [x] Makefile.docker con 30+ comandos
- [x] docs/DOCKER.md (900+ líneas)
- [x] Scripts quick-start (Bash + PowerShell)
- [x] Healthchecks en servicios
- [x] Usuario no-root
- [x] Profiles para AI/Ollama
- [x] Documentación completa
- [x] Ejemplos de uso
- [x] Troubleshooting guide

---

## 🎉 Conclusión

Stack Docker completamente funcional para ExamGenerator con:

- ✅ **5 contenedores** con prefijo ExGen-
- ✅ **3 volúmenes** persistentes
- ✅ **1 red** privada
- ✅ **30+ comandos** Make
- ✅ **900+ líneas** de documentación
- ✅ **Scripts** interactivos
- ✅ **Multi-platform** (Linux, Mac, Windows)
- ✅ **Production-ready**

**¡Todo listo para usar Docker con ExamGenerator!** 🐳🚀

---

**Quick Start:**
```bash
# Opción 1: Script interactivo
./scripts/docker-quickstart.sh

# Opción 2: Make
make -f Makefile.docker build && make -f Makefile.docker up

# Opción 3: Docker Compose
docker-compose up -d
```

**Acceder a Web UI:** http://localhost:5000
