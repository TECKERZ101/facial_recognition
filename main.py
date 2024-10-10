import subprocess

try:
    subprocess.run(["python", "photo.py"], check=True)
    subprocess.run(["python", "recognition.py"], check=True)
except subprocess.CalledProcessError:
    print("Failed to run a program.")
    quit("Module error 40")