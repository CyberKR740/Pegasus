import subprocess
import sys

def install_dependences(package):
    print(f"Instalando {package}...")
    subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)