#!/bin/bash

# ExamGenerator - Script de Instalación Automática para Linux
# by TiiZss
# Compatible con Ubuntu, Debian, CentOS, Fedora, Arch Linux y otras distribuciones

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_header() {
    echo -e "${CYAN}🎓 EXAMGENERATOR - Instalación Automática para Linux${NC}"
    echo -e "${CYAN}====================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ Error: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_info() {
    echo -e "${BLUE}🔍 $1${NC}"
}

print_step() {
    echo -e "${YELLOW}📦 $1${NC}"
}

# Función para detectar la distribución
detect_distro() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        DISTRO=$ID
        VERSION=$VERSION_ID
    elif [[ -f /etc/redhat-release ]]; then
        DISTRO="rhel"
    elif [[ -f /etc/debian_version ]]; then
        DISTRO="debian"
    else
        DISTRO="unknown"
    fi
    
    echo "Distribución detectada: $DISTRO"
}

# Función para instalar Python según la distribución
install_python() {
    print_step "Instalando Python y pip..."
    
    case $DISTRO in
        "ubuntu"|"debian")
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv
            ;;
        "fedora")
            sudo dnf install -y python3 python3-pip python3-venv
            ;;
        "centos"|"rhel")
            sudo yum install -y python3 python3-pip python3-venv
            ;;
        "arch"|"manjaro")
            sudo pacman -S --noconfirm python python-pip python-virtualenv
            ;;
        "opensuse"|"sles")
            sudo zypper install -y python3 python3-pip python3-venv
            ;;
        *)
            print_warning "Distribución no reconocida. Intentando instalación genérica..."
            if command -v apt >/dev/null 2>&1; then
                sudo apt update && sudo apt install -y python3 python3-pip python3-venv
            elif command -v yum >/dev/null 2>&1; then
                sudo yum install -y python3 python3-pip python3-venv
            elif command -v pacman >/dev/null 2>&1; then
                sudo pacman -S --noconfirm python python-pip python-virtualenv
            else
                print_error "No se pudo instalar Python automáticamente"
                print_info "Por favor instala Python 3.8+ manualmente desde tu gestor de paquetes"
                exit 1
            fi
            ;;
    esac
}

# Función para verificar Python
check_python() {
    print_info "Verificando Python..."
    
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_CMD="python3"
    elif command -v python >/dev/null 2>&1; then
        PYTHON_CMD="python"
    else
        print_error "Python no está instalado"
        read -p "¿Deseas instalar Python automáticamente? (s/N): " install_choice
        if [[ $install_choice =~ ^[SsYy]$ ]]; then
            detect_distro
            install_python
            if command -v python3 >/dev/null 2>&1; then
                PYTHON_CMD="python3"
            elif command -v python >/dev/null 2>&1; then
                PYTHON_CMD="python"
            else
                print_error "Falló la instalación de Python"
                exit 1
            fi
        else
            print_info "Por favor instala Python 3.8+ manualmente y ejecuta este script nuevamente"
            exit 1
        fi
    fi
    
    # Verificar versión de Python
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -ge 8 ]] || [[ $PYTHON_MAJOR -gt 3 ]]; then
        print_success "Python encontrado: $PYTHON_VERSION"
    else
        print_error "Se requiere Python 3.8 o superior. Versión encontrada: $PYTHON_VERSION"
        exit 1
    fi
}

# Función para verificar pip
check_pip() {
    print_info "Verificando pip..."
    
    if command -v pip3 >/dev/null 2>&1; then
        PIP_CMD="pip3"
    elif command -v pip >/dev/null 2>&1; then
        PIP_CMD="pip"
    else
        print_error "pip no está instalado"
        print_step "Instalando pip..."
        
        # Intentar instalar pip
        if command -v apt >/dev/null 2>&1; then
            sudo apt install -y python3-pip
        elif command -v yum >/dev/null 2>&1; then
            sudo yum install -y python3-pip
        elif command -v pacman >/dev/null 2>&1; then
            sudo pacman -S --noconfirm python-pip
        else
            # Método alternativo usando get-pip.py
            print_step "Descargando e instalando pip..."
            curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
            $PYTHON_CMD get-pip.py --user
            rm get-pip.py
        fi
        
        # Verificar nuevamente
        if command -v pip3 >/dev/null 2>&1; then
            PIP_CMD="pip3"
        elif command -v pip >/dev/null 2>&1; then
            PIP_CMD="pip"
        else
            print_error "No se pudo instalar pip"
            exit 1
        fi
    fi
    
    print_success "pip encontrado"
}

# Función para crear entorno virtual
create_virtual_env() {
    print_step "Creando entorno virtual..."
    
    if [[ -d ".venv" ]]; then
        print_warning "El entorno virtual ya existe. ¿Deseas recrearlo?"
        read -p "Recrear entorno virtual? (s/N): " recreate_choice
        if [[ $recreate_choice =~ ^[SsYy]$ ]]; then
            rm -rf .venv
        else
            print_info "Usando entorno virtual existente"
            return 0
        fi
    fi
    
    $PYTHON_CMD -m venv .venv
    
    if [[ $? -eq 0 ]]; then
        print_success "Entorno virtual creado"
    else
        print_error "No se pudo crear el entorno virtual"
        print_info "Intentando con virtualenv..."
        
        # Instalar virtualenv si no está disponible
        $PIP_CMD install --user virtualenv
        virtualenv .venv
        
        if [[ $? -ne 0 ]]; then
            print_error "No se pudo crear el entorno virtual con virtualenv"
            exit 1
        fi
        print_success "Entorno virtual creado con virtualenv"
    fi
}

