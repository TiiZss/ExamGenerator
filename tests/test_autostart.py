# Script para probar auto-inicio de Ollama
import subprocess
import sys

print("🧪 PROBANDO AUTO-INICIO DE OLLAMA")
print("=" * 60)
print()

# Ejecutar qg.py y simular respuesta 's'
process = subprocess.Popen(
    [sys.executable, "qg.py", "documento_ia.docx", "--motor", "ollama", "--modelo", "gemma3:4b", "--num_preguntas", "3"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

# Dar tiempo para que inicie
import time
output_lines = []

# Leer salida línea por línea
try:
    for line in iter(process.stdout.readline, ''):
        if not line:
            break
        print(line, end='')
        output_lines.append(line)
        
        # Si encuentra la pregunta de auto-inicio, responder 's'
        if "automáticamente?" in line.lower() and "s/n" in line.lower():
            print("s")  # Mostrar que enviamos 's'
            process.stdin.write("s\n")
            process.stdin.flush()
            
except KeyboardInterrupt:
    process.terminate()
    print("\n⚠️ Proceso interrumpido")

process.wait()

print()
print("=" * 60)
print("✅ Prueba completada")
print(f"Código de salida: {process.returncode}")
