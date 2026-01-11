#!/bin/bash

# ExamGenerator - Script de Instalación Automática con UV
# by TiiZss
# Version 11.20260111
# Compatible con Linux y macOS

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}🎓 EXAMGENERATOR - Instalación Automática (UV)${NC}"
echo -e "${CYAN}===============================================${NC}"
echo ""

# Verificar Python
echo -e "${YELLOW}🔍 Verificando Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python encontrado: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo -e "${GREEN}✅ Python encontrado: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ Error: Python no está instalado${NC}"
    echo -e "${YELLOW}Por favor instala Python 3.8+ primero:${NC}"
    echo -e "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo -e "  Fedora:        sudo dnf install python3 python3-pip"
    echo -e "  macOS:         brew install python3"
    exit 1
fi

# Verificar/Instalar UV
echo ""
echo -e "${YELLOW}🚀 Verificando UV (ultra-fast package manager)...${NC}"
if command -v uv &> /dev/null; then
    UV_VERSION=$(uv --version)
    echo -e "${GREEN}✅ UV encontrado: $UV_VERSION${NC}"
else
    echo -e "${YELLOW}📥 UV no encontrado, instalando...${NC}"
    echo -e "${CYAN}   UV es 10-100x más rápido que pip! 🚀${NC}"
    
    # Instalar UV usando curl
    if curl -LsSf https://astral.sh/uv/install.sh | sh; then
        # Agregar UV al PATH de la sesión actual
        export PATH="$HOME/.cargo/bin:$PATH"
        
        UV_VERSION=$(uv --version)
        echo -e "${GREEN}✅ UV instalado correctamente: $UV_VERSION${NC}"
        echo -e "${CYAN}💡 Agrega UV al PATH permanentemente:${NC}"
        echo -e "   echo 'export PATH=\"\$HOME/.cargo/bin:\$PATH\"' >> ~/.bashrc"
        echo -e "   source ~/.bashrc"
    else
        echo -e "${RED}❌ Error instalando UV${NC}"
        echo -e "${YELLOW}Intenta manualmente:${NC}"
        echo -e "   curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
fi

# Crear entorno virtual con UV
echo ""
echo -e "${YELLOW}📦 Creando entorno virtual con UV...${NC}"
if uv venv .venv; then
    echo -e "${GREEN}✅ Entorno virtual creado (.venv)${NC}"
else
    echo -e "${RED}❌ Error creando entorno virtual${NC}"
    exit 1
fi

# Instalar dependencias con UV
echo ""
echo -e "${YELLOW}📚 Instalando dependencias con UV...${NC}"
echo -e "${CYAN}   Esto es mucho más rápido que pip...${NC}"
if uv pip install -r requirements.txt; then
    echo -e "${GREEN}✅ Todas las dependencias instaladas${NC}"
else
    echo -e "${RED}❌ Error instalando dependencias${NC}"
    exit 1
fi

# Mensaje de éxito
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
echo -e "${GREEN}🎉 ¡Instalación completada con UV!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
echo ""

# Instrucciones de uso
echo -e "${CYAN}📋 PRÓXIMOS PASOS:${NC}"
echo ""
echo -e "${WHITE}1️⃣  Activar entorno virtual:${NC}"
echo -e "   ${YELLOW}source .venv/bin/activate${NC}"
echo ""
echo -e "${WHITE}2️⃣  Interfaz Web (Recomendado):${NC}"
echo -e "   ${YELLOW}uv run python run_web.py${NC}"
echo -e "   Luego abre: http://localhost:5000"
echo ""
echo -e "${WHITE}3️⃣  Generador básico (CLI):${NC}"
echo -e "   ${YELLOW}uv run python eg.py examples/preguntas.txt Parcial 3 10${NC}"
echo ""
echo -e "${WHITE}4️⃣  Generador con IA:${NC}"
echo -e "   export GOOGLE_API_KEY='tu-api-key'"
echo -e "   ${YELLOW}uv run python qg.py examples/documento_ia.docx --num_preguntas 10${NC}"
echo ""
echo -e "${WHITE}5️⃣  Ver demo de funcionalidades:${NC}"
echo -e "   ${YELLOW}uv run python examples/demo_features.py${NC}"
echo ""

# Información adicional
echo -e "${CYAN}💡 VENTAJAS DE UV:${NC}"
echo -e "   • 10-100x más rápido que pip"
echo -e "   • Resolución de dependencias inteligente"
echo -e "   • Instalación paralela de paquetes"
echo -e "   • Compatible con requirements.txt"
echo ""
echo -e "${CYAN}📚 Documentación: README.md | QUICK_START_V11.md${NC}"
echo ""
