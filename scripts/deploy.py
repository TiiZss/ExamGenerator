import os
import sys
import tarfile
import paramiko
import time
import urllib.request
import ssl
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.production')

DEPLOY_HOST = os.getenv('DEPLOY_HOST')
DEPLOY_USER = os.getenv('DEPLOY_USER')
DEPLOY_PASS = os.getenv('DEPLOY_PASS')
DOMAIN_NAME = os.getenv('DOMAIN_NAME')
LETSENCRYPT_EMAIL = os.getenv('LETSENCRYPT_EMAIL')

if not all([DEPLOY_HOST, DEPLOY_USER, DEPLOY_PASS, DOMAIN_NAME]):
    print("Error: Missing required deployment variables in .env.production")
    sys.exit(1)

REMOTE_DIR = f"/var/www/{DOMAIN_NAME}"
DEPLOY_PACKAGE = "deploy_package.tar.gz"

def create_package():
    print(f"Compressing files into {DEPLOY_PACKAGE}...")
    with tarfile.open(DEPLOY_PACKAGE, "w:gz") as tar:
        for item in os.listdir('.'):
            if item in ['.git', 'output', '__pycache__', '.venv', '.vscode', DEPLOY_PACKAGE]:
                continue
            if item.endswith('.tar.gz'):
                continue
            tar.add(item, arcname=item)

