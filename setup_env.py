#!/usr/bin/env python3
"""
Create a virtual environment for the sentiment analysis project and install
the required packages.

Usage:
    python setup_env.py
"""
import platform
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
VENV_DIR = PROJECT_DIR / ".venv"

# The planned TF-IDF + LinearSVC model and the rule-based layer run on the CPU
# through scikit-learn, so no GPU-specific packages are needed.
PACKAGES = [
    "numpy",
    "pandas",
    "scikit-learn",
    "matplotlib",
    "nltk",
    "jupyter",
]


def venv_python():
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def run(cmd):
    print("+", " ".join(str(c) for c in cmd), flush=True)
    subprocess.run(cmd, check=True)


def main():
    if not VENV_DIR.exists():
        print(f"Creating virtual environment at {VENV_DIR}")
        run([sys.executable, "-m", "venv", str(VENV_DIR)])
    else:
        print(f"Using existing virtual environment at {VENV_DIR}")

    py = str(venv_python())
    run([py, "-m", "pip", "install", "--upgrade", "pip"])
    run([py, "-m", "pip", "install", *PACKAGES])

    # Record the exact versions so the environment can be rebuilt later.
    lock_file = PROJECT_DIR / "requirements-lock.txt"
    with open(lock_file, "w") as f:
        subprocess.run([py, "-m", "pip", "freeze"], stdout=f, check=True)
    print(f"Wrote {lock_file.name}")

    if platform.system() == "Windows":
        activate = r".venv\Scripts\activate"
    else:
        activate = "source .venv/bin/activate"
    print("\nSetup complete. Activate the environment with:")
    print(f"  {activate}")


if __name__ == "__main__":
    main()
