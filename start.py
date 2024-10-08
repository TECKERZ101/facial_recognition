import importlib.util
import subprocess

deepfaceKnownInstalled = False
pillowKnownInstalled = False

packagesNeeded = ["pillow", "deepface"]

for package in packagesNeeded:
    try:
        spec = importlib.util.find_spec(package)
        if spec is None:
            raise ImportError(f"{package} is not installed")
        elif spec is not None:
            raise ImportError(f"{package} is installed")
    except ImportError:
        try:
            subprocess.run(["pip", "install", package], check=True)
            print(f"{package} has been installed successfully.")
            if package == "deepface":
                deepfaceKnownInstalled = True
            elif package == "pillow":
                pillowKnownInstalled = True
            else:
                quit("Import Error: 20")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}.")
            exit("Load Error: 10")

if deepfaceKnownInstalled == True and pillowKnownInstalled == True:
    try:
        subprocess.run(["python", "main.py"], check=True)
    except subprocess.CalledProcessError:
        print("Subprocess Error: 30")
else:
    quit("Load Error: 11")