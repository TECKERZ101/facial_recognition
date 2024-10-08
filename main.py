import importlib.util
import subprocess

deepfaceKnownInstalled = False
scwKnownInstalled = False

packagesNeeded = ["deepface", "simplecamerawidget"]

for package in packagesNeeded:
    try:
        spec = importlib.util.find_spec(package)
        if spec is None:
            raise ImportError(f"{package} is not installed")
    except ImportError:
        try:
            subprocess.run(["pip", "install", package], check=True)
            print(f"{package} has been installed successfully.")
            if package == "deepface":
                deepfaceKnownInstalled = True
            elif package == "simplecamerawidget":
                scwKnownInstalled = True
            else:
                quit("Import Error: 20")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}.")
            exit("Load Error: 10")

if deepfaceKnownInstalled == True and scwKnownInstalled = True:
    subprocess.run(["python", "recognition.py"], check=True)
else:
    quit("Load Error: 11")