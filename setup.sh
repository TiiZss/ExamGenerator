#!/bin/bash

# ExamGenerator - Script de Instalación Universal
# by TiiZss
# Compatible con Linux, macOS y Windows (WSL/Git Bash)

# Detectar sistema operativo
detect_os() {
    case "$OSTYPE" in
        linux*|Linux*)
            OS="linux"
            ;;
        darwin*|Darwin*)
            OS="macos"
            ;;
        cygwin*|msys*|win32*|Win*)
            OS="windows"
            ;;
        *)
            OS="unknown"
            ;;
    esac
    echo "Sistema detectado: $OS"
}

# Función principal
main() {
    detect_os
    
    case $OS in
        "linux"|"macos")
            echo "🐧 Ejecutando instalación para Linux/macOS..."
            chmod +x install.sh
            ./install.sh
            ;;
        "windows")
            echo "🪟 Para Windows, ejecuta:"
            echo "powershell -ExecutionPolicy Bypass -File install.ps1"
            ;;
        *)
            echo "❓ Sistema no reconocido. Intentando instalación Linux..."
            chmod +x install.sh
            ./install.sh
            ;;
    esac
}

main "$@"