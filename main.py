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
            subprocess.run(["python", "p1.py"], check=True)
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}.")

check_and_install("deepface")
