# Deploy Script for ExamGenerator (Docker Version)
# Reads configuration from .env.production

$EnvFile = ".env.production"
if (!(Test-Path $EnvFile)) {
    Write-Error "File $EnvFile not found!"
    exit 1
}

# Parse .env file
Get-Content $EnvFile | ForEach-Object {
    if ($_ -match "^\s*([^#=]+)=(.*)$") {
        $Key = $matches[1].Trim()
        $Value = $matches[2].Trim()
        # Remove quotes if present
        $Value = $Value -replace '^["'']|["'']$'
        Set-Variable -Name $Key -Value $Value -Scope Script
    }
}

Write-Host "Deploying to $DEPLOY_USER@$DEPLOY_HOST (Docker Stack)..."
Write-Host "Domain: $DOMAIN_NAME"

$RemoteDir = "/var/www/$DOMAIN_NAME"

# Define commands to run on server
$RemoteScript = @"
set -e

# 1. Install System Dependencies & Docker
echo "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    sudo usermod -aG docker $DEPLOY_USER
fi

echo "Installing Nginx and Certbot..."
sudo apt-get update
sudo apt-get install -y nginx certbot python3-certbot-nginx acl

# 2. Setup Directory
echo "Setting up directories..."
sudo mkdir -p $RemoteDir
sudo chown -R ${DEPLOY_USER}:${DEPLOY_USER} $RemoteDir

# 3. Setup Nginx (Host Proxy)
echo "Configuring Host Nginx..."
sudo cp $RemoteDir/nginx_examgenerator.conf /etc/nginx/sites-available/$DOMAIN_NAME
if [ ! -e /etc/nginx/sites-enabled/$DOMAIN_NAME ]; then
    sudo ln -s /etc/nginx/sites-available/$DOMAIN_NAME /etc/nginx/sites-enabled/
fi
sudo nginx -t
sudo systemctl reload nginx

# 4. SSL Certificate (Certbot)
echo "Setting up SSL..."
if ! sudo certbot certificates | grep -q "$DOMAIN_NAME"; then
    sudo certbot --nginx -d $DOMAIN_NAME --non-interactive --agree-tos -m $LETSENCRYPT_EMAIL
fi

# 5. Launch Docker Stack
echo "Launching Docker Stack..."
cd $RemoteDir
# Ensure .env exists (copied from .env.production)
cp .env.production .env

# Pull/Build and Start
# Try 'docker compose' (v2) first, then 'docker-compose' (v1)
if docker compose version >/dev/null 2>&1; then
    docker compose up -d --build --remove-orphans
else
    docker-compose up -d --build --remove-orphans
fi

echo "Pruning unused images..."
docker image prune -f

echo "Deployment Complete! Check https://$DOMAIN_NAME"
"@

# Write remote script to a temp file
$TempScript = New-TemporaryFile
Set-Content -Path $TempScript.FullName -Value $RemoteScript

# 1. Copy Files
Write-Host "Copying files to server..."
# Files needed for Docker build and runtime
$FilesToSend = @(
    "examgenerator", 
    "scripts", 
    "templates", 
    "assets", 
    "requirements.txt", 
    "run_web.py", 
    "qg.py", 
    "eg.py", 
    "cli.py", 
    "config.yaml", 
    "Dockerfile", 
    "docker-compose.yml", 
    "nginx_examgenerator.conf", 
    "pyproject.toml", 
    "uv.lock",
    ".env.production"
)

# Use tar to zip and scp to avoid recursion issues if possible, 
# but simple loop is robust for small file sets on Windows without needing external tools.
foreach ($File in $FilesToSend) {
    if (Test-Path $File) {
        Write-Host "  Uploading $File..."
        scp -r $File "${DEPLOY_USER}@${DEPLOY_HOST}:${RemoteDir}/"
    }
}

# 2. Execute Remote Setup
Write-Host "Executing remote setup..."
Get-Content $TempScript.FullName | ssh "${DEPLOY_USER}@${DEPLOY_HOST}" "bash -s"

Remove-Item $TempScript.FullName