# Función para activar entorno virtual
activate_virtual_env() {
    print_step "Activando entorno virtual..."
    
    if [[ -f ".venv/bin/activate" ]]; then
        source .venv/bin/activate
        print_success "Entorno virtual activado"
    else
        print_error "No se encontró el script de activación del entorno virtual"
        exit 1
    fi
}

# Función para instalar dependencias
install_dependencies() {
    print_step "Actualizando pip..."
    pip install --upgrade pip
    
    print_step "Instalando dependencias..."
    
    if [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt
        if [[ $? -eq 0 ]]; then
            print_success "Dependencias instaladas correctamente"
        else
            print_error "Error al instalar algunas dependencias"
            print_info "Intentando instalación individual de dependencias críticas..."
            
            # Instalar dependencias críticas una por una
            critical_deps=("python-docx>=1.1.0" "openpyxl>=3.1.0")
            for dep in "${critical_deps[@]}"; do
                print_info "Instalando $dep..."
                pip install "$dep"
            done
            
            print_warning "Algunas dependencias opcionales pueden no haberse instalado"
            print_info "El generador básico debería funcionar correctamente"
        fi
    else
        print_error "Archivo requirements.txt no encontrado"
        print_step "Instalando dependencias básicas manualmente..."
        
        pip install python-docx>=1.1.0 openpyxl>=3.1.0
        print_info "Instalando dependencias opcionales para IA..."
        pip install google-generativeai>=0.3.0 pypdf>=3.17.0 python-pptx>=0.6.23 typing-extensions>=4.8.0 2>/dev/null || true
    fi
}

# Función para verificar instalación
verify_installation() {
    print_step "Verificando instalación..."
    
    # Verificar que los módulos principales se puedan importar
    if $PYTHON_CMD -c "import docx, openpyxl" 2>/dev/null; then
        print_success "Módulos principales verificados"
    else
        print_error "Error en la verificación de módulos principales"
        exit 1
    fi
    
    # Verificar archivos del proyecto
    if [[ -f "eg.py" && -f "qg.py" && -f "preguntas.txt" ]]; then
        print_success "Archivos del proyecto verificados"
    else
        print_warning "Algunos archivos del proyecto no se encontraron"
        print_info "Asegúrate de estar en el directorio correcto del proyecto"
    fi
}

# Función para mostrar información post-instalación
show_next_steps() {
    echo ""
    echo -e "${GREEN}🎉 ¡Instalación completada!${NC}"
    echo ""
    echo -e "${CYAN}📋 PRÓXIMOS PASOS:${NC}"
    echo ""
    echo -e "${NC}1. ${YELLOW}Para activar el entorno virtual manualmente:${NC}"
    echo -e "${BLUE}   source .venv/bin/activate${NC}"
    echo ""
    echo -e "${NC}2. ${YELLOW}Para usar el generador básico:${NC}"
    echo -e "${BLUE}   python eg.py preguntas.txt MiExamen 5 10${NC}"
    echo ""
    echo -e "${NC}3. ${YELLOW}Para usar el generador con IA (opcional):${NC}"
    echo -e "${BLUE}   export GOOGLE_API_KEY='tu-api-key'${NC}"
    echo -e "${BLUE}   python qg.py documento.pdf --num_preguntas 10${NC}"
    echo ""
    echo -e "${NC}4. ${YELLOW}Para desactivar el entorno virtual:${NC}"
    echo -e "${BLUE}   deactivate${NC}"
    echo ""
    echo -e "${NC}5. ${YELLOW}Lee el README.md para más opciones avanzadas${NC}"
    echo ""
    echo -e "${CYAN}📚 COMANDOS ÚTILES:${NC}"
    echo -e "${NC}   • Ver ayuda completa: ${BLUE}python eg.py${NC}"
    echo -e "${NC}   • Generar examen DOCX: ${BLUE}python eg.py preguntas.txt Test 3 5 docx${NC}"
    echo -e "${NC}   • Respuestas en HTML: ${BLUE}python eg.py preguntas.txt Test 3 5 txt \"\" html${NC}"
    echo ""
}

# Función principal
main() {
    print_header
    
    # Verificar si estamos en el directorio correcto
    if [[ ! -f "eg.py" ]]; then
        print_warning "No se encontró eg.py en el directorio actual"
        print_info "Asegúrate de estar en el directorio del proyecto ExamGenerator"
        read -p "¿Continuar de todos modos? (s/N): " continue_choice
        if [[ ! $continue_choice =~ ^[SsYy]$ ]]; then
            exit 1
        fi
    fi
    
    # Detectar distribución
    detect_distro
    
    # Verificar e instalar Python si es necesario
    check_python
    
    # Verificar e instalar pip si es necesario
    check_pip
    
    # Crear entorno virtual
    create_virtual_env
    
    # Activar entorno virtual
    activate_virtual_env
    
    # Instalar dependencias
    install_dependencies
    
    # Verificar instalación
    verify_installation
    
    # Mostrar pasos siguientes
    show_next_steps
}

# Manejo de errores
trap 'print_error "Instalación interrumpida"; exit 1' INT TERM

# Verificar si el script se ejecuta como root (no recomendado para entornos virtuales)
if [[ $EUID -eq 0 ]]; then
    print_warning "Ejecutando como root no es recomendado para entornos virtuales"
    print_info "Se recomienda ejecutar como usuario normal"
    read -p "¿Continuar como root? (s/N): " root_choice
    if [[ ! $root_choice =~ ^[SsYy]$ ]]; then
        exit 1
    fi
fi

# Ejecutar función principal
main "$@"