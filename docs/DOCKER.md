# 🐳 ExamGenerator - Guía Docker

**Versión:** 12.20260111  
**Stack Name:** ExamGenerator  
**Container Prefix:** ExGen-

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación Rápida](#instalación-rápida)
4. [Arquitectura del Stack](#arquitectura-del-stack)
5. [Uso Básico](#uso-básico)
6. [Comandos Avanzados](#comandos-avanzados)
7. [Configuración](#configuración)
8. [Volúmenes y Persistencia](#volúmenes-y-persistencia)
9. [Troubleshooting](#troubleshooting)
10. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## 🎯 Introducción

ExamGenerator está disponible como un stack Docker completo que incluye:

- **ExGen-App**: CLI para generación de exámenes
- **ExGen-Web**: Interfaz web en puerto 5000
- **ExGen-AI-Gemini**: Worker para IA con Google Gemini
- **ExGen-AI-Ollama**: Servidor Ollama para IA local
- **ExGen-AI-Worker**: Worker para IA con Ollama

**Ventajas de usar Docker:**
- ✅ No necesitas instalar Python ni dependencias
- ✅ Entorno aislado y reproducible
- ✅ Fácil de desplegar en cualquier servidor
- ✅ Escalable y portable

---

## 📦 Requisitos Previos

- **Docker**: >= 20.10
- **Docker Compose**: >= 2.0
- **RAM**: Mínimo 2GB (4GB recomendado con IA)
- **Disco**: 2GB para imágenes + espacio para outputs

### Verificar instalación:

```bash
docker --version
docker-compose --version
```

---

## 🚀 Instalación Rápida

### 1. Clonar el repositorio

```bash
git clone https://github.com/TiiZss/ExamGenerator.git
cd ExamGenerator
```

### 2. Configurar variables de entorno

```bash
# Copiar ejemplo de configuración
cp .env.example .env

# Editar con tu API key de Google (opcional, solo para IA)
nano .env
# Añadir: GOOGLE_API_KEY=tu-api-key-aqui
```

### 3. Construir e iniciar

```bash
# Opción A: Usando Make (recomendado)
make -f Makefile.docker build
make -f Makefile.docker up

# Opción B: Usando Docker Compose directamente
docker-compose build
docker-compose up -d app web
```

### 4. Verificar

```bash
# Ver contenedores activos
docker-compose ps

# Ver logs
docker-compose logs -f web

# Acceder a la web
# Abre http://localhost:5000 en tu navegador
```

---

## 🏗️ Arquitectura del Stack

### Contenedores

| Contenedor | Nombre | Puerto | Descripción |
|------------|--------|--------|-------------|
| App | ExGen-App | - | CLI principal para generación |
| Web | ExGen-Web | 5000 | Interfaz web Flask |
| AI Gemini | ExGen-AI-Gemini | - | Worker para Google Gemini |
| Ollama Server | ExGen-AI-Ollama | 11434 | Servidor Ollama (IA local) |
| AI Worker | ExGen-AI-Worker | - | Worker para Ollama |

### Red

- **Nombre**: ExGen-Network
- **Tipo**: Bridge
- **Subnet**: 172.25.0.0/16

### Volúmenes

| Volumen | Nombre | Propósito |
|---------|--------|-----------|
| Output | ExGen-Output | Exámenes generados |
| Logs | ExGen-Logs | Logs de la aplicación |
| Ollama Models | ExGen-Ollama-Models | Modelos de IA locales |

---

## 💻 Uso Básico

### Comandos con Make

```bash
# Ver ayuda
make -f Makefile.docker help

# Información del sistema
make -f Makefile.docker info

# Validar archivo de preguntas
make -f Makefile.docker validate FILE=preguntas.txt

# Generar exámenes
make -f Makefile.docker generate FILE=preguntas.txt PREFIX=Parcial NUM=3 Q=10

# Ver logs
make -f Makefile.docker logs

# Acceder a shell
make -f Makefile.docker shell
```

### Comandos con Docker Compose

```bash
# Iniciar servicios básicos
docker-compose up -d app web

# Iniciar con IA Gemini
docker-compose --profile ai up -d

# Iniciar con Ollama
docker-compose --profile ollama up -d

# Detener todo
docker-compose down

# Ver logs
docker-compose logs -f web

# Ejecutar comando en contenedor
docker-compose exec app cli.py info
```

---

## 🔧 Comandos Avanzados

### Generación de Exámenes

```bash
# Generar 5 exámenes con 20 preguntas en formato DOCX
docker-compose run --rm -v $(pwd)/output:/output app \
  cli.py generate /data/questions/preguntas.txt Final 5 20 \
  --format docx --answers html

# Generar con plantilla personalizada
docker-compose run --rm \
  -v $(pwd)/templates:/app/templates:ro \
  -v $(pwd)/output:/output \
  app cli.py generate /data/questions/preguntas.txt Parcial 3 10 \
  --template /app/templates/mi_plantilla.docx
```

### Generación con IA

```bash
# Con Google Gemini
docker-compose run --rm ai-gemini cli.py ai-generate \
  /data/questions/documento.pdf \
  --num-questions 15 \
  --language español \
  --output /output/preguntas_gemini.txt

# Con Ollama (primero descargar modelo)
docker-compose exec ollama ollama pull llama2

docker-compose run --rm ai-ollama cli.py ai-generate \
  /data/questions/documento.pdf \
  --num-questions 10 \
  --engine ollama \
  --model llama2
```

### Validación

```bash
# Validar archivo de preguntas
docker-compose run --rm app cli.py validate \
  /data/questions/preguntas.txt
```

### Configuración

```bash
# Mostrar configuración actual
docker-compose run --rm app cli.py config --show

# Crear configuración personalizada
docker-compose run --rm app cli.py config --create \
  --path /app/mi_config.yaml
```

---

## ⚙️ Configuración

### Variables de Entorno (.env)

```bash
# API Keys
GOOGLE_API_KEY=tu-api-key-aqui

# Puertos
EXAMGEN_WEB_PORT=5000
OLLAMA_PORT=11434

# IA
GEMINI_MODEL=gemini-1.5-flash
OLLAMA_MODEL=llama2

# Entorno
FLASK_ENV=production
TZ=Europe/Madrid
LOG_LEVEL=INFO
```

### Configuración YAML (config.yaml)

Puedes personalizar `config.yaml` en la raíz del proyecto. Ver [MIGRATION_V12.md](MIGRATION_V12.md) para opciones completas.

### Perfiles de Docker Compose

```bash
# Sin IA (solo App + Web)
docker-compose up -d

# Con IA Gemini
docker-compose --profile ai up -d

# Con Ollama
docker-compose --profile ollama up -d

# Todo junto
docker-compose --profile ai --profile ollama up -d
```

---

## 💾 Volúmenes y Persistencia

### Estructura de Directorios

```
ExamGenerator/
├── examples/          # Montado en /data/questions (read-only)
├── templates/         # Montado en /app/templates (read-only)
├── output/           # Montado en /output (read-write)
│   └── Examenes_*/   # Exámenes generados
├── config.yaml       # Montado en /app/config.yaml
└── ...
```

### Backup de Outputs

```bash
# Usando Make
make -f Makefile.docker backup

# Manual
docker-compose exec app tar -czf /output/backup-$(date +%Y%m%d).tar.gz /output/Examenes_*
docker cp ExGen-App:/output/backup-*.tar.gz ./backups/
```

### Limpiar Outputs

```bash
# Usando Make
make -f Makefile.docker clean

# Manual
docker-compose exec app rm -rf /output/Examenes_*
```

---

## 🔍 Troubleshooting

### Problema: Contenedor no inicia

```bash
# Ver logs detallados
docker-compose logs web

# Verificar estado
docker-compose ps

# Recrear contenedor
docker-compose up -d --force-recreate web
```

### Problema: No puede acceder a la web

```bash
# Verificar puerto
docker-compose port web 5000

# Verificar firewall
sudo ufw allow 5000/tcp

# Probar desde dentro del contenedor
docker-compose exec web curl http://localhost:5000
```

### Problema: "GOOGLE_API_KEY not found"

```bash
# Verificar variable de entorno
docker-compose config | grep GOOGLE_API_KEY

# Verificar archivo .env
cat .env | grep GOOGLE_API_KEY

# Reiniciar con nueva configuración
docker-compose down
docker-compose up -d
```

### Problema: Ollama muy lento

```bash
# Verificar recursos
docker stats ExGen-AI-Ollama

# Usar modelo más ligero
docker-compose exec ollama ollama pull llama2:7b

# Aumentar recursos en docker-compose.yml:
# deploy:
#   resources:
#     limits:
#       cpus: '4'
#       memory: 8G
```

### Problema: Permisos en output/

```bash
# Cambiar permisos del volumen
docker-compose exec --user root app chown -R examgen:examgen /output

# O desde host
sudo chown -R $USER:$USER output/
```

### Limpiar todo y empezar de nuevo

```bash
# Detener y eliminar todo
docker-compose down -v

# Limpiar imágenes
docker rmi examgenerator:12.20260111

# Reconstruir
docker-compose build --no-cache
docker-compose up -d
```

---

## 📚 Ejemplos Prácticos

### Ejemplo 1: Generar exámenes básicos

```bash
# 1. Validar preguntas
make -f Makefile.docker validate FILE=preguntas.txt

# 2. Generar 3 exámenes de 10 preguntas
make -f Makefile.docker generate \
  FILE=preguntas.txt PREFIX=Parcial NUM=3 Q=10

# 3. Ver resultados
ls -lh output/Examenes_Parcial/
```

### Ejemplo 2: Workflow completo con IA

```bash
# 1. Iniciar stack con Gemini
docker-compose --profile ai up -d

# 2. Generar preguntas desde PDF
docker-compose run --rm \
  -v $(pwd)/examples:/data:ro \
  -v $(pwd)/output:/output \
  ai-gemini cli.py ai-generate /data/documento.pdf \
  --num-questions 20 \
  --language español \
  --output /output/preguntas_ia.txt

# 3. Validar preguntas generadas
docker-compose run --rm \
  -v $(pwd)/output:/data \
  app cli.py validate /data/preguntas_ia.txt

# 4. Generar exámenes
docker-compose run --rm \
  -v $(pwd)/output:/data \
  -v $(pwd)/output:/output \
  app cli.py generate /data/preguntas_ia.txt ExamenIA 5 15 \
  --format both --answers html
```

### Ejemplo 3: Uso de la interfaz web

```bash
# 1. Iniciar interfaz web
docker-compose up -d web

# 2. Abrir navegador
make -f Makefile.docker web
# O manualmente: http://localhost:5000

# 3. Subir archivo de preguntas desde la web
# 4. Generar exámenes desde la interfaz
# 5. Descargar resultados
```

### Ejemplo 4: Desarrollo con hot reload

```bash
# Crear docker-compose.dev.yml
cat > docker-compose.dev.yml << 'EOF'
version: '3.8'
services:
  web:
    volumes:
      - ./examgenerator:/app/examgenerator:ro
      - ./cli.py:/app/cli.py:ro
      - ./run_web.py:/app/run_web.py:ro
    environment:
      FLASK_ENV: development
      FLASK_DEBUG: 1
EOF

# Iniciar en modo desarrollo
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up web
```

### Ejemplo 5: Batch processing

```bash
# Generar múltiples conjuntos de exámenes
for prefix in Parcial1 Parcial2 Final; do
  docker-compose run --rm -v $(pwd)/output:/output app \
    cli.py generate /data/questions/preguntas.txt \
    $prefix 3 10 --format both --answers xlsx
done

# Comprimir todos los outputs
cd output && tar -czf examenes_$(date +%Y%m%d).tar.gz Examenes_*
```

---

## 🚢 Deployment en Producción

### Docker Swarm

```bash
# Inicializar Swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml examgen

# Verificar servicios
docker stack services examgen

# Ver logs
docker service logs -f examgen_web
```

### Kubernetes (básico)

```bash
# Generar manifests desde docker-compose
kompose convert -f docker-compose.yml

# Aplicar
kubectl apply -f .

# Verificar
kubectl get pods -l app=examgenerator
```

### Reverse Proxy con Nginx

```nginx
# /etc/nginx/sites-available/examgen
server {
    listen 80;
    server_name examgen.tudominio.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### SSL con Let's Encrypt

```bash
# Instalar certbot
docker run -it --rm --name certbot \
  -v "/etc/letsencrypt:/etc/letsencrypt" \
  -v "/var/lib/letsencrypt:/var/lib/letsencrypt" \
  certbot/certbot certonly --standalone \
  -d examgen.tudominio.com

# Configurar nginx con SSL
# Actualizar docker-compose.yml con volúmenes SSL
```

---

## 📊 Monitoring y Logs

### Ver logs en tiempo real

```bash
# Todos los servicios
docker-compose logs -f

# Solo web
docker-compose logs -f web

# Con timestamps
docker-compose logs -f --timestamps web
```

### Monitoreo de recursos

```bash
# Ver uso de recursos
docker stats ExGen-App ExGen-Web

# Inspeccionar contenedor
docker inspect ExGen-Web

# Ver procesos
docker-compose exec web ps aux
```

### Healthchecks

```bash
# Ver estado de salud
docker-compose ps

# Healthcheck manual
docker-compose exec web curl -f http://localhost:5000/health || echo "Unhealthy"
```

---

## 🔐 Seguridad

### Mejores prácticas

1. **No ejecutar como root**: Los contenedores usan usuario `examgen`
2. **Variables de entorno**: Nunca commitear `.env` con secrets
3. **Red aislada**: Stack usa red bridge privada
4. **Volúmenes read-only**: Templates y ejemplos montados RO
5. **Secrets management**: Usar Docker secrets en producción

### Escaneo de vulnerabilidades

```bash
# Escanear imagen
docker scan examgenerator:12.20260111

# Con Trivy
trivy image examgenerator:12.20260111
```

---

## 🎓 Cheat Sheet

```bash
# === BUILD ===
make -f Makefile.docker build          # Construir imágenes
make -f Makefile.docker build-fast     # Build rápido (con cache)

# === UP/DOWN ===
make -f Makefile.docker up             # Iniciar App + Web
make -f Makefile.docker up-ai          # Iniciar con IA Gemini
make -f Makefile.docker up-ollama      # Iniciar con Ollama
make -f Makefile.docker down           # Detener todo

# === LOGS ===
make -f Makefile.docker logs           # Ver todos los logs
make -f Makefile.docker logs-web       # Solo logs web
make -f Makefile.docker ps             # Listar contenedores

# === SHELL ===
make -f Makefile.docker shell          # Shell en App
make -f Makefile.docker shell-web      # Shell en Web
make -f Makefile.docker shell-root     # Shell como root

# === COMANDOS ===
make -f Makefile.docker info           # Info del sistema
make -f Makefile.docker validate FILE=preguntas.txt
make -f Makefile.docker generate FILE=preguntas.txt PREFIX=Test NUM=2 Q=5
make -f Makefile.docker ai-generate FILE=doc.pdf NUM=10

# === LIMPIEZA ===
make -f Makefile.docker clean          # Limpiar outputs
make -f Makefile.docker clean-logs     # Limpiar logs
make -f Makefile.docker prune          # Limpieza profunda Docker

# === OLLAMA ===
make -f Makefile.docker ollama-pull MODEL=llama2
make -f Makefile.docker ollama-list
make -f Makefile.docker ollama-rm MODEL=llama2

# === OTROS ===
make -f Makefile.docker demo           # Demo completo
make -f Makefile.docker backup         # Backup de outputs
make -f Makefile.docker web            # Abrir navegador
```

---

## 📞 Soporte

- **GitHub**: https://github.com/TiiZss/ExamGenerator
- **Issues**: https://github.com/TiiZss/ExamGenerator/issues
- **Documentación**: [docs/](../docs/)

---

## 📝 Changelog Docker

**v12.20260111:**
- ✨ Stack Docker completo con prefijo ExGen-
- ✨ Multi-stage build optimizado
- ✨ Soporte para Gemini y Ollama
- ✨ Makefile con 30+ comandos
- ✨ Health checks integrados
- ✨ Usuario no-root por seguridad
- ✨ Volúmenes persistentes
- ✨ Red aislada
- ✨ Profiles para diferentes modos
- ✨ Documentación completa

---

**¡Happy Dockering!** 🐳🎉
