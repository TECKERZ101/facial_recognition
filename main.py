import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
import os

def capture_and_recognize():
    try:
        subprocess.run(["python", "photo.py"], check=True)
        subprocess.run(["python", "recognition.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def recognize_face():
    try:
        subprocess.run(["python", "recognition.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def live_analysis():
    try:
        subprocess.run(["python", "live.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def setup():
    try:
        subprocess.run(["python", "setup.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def exit_program():
    root.destroy()

# --- Dark mode colors ---
BG_COLOR = "#23272e"
FG_COLOR = "#f5f6fa"
BTN_BG = "#2f3640"
BTN_FG = "#f5f6fa"
BTN_ACTIVE_BG = "#353b48"
BTN_ACTIVE_FG = "#dcdde1"


root = tk.Tk()
root.title("Facial Recognition")
root.iconbitmap("logo.ico")
root.geometry("370x370")
root.configure(bg=BG_COLOR)

# --- Load Roboto font (after root is created) ---
font_path = os.path.join(os.path.dirname(__file__), "font", "Roboto-Regular.ttf")
if os.path.exists(font_path):
    try:
        root.tk.call('font', 'create', 'Roboto', '-family', 'Roboto', '-size', '12', '-weight', 'normal')
        title_font = tkfont.Font(root=root, family="Roboto", size=18, weight="bold")
        btn_font = tkfont.Font(root=root, family="Roboto", size=12)
        tkfont.nametofont("TkDefaultFont").configure(family="Roboto")
    except Exception:
        title_font = ("Arial", 18, "bold")
        btn_font = ("Arial", 12)
else:
    title_font = ("Arial", 18, "bold")
    btn_font = ("Arial", 12)

title_label = tk.Label(root, text="Facial Recognition", font=title_font, bg=BG_COLOR, fg=FG_COLOR)
title_label.pack(pady=15)

menu_frame = tk.Frame(root, bg=BG_COLOR)
menu_frame.pack(pady=20)

btn1 = tk.Button(menu_frame, text="Capture Photo & Recognize", width=25, command=capture_and_recognize,
                 font=btn_font, bg=BTN_BG, fg=BTN_FG, activebackground=BTN_ACTIVE_BG, activeforeground=BTN_ACTIVE_FG, bd=0, highlightthickness=0)
btn1.pack(pady=7)

btn2 = tk.Button(menu_frame, text="Recognize Face", width=25, command=recognize_face,
                 font=btn_font, bg=BTN_BG, fg=BTN_FG, activebackground=BTN_ACTIVE_BG, activeforeground=BTN_ACTIVE_FG, bd=0, highlightthickness=0)
btn2.pack(pady=7)

# --- New Live Analysis Button ---
btn_live = tk.Button(menu_frame, text="Live Analysis", width=25, command=live_analysis,
                     font=btn_font, bg=BTN_BG, fg=BTN_FG, activebackground=BTN_ACTIVE_BG, activeforeground=BTN_ACTIVE_FG, bd=0, highlightthickness=0)
btn_live.pack(pady=7)

btn3 = tk.Button(menu_frame, text="Setup", width=25, command=setup,
                 font=btn_font, bg=BTN_BG, fg=BTN_FG, activebackground=BTN_ACTIVE_BG, activeforeground=BTN_ACTIVE_FG, bd=0, highlightthickness=0)
btn3.pack(pady=7)

btn4 = tk.Button(menu_frame, text="Exit", width=25, command=exit_program,
                 font=btn_font, bg=BTN_BG, fg=BTN_FG, activebackground=BTN_ACTIVE_BG, activeforeground=BTN_ACTIVE_FG, bd=0, highlightthickness=0)
btn4.pack(pady=7)

root.mainloop()