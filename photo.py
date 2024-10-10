import tkinter as tk
from PIL import Image, ImageTk
import cv2

class CameraApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Live Camera View")
        self.master.geometry("640x500") # 800x600

        self.label = tk.Label(self.master)
        self.label.pack()

        self.capture = cv2.VideoCapture(0)
        self.update_frame()

        self.button = tk.Button(self.master, text="Take Photo", command=self.take_photo)
        self.button.pack(pady=(10, 0))  # Add some padding above the button
        self.button.configure(bg="#4CAF50", fg="white")  # Change background color to green

        self.button.pack()

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2_im)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.config(image=imgtk)
            self.label.image = imgtk
        self.master.after(10, self.update_frame)

    def take_photo(self):
        ret, frame = self.capture.read()
        if ret:
            cv2.imwrite("img.jpg", frame)
            print("Photo saved as img.jpg")
            root.quit()

root = tk.Tk()
camera_app = CameraApp(root)
root.mainloop()
