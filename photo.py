import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import simplecamerawidget

def take_photo():
    try:
        # Capture the photo
        photo = simplecamerawidget.take_picture()
        
        # Convert the photo to a PIL Image
        pil_image = Image.frombytes("RGB", photo.size, photo.tobytes())
        
        # Save the image
        pil_image.save("img.jpg")
        messagebox.showinfo("Success", "Photo saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to capture or save photo: {str(e)}")

root = tk.Tk()
root.title("Photo Capture")

# Create a frame for the camera widget
camera_frame = tk.Frame(root)
camera_frame.pack()

# Add the camera widget
camera_widget = simplecamerawidget.CameraWidget(camera_frame)
camera_widget.pack()

# Create a button to trigger photo capture
capture_button = tk.Button(root, text="Capture Photo", command=take_photo)
capture_button.pack(pady=10)

root.mainloop()
