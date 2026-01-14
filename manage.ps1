<#
.SYNOPSIS
    ExamGenerator Management Menu for PowerShell
.DESCRIPTION
    Provides a menu-driven interface to manage the ExamGenerator project on Windows.
#>

function Show-Menu {
    Clear-Host
    Write-Host "========================================================" -ForegroundColor Cyan
    Write-Host "              EXAMGENERATOR MANAGEMENT" -ForegroundColor Cyan
    Write-Host "========================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  1. Start Environment (Local)"
    Write-Host "     [Launches Docker Stack: App + Web + DB]" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  2. Deploy to Production"
    Write-Host "     [Uploads code to server and deploys]" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  3. Docker Quickstart"
    Write-Host "     [Clean start without cache]" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  4. Install Dependencies"
    Write-Host "     [Setup local python environment]" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  5. Generate Secret Key"
    Write-Host "     [Create new Flask Secret Key]" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  6. CLI Help"
    Write-Host "     [Show available ExamGenerator commands]" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  0. Exit"
    Write-Host ""
    Write-Host "========================================================" -ForegroundColor Cyan
}

function Run-Start {
    Clear-Host
    if (Test-Path "scripts\start.ps1") {
        & "scripts\start.ps1"
    }
    else {
        Write-Warning "scripts\start.ps1 not found. Falling back to scripts\start.bat"
        cmd.exe /c "scripts\start.bat"
    }
    Pause
}

function Run-Deploy {
    Clear-Host
    Write-Host "Launching Deployment Script..." -ForegroundColor Yellow
    
    if (!(Test-Path ".env.production")) {
        Write-Error "Deployment requires .env.production! Please create it first."
        Write-Host "You can copy .env.example to .env.production and fill in the details."
        Pause
        return
    }

    # Check for Paramiko
    $ParamikoCheck = uv run python -c "import paramiko" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Required library 'paramiko' not found!"
        Write-Host "Please run option '4. Install Dependencies' first."
        Pause
        return
    }

    if (Test-Path "scripts\deploy.ps1") {
        & "scripts\deploy.ps1"
    }
    else {
        Write-Error "scripts\deploy.ps1 not found!"
    }
    Write-Host ""
    Pause
}

function Run-Quickstart {
    Clear-Host
    Write-Host "Launching Quickstart..." -ForegroundColor Yellow
    if (Test-Path "scripts\docker-quickstart.ps1") {
        & "scripts\docker-quickstart.ps1"
    }
    else {
        Write-Error "scripts\docker-quickstart.ps1 not found!"
    }
    Write-Host ""
    Pause
}

function Run-Install {
    Clear-Host
    Write-Host "Installing Dependencies..." -ForegroundColor Yellow
    if (Test-Path "scripts\install.ps1") {
        & "scripts\install.ps1"
    }
    else {
        Write-Error "scripts\install.ps1 not found!"
    }
    Write-Host ""
    Pause
}

function Run-Secret {
    Clear-Host
    Write-Host "Generating Secret Key..." -ForegroundColor Yellow
    uv run python scripts\generate_secret.py
    Write-Host ""
    Pause
}

function Run-CLI {
    Clear-Host
    uv run python cli.py --help
    Write-Host ""
    Pause
}

# Main Loop
while ($true) {
    Show-Menu
    $choice = Read-Host "Select an option [0-6]"
    
    switch ($choice) {
        "1" { Run-Start }
        "2" { Run-Deploy }
        "3" { Run-Quickstart }
        "4" { Run-Install }
        "5" { Run-Secret }
        "6" { Run-CLI }
        "0" { Write-Host "Goodbye!"; exit }
        default { 
            Write-Warning "Invalid option. Please try again."
            Start-Sleep -Seconds 2
        }
    }
}
