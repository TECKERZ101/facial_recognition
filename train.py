import tkinter as tk
from tkinter import messagebox, font as tkfont
from PIL import Image, ImageTk
import cv2
import os
import time

BG_COLOR = "#23272e"
FG_COLOR = "#f5f6fa"
FRAME_BG = "#2f3640"

class TrainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Add New Face to Database")
        self.master.geometry("700x600")
        self.master.configure(bg=BG_COLOR)

        # Load Roboto font if available
        font_path = os.path.join(os.path.dirname(__file__), "font", "Roboto-Regular.ttf")
        if os.path.exists(font_path):
            try:
                self.master.tk.call('font', 'create', 'Roboto', '-family', 'Roboto', '-size', '12', '-weight', 'normal')
                title_font = tkfont.Font(root=self.master, family="Roboto", size=18, weight="bold")
                label_font = tkfont.Font(root=self.master, family="Roboto", size=13)
                btn_font = tkfont.Font(root=self.master, family="Roboto", size=12)
            except Exception:
                title_font = ("Arial", 18, "bold")
                label_font = ("Arial", 13)
                btn_font = ("Arial", 12)
        else:
            title_font = ("Arial", 18, "bold")
            label_font = ("Arial", 13)
            btn_font = ("Arial", 12)

        self.title_label = tk.Label(master, text="Add New Face to Database", font=title_font, bg=BG_COLOR, fg=FG_COLOR)
        self.title_label.pack(pady=(18, 8))

        self.video_frame = tk.Frame(master, bg=FRAME_BG)
        self.video_frame.pack(pady=(0, 10), padx=10)

        self.image_label = tk.Label(self.video_frame, bg=FRAME_BG)
        self.image_label.pack()

        entry_frame = tk.Frame(master, bg=BG_COLOR)
        entry_frame.pack(pady=(10, 0))

        self.name_label = tk.Label(entry_frame, text="Name:", font=label_font, bg=BG_COLOR, fg=FG_COLOR)
        self.name_label.pack(side=tk.LEFT, padx=(0, 8))

        self.name_entry = tk.Entry(entry_frame, font=label_font, width=24)
        self.name_entry.pack(side=tk.LEFT)

        self.capture_btn = tk.Button(
            master,
            text="Take Photo",
            command=self.take_photo,
            font=btn_font,
            bg=FRAME_BG,
            fg=FG_COLOR,
            activebackground="#353b48",
            activeforeground="#dcdde1",
            bd=0,
            highlightthickness=0,
            width=18
        )
        self.capture_btn.pack(pady=18)

        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.current_frame = None

        self.update_video()
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_video(self):
        if not self.running:
            return
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame
            display_frame = cv2.resize(frame, (480, 360))
            rgb_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.image_label.imgtk = imgtk
            self.image_label.configure(image=imgtk)
        self.master.after(30, self.update_video)

    def take_photo(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Required", "Please enter a name before taking a photo.")
            return
        if self.current_frame is None:
            messagebox.showerror("Camera Error", "No camera frame available.")
            return
        save_dir = os.path.join("database", name)
        os.makedirs(save_dir, exist_ok=True)
        timestamp = int(time.time())
        filename = os.path.join(save_dir, f"{timestamp}.jpg")
        cv2.imwrite(filename, self.current_frame)
        messagebox.showinfo("Photo Saved", f"Photo saved to:\n{filename}")

    def on_close(self):
        self.running = False
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("logo.ico")
    app = TrainApp(root)
    root.mainloop()