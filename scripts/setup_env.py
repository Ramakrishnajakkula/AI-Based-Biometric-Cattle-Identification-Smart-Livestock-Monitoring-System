"""
Environment Setup Script — Creates venvs and installs dependencies
Author: Team

Usage: python scripts/setup_env.py
"""

import subprocess
import sys
import os


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODULES = {
    "ml": os.path.join(ROOT, "ml", "requirements.txt"),
    "backend": os.path.join(ROOT, "backend", "requirements.txt"),
    "iot": os.path.join(ROOT, "iot", "requirements.txt"),
}


def setup_module(name: str, req_file: str):
    """Create venv and install requirements for a module."""
    venv_path = os.path.join(ROOT, name, "venv")
    
    if os.path.exists(venv_path):
        print(f"  [{name}] venv already exists, skipping creation")
    else:
        print(f"  [{name}] Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
    
    # Determine pip path
    pip = os.path.join(venv_path, "Scripts" if sys.platform == "win32" else "bin", "pip")
    
    print(f"  [{name}] Installing requirements...")
    subprocess.run([pip, "install", "-r", req_file], check=True)
    print(f"  [{name}] Done!")


def main():
    print("=== Cattle Monitoring — Environment Setup ===\n")
    
    # Install common requirements first
    common_req = os.path.join(ROOT, "requirements-common.txt")
    if os.path.exists(common_req):
        print("[common] Installing common requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", common_req], check=True)
    
    for name, req_file in MODULES.items():
        if os.path.exists(req_file):
            print(f"\n[{name}] Setting up...")
            setup_module(name, req_file)
        else:
            print(f"\n[{name}] requirements.txt not found, skipping")
    
    print("\n=== Setup complete! ===")
    print("Next steps:")
    print("  1. cd frontend && npm install")
    print("  2. docker-compose up -d")
    print("  3. Copy .env.example → .env and fill in values")


if __name__ == "__main__":
    main()
