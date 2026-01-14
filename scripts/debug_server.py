import paramiko
import os
from dotenv import load_dotenv

load_dotenv('.env.production')

HOST = os.getenv('DEPLOY_HOST')
USER = os.getenv('DEPLOY_USER')
PASS = os.getenv('DEPLOY_PASS')

def debug():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, (22), username=USER, password=PASS)

    commands = [
        "echo '--- NGINX STATUS ---'",
        "systemctl status nginx --no-pager",
        "echo '--- NGINX ERROR LOGS ---'",
        "journalctl -u nginx --no-pager | tail -n 20",
        "echo '--- APP CONNECTIVITY CHECK ---'",
        "curl -v http://localhost:5000/health || echo 'Curl failed'",
        "echo '--- DOCKER CONTAINERS ---'",
        "docker ps -a"
    ]

    with open('debug_log.txt', 'w', encoding='utf-8') as f:
        for cmd in commands:
            f.write(f"\n=== Executing: {cmd} ===\n")
            stdin, stdout, stderr = client.exec_command(cmd)
            out = stdout.read().decode()
            err = stderr.read().decode()
            f.write(out)
            if err:
                f.write(f"STDERR: {err}\n")
            print(f"Executed {cmd}")

    client.close()

if __name__ == "__main__":
    debug()
