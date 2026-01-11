#!/bin/bash

# ExamGenerator - Instalación Rápida para Linux
# by TiiZss

echo "🎓 ExamGenerator - Instalación Rápida"
echo "===================================="

# Colores básicos
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 no encontrado${NC}"
    echo "Instala Python3 con: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

echo -e "${GREEN}✅ Python3 encontrado${NC}"

# Crear entorno virtual
echo -e "${YELLOW}📦 Creando entorno virtual...${NC}"
python3 -m venv .venv

# Activar entorno virtual
echo -e "${YELLOW}🔧 Activando entorno virtual...${NC}"
source .venv/bin/activate

# Actualizar pip e instalar dependencias
echo -e "${YELLOW}📚 Instalando dependencias...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}🎉 ¡Instalación completada!${NC}"
echo ""
echo "Para usar:"
echo "1. source .venv/bin/activate"
echo "2. python eg.py preguntas.txt Test 5 10"
echo ""
echo "Para desactivar: deactivate"