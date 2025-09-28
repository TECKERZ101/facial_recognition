deepfaceKnownInstalled = False
import importlib.util
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import ttk

packagesNeeded = ["pillow", "deepface", "tf-keras", "opencv-python"]

class SetupApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Setup - Installing Packages")
        self.master.geometry("420x200")
        self.master.configure(bg="#23272e")

        self.label = tk.Label(master, text="Installing required packages...", font=("Arial", 14, "bold"), bg="#23272e", fg="#f5f6fa")
        self.label.pack(pady=(20, 10))

        self.progress = ttk.Progressbar(master, orient="horizontal", length=350, mode="determinate")
        self.progress.pack(pady=10)
        self.progress['maximum'] = len(packagesNeeded)

        self.status = tk.Label(master, text="", font=("Arial", 11), bg="#23272e", fg="#f5f6fa")
        self.status.pack(pady=(10, 0))

        self.done = False
        threading.Thread(target=self.install_packages, daemon=True).start()

    def install_packages(self):
        for idx, package in enumerate(packagesNeeded, 1):
            self.status.config(text=f"Checking {package}...")
            self.progress['value'] = idx - 1
            self.master.update_idletasks()
            try:
                spec = importlib.util.find_spec(package)
                if spec is not None:
                    self.status.config(text=f"{package} already installed.")
                else:
                    raise ImportError
            except ImportError:
                self.status.config(text=f"Installing {package}...")
                self.master.update_idletasks()
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
                    self.status.config(text=f"{package} installed successfully.")
                except subprocess.CalledProcessError:
                    self.status.config(text=f"Failed to install {package}.")
                    self.progress['value'] = idx
                    self.master.update_idletasks()
                    return
            self.progress['value'] = idx
            self.master.update_idletasks()
        self.status.config(text="All packages installed.")
        self.done = True
        self.master.after(1200, self.master.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("logo.ico")
    app = SetupApp(root)
    root.mainloop()