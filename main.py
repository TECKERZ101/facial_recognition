import importlib.util
import sys
import os

import importlib.util
import subprocess

def check_and_install(package):
    try:
        spec = importlib.util.find_spec(package)
        if spec is None:
            raise ImportError(f"{package} is not installed")
    except ImportError:
        try:
            subprocess.run(["pip", "install", package], check=True)
            print(f"{package} has been installed successfully.")
            os.system("python p1.py")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}.")

check_and_install("deepface")
