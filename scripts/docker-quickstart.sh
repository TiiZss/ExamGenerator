#!/bin/bash
# ExamGenerator - Quick Start Docker Script

set -e

echo "🐳 ExamGenerator Docker - Quick Start"
echo "====================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Error: Docker no está instalado${NC}"
    echo "Instala Docker desde: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Error: Docker Compose no está instalado${NC}"
    echo "Instala Docker Compose desde: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✓ Docker y Docker Compose detectados${NC}"
echo ""

# Check .env
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️ Archivo .env no encontrado${NC}"
    echo "Creando desde .env.example..."
    cp .env.example .env
    echo -e "${GREEN}✓ .env creado${NC}"
    echo -e "${YELLOW}⚠️ IMPORTANTE: Edita .env y añade tu GOOGLE_API_KEY si vas a usar IA${NC}"
    echo ""
fi

# Check output directory
if [ ! -d output ]; then
    echo "📁 Creando directorio output..."
    mkdir -p output
fi

# Menu
echo "Elige una opción:"
echo ""
echo "1) Build - Construir imágenes Docker"
echo "2) Start - Iniciar stack básico (App + Web)"
echo "3) Start AI - Iniciar con soporte de IA (Gemini)"
echo "4) Start Ollama - Iniciar con Ollama (IA local)"
echo "5) Stop - Detener todos los contenedores"
echo "6) Logs - Ver logs en tiempo real"
echo "7) Shell - Abrir terminal en contenedor"
echo "8) Demo - Ejecutar demo completo"
echo "9) Clean - Limpiar outputs generados"
echo "0) Exit"
echo ""
read -p "Opción: " option

case $option in
    1)
        echo -e "${YELLOW}🔨 Construyendo imágenes...${NC}"
        docker-compose build
        echo -e "${GREEN}✓ Build completado${NC}"
        ;;
    2)
        echo -e "${YELLOW}🚀 Iniciando stack básico...${NC}"
        docker-compose up -d app web
        echo -e "${GREEN}✓ Stack iniciado${NC}"
        echo ""
        echo "📊 Web UI: http://localhost:5000"
        echo "Ver logs: docker-compose logs -f web"
        ;;
    3)
        echo -e "${YELLOW}🚀 Iniciando con IA Gemini...${NC}"
        if [ -z "$GOOGLE_API_KEY" ] && ! grep -q "GOOGLE_API_KEY=.*[^=]" .env; then
            echo -e "${RED}⚠️ ADVERTENCIA: GOOGLE_API_KEY no configurada en .env${NC}"
            echo "Edita .env y añade tu API key de Google"
        fi
        docker-compose --profile ai up -d
        echo -e "${GREEN}✓ Stack con IA iniciado${NC}"
        ;;
    4)
        echo -e "${YELLOW}🚀 Iniciando con Ollama...${NC}"
        docker-compose --profile ollama up -d
        echo ""
        echo -e "${YELLOW}⬇️ Descargando modelo llama2...${NC}"
        echo "Esto puede tardar varios minutos..."
        docker-compose exec ollama ollama pull llama2
        echo -e "${GREEN}✓ Stack con Ollama listo${NC}"
        ;;
    5)
        echo -e "${YELLOW}🛑 Deteniendo contenedores...${NC}"
        docker-compose down
        echo -e "${GREEN}✓ Contenedores detenidos${NC}"
        ;;
    6)
        echo -e "${YELLOW}📋 Mostrando logs (Ctrl+C para salir)...${NC}"
        docker-compose logs -f
        ;;
    7)
        echo -e "${YELLOW}🐚 Abriendo shell en ExGen-App...${NC}"
        docker-compose exec app /bin/bash
        ;;
    8)
        echo -e "${YELLOW}🎬 Ejecutando demo...${NC}"
        echo ""
        echo "1. Validando preguntas..."
        docker-compose run --rm app cli.py validate /data/questions/preguntas.txt
        echo ""
        echo "2. Generando 2 exámenes de 5 preguntas..."
        docker-compose run --rm -v $(pwd)/output:/output app \
            cli.py generate /data/questions/preguntas.txt Demo 2 5 \
            --format both --answers html
        echo ""
        echo -e "${GREEN}✓ Demo completado${NC}"
        echo "📁 Revisa: output/Examenes_Demo/"
        ;;
    9)
        echo -e "${YELLOW}🧹 Limpiando outputs...${NC}"
        rm -rf output/Examenes_*
        echo -e "${GREEN}✓ Limpieza completada${NC}"
        ;;
    0)
        echo "👋 ¡Hasta luego!"
        exit 0
        ;;
    *)
        echo -e "${RED}❌ Opción inválida${NC}"
        exit 1
        ;;
esac

echo ""
echo "Para más opciones: make -f Makefile.docker help"
echo "Documentación: docs/DOCKER.md"
