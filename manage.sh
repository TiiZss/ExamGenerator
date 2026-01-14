#!/bin/bash
# ExamGenerator Management Menu

while true; do
    clear
    echo "========================================================"
    echo "              EXAMGENERATOR MANAGEMENT"
    echo "========================================================"
    echo ""
    echo "  1. Start Environment (Local)"
    echo "     [Launches Docker Stack: App + Web + DB]"
    echo ""
    echo "  2. Deploy to Production"
    echo "     [Uploads code to server and deploys]"
    echo ""
    echo "  3. Docker Quickstart"
    echo "     [Clean start without cache]"
    echo ""
    echo "  4. Install Dependencies"
    echo "     [Setup local python environment]"
    echo ""
    echo "  5. Generate Secret Key"
    echo "     [Create new Flask Secret Key]"
    echo ""
    echo "  6. CLI Help"
    echo "     [Show available ExamGenerator commands]"
    echo ""
    echo "  0. Exit"
    echo ""
    echo "========================================================"
    read -p "Select an option [0-6]: " choice

    case $choice in
        1)
            bash scripts/start.sh
            echo ""
            read -p "Press Enter to continue..."
            ;;
        2)
            # Check for powershell context or emulate deploy
            echo "Deploy script is currently PowerShell based."
            if command -v pwsh &> /dev/null; then
                pwsh scripts/deploy.ps1
            else
                echo "Error: 'pwsh' not found. Please run this on Windows or install PowerShell for Linux."
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        3)
            bash scripts/docker-quickstart.sh
            echo ""
            read -p "Press Enter to continue..."
            ;;
        4)
            bash scripts/install.sh
            echo ""
            read -p "Press Enter to continue..."
            ;;
        5)
            python3 scripts/generate_secret.py
            echo ""
            read -p "Press Enter to continue..."
            ;;
        6)
            python3 cli.py --help
            echo ""
            read -p "Press Enter to continue..."
            ;;
        0)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            sleep 2
            ;;
    esac
done
