
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import cv2
import time
import os


# --- Dark mode colors ---
BG_COLOR = "#23272e"
FG_COLOR = "#f5f6fa"
BTN_BG = "#2f3640"
BTN_FG = "#f5f6fa"
BTN_ACTIVE_BG = "#353b48"
BTN_ACTIVE_FG = "#dcdde1"

class CameraApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Live Camera View")
        # Set a larger window size and minimum size
        self.master.geometry("800x650")
        self.master.minsize(800, 650)
        self.master.configure(bg=BG_COLOR)

        # Load Roboto font if available
        font_path = os.path.join(os.path.dirname(__file__), "font", "Roboto-Regular.ttf")
        if os.path.exists(font_path):
            try:
                self.master.tk.call('font', 'create', 'Roboto', '-family', 'Roboto', '-size', '12', '-weight', 'normal')
                label_font = tkfont.Font(root=self.master, family="Roboto", size=16, weight="bold")
                btn_font = tkfont.Font(root=self.master, family="Roboto", size=12)
            except Exception:
                label_font = ("Arial", 16, "bold")
                btn_font = ("Arial", 12)
        else:
            label_font = ("Arial", 16, "bold")
            btn_font = ("Arial", 12)

        # Frame for camera image
        self.image_frame = tk.Frame(self.master, bg=BG_COLOR)
        self.image_frame.pack(pady=(20, 10), fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.image_frame, bg=BG_COLOR)
        self.label.pack(expand=True)

        self.capture = cv2.VideoCapture(0)
        self.update_frame()

        # Frame for button
        self.button_frame = tk.Frame(self.master, bg=BG_COLOR)
        self.button_frame.pack(pady=(0, 30))

        self.button = tk.Button(
            self.button_frame,
            text="Take Photo",
            command=self.take_photo,
            font=btn_font,
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_ACTIVE_BG,
            activeforeground=BTN_ACTIVE_FG,
            bd=0,
            highlightthickness=0,
            width=20
        )
        self.button.pack()

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)


    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2_im)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.config(image=imgtk)
            self.label.image = imgtk
        self.master.after(15, self.update_frame)


    def take_photo(self):
        ret, frame = self.capture.read()
        if ret:
            cv2.imwrite("img.jpg", frame)
            tim = time.time()
            archive_dir = "archive"
            if not os.path.exists(archive_dir):
                os.makedirs(archive_dir)
            fileName = os.path.join(archive_dir, f"{tim}.jpg")
            cv2.imwrite(fileName, frame)
            print("Photo saved as img.jpg")
            self.cleanup()
            self.master.quit()

    def on_close(self):
        self.cleanup()
        self.master.destroy()

    def cleanup(self):
        if hasattr(self, 'capture') and self.capture.isOpened():
            self.capture.release()


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("logo.ico")
    camera_app = CameraApp(root)
    root.mainloop()
