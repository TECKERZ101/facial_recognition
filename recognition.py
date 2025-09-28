import threading
import tkinter as tk
from tkinter import ttk, messagebox
from deepface import DeepFace

def analyze_face(progress, status_label, root):
	try:
		status_label.config(text="Analyzing image...")
		progress['value'] = 20
		root.update_idletasks()
		objs = DeepFace.analyze(
			img_path="img.jpg",
			actions=['age', 'gender', 'emotion'],
		)
		progress['value'] = 90
		root.update_idletasks()
		item = objs[0]
		gender_dict = item['gender']
		dominant_gender = item['dominant_gender']
		age = item['age']
		dominant_emotion = item['dominant_emotion']
		result = f"Age: {age}\nEmotion: {dominant_emotion}\nGender: {dominant_gender}"
		progress['value'] = 100
		status_label.config(text="Analysis complete.")
		root.update_idletasks()
		show_result(root, result)
	except Exception as e:
		messagebox.showerror("Error", f"An error occurred during analysis:\n{e}")
		root.destroy()

def show_result(root, result):
	# Custom styled result window
	result_win = tk.Toplevel(root)
	result_win.iconbitmap("logo.ico")
	result_win.title("Facial Recognition Results")
	result_win.geometry("350x200")
	result_win.configure(bg="#23272e")
	label = tk.Label(result_win, text="Recognition Results", font=("Arial", 16, "bold"), bg="#23272e", fg="#f5f6fa")
	label.pack(pady=(18, 8))
	result_label = tk.Label(result_win, text=result, font=("Arial", 13), bg="#23272e", fg="#f5f6fa", justify="left")
	result_label.pack(pady=(0, 18))
	ok_btn = tk.Button(result_win, text="OK", command=lambda: (result_win.destroy(), root.destroy()),
					  font=("Arial", 12), bg="#2f3640", fg="#f5f6fa", activebackground="#353b48", activeforeground="#dcdde1", bd=0, highlightthickness=0, width=10)
	ok_btn.pack()
	result_win.transient(root)
	result_win.grab_set()
	result_win.focus_set()

def main():
	root = tk.Tk()
	root.title("Facial Recognition Progress")
	root.iconbitmap("logo.ico")
	root.geometry("350x160")
	root.configure(bg="#23272e")

	label = tk.Label(root, text="Analyzing face...", font=("Arial", 15, "bold"), bg="#23272e", fg="#f5f6fa")
	label.pack(pady=(20, 10))

	progress = ttk.Progressbar(root, orient="horizontal", length=250, mode="determinate")
	progress.pack(pady=10)
	progress['value'] = 0
	progress['maximum'] = 100

	status_label = tk.Label(root, text="", font=("Arial", 11), bg="#23272e", fg="#f5f6fa")
	status_label.pack(pady=(10, 0))

	threading.Thread(target=analyze_face, args=(progress, status_label, root), daemon=True).start()
	root.mainloop()

if __name__ == "__main__":
	main()