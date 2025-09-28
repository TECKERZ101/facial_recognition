import cv2
import threading
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
from deepface import DeepFace
import os

DB_PATH = "database/"

BG_COLOR = "#23272e"
FG_COLOR = "#f5f6fa"
FRAME_BG = "#2f3640"

class LiveAnalysisApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Live Face Recognition & Attribute Analysis")
        self.master.geometry("900x700")
        self.master.configure(bg=BG_COLOR)

        # Load Roboto font if available
        font_path = os.path.join(os.path.dirname(__file__), "font", "Roboto-Regular.ttf")
        if os.path.exists(font_path):
            try:
                self.master.tk.call('font', 'create', 'Roboto', '-family', 'Roboto', '-size', '12', '-weight', 'normal')
                title_font = tkfont.Font(root=self.master, family="Roboto", size=18, weight="bold")
                attr_font = tkfont.Font(root=self.master, family="Roboto", size=14)
            except Exception:
                title_font = ("Arial", 18, "bold")
                attr_font = ("Arial", 14)
        else:
            title_font = ("Arial", 18, "bold")
            attr_font = ("Arial", 14)

        self.title_label = tk.Label(master, text="Live Face Recognition & Attribute Analysis", font=title_font, bg=BG_COLOR, fg=FG_COLOR)
        self.title_label.pack(pady=(18, 8))

        self.video_frame = tk.Frame(master, bg=FRAME_BG)
        self.video_frame.pack(pady=(0, 10), padx=10, fill=tk.BOTH, expand=True)

        self.image_label = tk.Label(self.video_frame, bg=FRAME_BG)
        self.image_label.pack()

        self.attr_label = tk.Label(master, text="", font=attr_font, bg=BG_COLOR, fg=FG_COLOR, justify="left")
        self.attr_label.pack(pady=(10, 0))

        self.cap = cv2.VideoCapture(0)
        self.running = True

        self.analysis_lock = threading.Lock()
        self.analysis_thread = None
        self.last_result = "Detecting..."

        self.update_video()
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_video(self):
        if not self.running:
            return
        ret, frame = self.cap.read()
        if ret:
            display_frame = cv2.resize(frame, (640, 480))
            rgb_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.image_label.imgtk = imgtk
            self.image_label.configure(image=imgtk)
            # Start analysis in a separate thread if not already running
            if self.analysis_thread is None or not self.analysis_thread.is_alive():
                self.analysis_thread = threading.Thread(target=self.analyze_frame, args=(frame.copy(),), daemon=True)
                self.analysis_thread.start()
        self.attr_label.config(text=self.last_result)
        self.master.after(60, self.update_video)

    def analyze_frame(self, frame):
        with self.analysis_lock:
            try:
                # Resize for faster analysis
                small_frame = cv2.resize(frame, (320, 240))
                result = DeepFace.find(
                    img_path = small_frame,
                    db_path = DB_PATH,
                    enforce_detection = False,
                    detector_backend = "opencv",
                    silent = True
                )
                # result is a list of DataFrames, one per model. We'll use VGG-Face (first)
                identity = "Unknown"
                if len(result) > 0 and not result[0].empty:
                    identity = os.path.basename(os.path.dirname(result[0].iloc[0]['identity']))
                # Now analyze attributes
                analysis = DeepFace.analyze(
                    small_frame,
                    actions=['age', 'gender', 'emotion'],
                    enforce_detection=False,
                    silent=True
                )
                if isinstance(analysis, list):
                    analysis = analysis[0]
                age = analysis.get('age', 'N/A')
                gender = analysis.get('dominant_gender', 'N/A')
                emotion = analysis.get('dominant_emotion', 'N/A')
                self.last_result = f"Identity: {identity}\nAge: {age}\nGender: {gender}\nEmotion: {emotion}"
            except Exception:
                self.last_result = "Face not detected"

    def on_close(self):
        self.running = False
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("logo.ico")
    app = LiveAnalysisApp(root)
    root.mainloop()