def deploy():
    try:
        # Create SSH Client
        print(f"Connecting to {DEPLOY_USER}@{DEPLOY_HOST}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(DEPLOY_HOST, username=DEPLOY_USER, password=DEPLOY_PASS)

        # SFTP Client for Upload
        sftp = ssh.open_sftp()
        
        # Upload Package
        print(f"Uploading {DEPLOY_PACKAGE}...")
        try:
            sftp.stat(REMOTE_DIR)
        except FileNotFoundError:
            print(f"Creating remote directory {REMOTE_DIR}...")
            # Simple recursive mkdir not available in sftp, executing command instead
            ssh.exec_command(f"sudo mkdir -p {REMOTE_DIR} && sudo chown {DEPLOY_USER}:{DEPLOY_USER} {REMOTE_DIR}")

        sftp.put(DEPLOY_PACKAGE, f"{REMOTE_DIR}/{DEPLOY_PACKAGE}")
        sftp.close()

        # Remote Execution
        remote_script = f"""
set -e
export DEPLOY_USER={DEPLOY_USER}
export DOMAIN_NAME={DOMAIN_NAME}
export LETSENCRYPT_EMAIL={LETSENCRYPT_EMAIL}
export REMOTE_DIR={REMOTE_DIR}

# 1. Install System Dependencies & Docker
echo "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    echo "{DEPLOY_PASS}" | sudo -S usermod -aG docker {DEPLOY_USER}
fi

echo "Installing Nginx and Certbot..."
echo "{DEPLOY_PASS}" | sudo -S apt-get update
echo "{DEPLOY_PASS}" | sudo -S apt-get install -y nginx certbot python3-certbot-nginx acl

# 2. Setup Directory Permissions
echo "{DEPLOY_PASS}" | sudo -S chown -R {DEPLOY_USER}:{DEPLOY_USER} {REMOTE_DIR}

# Unpacking
echo "Unpacking..."
cd {REMOTE_DIR}
tar -xzf {DEPLOY_PACKAGE}
rm {DEPLOY_PACKAGE}

# Ensure output directory exists (excluded from tar)
mkdir -p output logs config
chmod 777 output logs config

echo "🔍 DEBUG: Verifying Dockerfile content..."
grep "COPY" Dockerfile || true

echo "Cleaning Docker Builder Cache..."
echo "{DEPLOY_PASS}" | sudo -S docker builder prune -f

# 3. Nginx
echo "Configuring Nginx..."

# Ensure Port 80 is free for Nginx
echo "Cleaning up potential conflicts..."
echo "{DEPLOY_PASS}" | sudo -S rm -f /etc/nginx/sites-enabled/default
echo "{DEPLOY_PASS}" | sudo -S systemctl stop apache2 2>/dev/null || true

echo "{DEPLOY_PASS}" | sudo -S cp {REMOTE_DIR}/nginx_examgenerator.conf /etc/nginx/sites-available/{DOMAIN_NAME}
if [ ! -e /etc/nginx/sites-enabled/{DOMAIN_NAME} ]; then
    echo "{DEPLOY_PASS}" | sudo -S ln -s /etc/nginx/sites-available/{DOMAIN_NAME} /etc/nginx/sites-enabled/
fi
echo "{DEPLOY_PASS}" | sudo -S nginx -t

# Try reload, if fails (e.g. stopped), try start
if ! echo "{DEPLOY_PASS}" | sudo -S systemctl reload nginx 2>/dev/null; then
    echo "Nginx reload failed, attempting to start..."
    if ! echo "{DEPLOY_PASS}" | sudo -S systemctl enable --now nginx; then
        echo "❌ Nginx failed to start! Debugging..."
        echo "{DEPLOY_PASS}" | sudo -S systemctl status nginx --no-pager -l
        echo "{DEPLOY_PASS}" | sudo -S journalctl -xeu nginx --no-pager | tail -n 20
        # Don't exit yet, try to launch docker anyway so the backend at least runs
    fi
else
    echo "Nginx reloaded successfully."
fi

# 4. SSL
echo "Setting up SSL..."
# Check if we need to obtain certs OR reinstall SSL config
NEEDS_SSL=0
if ! echo "{DEPLOY_PASS}" | sudo -S certbot certificates | grep -q "{DOMAIN_NAME}"; then
    echo "Certificate missing, obtaining..."
    NEEDS_SSL=1
elif ! grep -q "ssl_certificate" /etc/nginx/sites-enabled/{DOMAIN_NAME}; then
    echo "Certificate exists but Nginx config missing SSL, reinstalling..."
    NEEDS_SSL=1
fi

if [ "$NEEDS_SSL" -eq "1" ]; then
    echo "{DEPLOY_PASS}" | sudo -S certbot --nginx -d {DOMAIN_NAME} --non-interactive --agree-tos -m {LETSENCRYPT_EMAIL} --redirect
else
    echo "SSL already configured."
fi

# 5. Docker Stack
echo "Launching Docker Stack..."
cp .env.production .env

# Force rebuild to ensure changes are picked up
if docker compose version >/dev/null 2>&1; then
    docker compose up -d --build --remove-orphans
else
    # Fallback for older docker-compose
    docker-compose up -d --build --remove-orphans
fi

echo "Pruning..."
docker image prune -f
"""
        print("Executing remote setup...")
        # Use a safer way to execute large scripts: write to stdin of bash
        stdin, stdout, stderr = ssh.exec_command("bash -s")
        stdin.write(remote_script)
        stdin.channel.shutdown_write()
        
        # Stream output
        for line in stdout:
            print(line.strip())
        
        # Check errors
        exit_status = stdout.channel.recv_exit_status()
        if exit_status != 0:
            print("Error executing remote script:")
            print(stderr.read().decode())
            sys.exit(exit_status)
            
        # 6. Post-Deployment Health Check
        print("\nRunning Health Check...")
        time.sleep(5) # Give it a moment to reload
        
        target_url = f"https://{DOMAIN_NAME}/health"
        
        check_passed = False
        for i in range(12): # Try for 60 seconds (12 * 5s)
            try:
                print(f"Checking {target_url} (Attempt {i+1}/12)...")
                # Context to ignore SSL errors if using self-signed or fresh certs
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                
                req = urllib.request.Request(
                    target_url, 
                    headers={'User-Agent': 'ExamGenerator-DeployBot'}
                )
                
                with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                    if response.status == 200:
                        print(f"✅ SUCCESS: Site is UP and returned 200 OK!")
                        check_passed = True
                        break
                    else:
                        print(f"⚠️  warning: Site returned status {response.status}")
            except Exception as e:
                print(f"⏳ Waiting for site... ({e})")
            
            time.sleep(5)
            
        if not check_passed:
            print(f"❌ ERROR: Site did not come online at {target_url} after 60 seconds.")
            print("\n🔍 Debugging: Fetching Remote Logs...")
            
            print("\n--- Nginx Status ---")
            stdin, stdout, stderr = ssh.exec_command("systemctl status nginx --no-pager")
            print(stdout.read().decode())
            print(stderr.read().decode())

            print("\n--- Docker Logs (tail) ---")
            stdin, stdout, stderr = ssh.exec_command(f"cd {REMOTE_DIR} && docker compose logs --tail=50")
            print(stdout.read().decode())
            print(stderr.read().decode())
            
            print("\n--- Docker Containers ---")
            stdin, stdout, stderr = ssh.exec_command(f"cd {REMOTE_DIR} && docker compose ps -a")
            print(stdout.read().decode())
        else:
            print("🚀 Deployment Verified Successfully!")

    except Exception as e:
        print(f"Deployment Failed: {e}")
        sys.exit(1)
    finally:
        if 'ssh' in locals() and ssh:
            ssh.close()
        if os.path.exists(DEPLOY_PACKAGE):
            os.remove(DEPLOY_PACKAGE)

if __name__ == "__main__":
    create_package()
    deploy()
