
import tkinter as tk
from tkinter import scrolledtext
import time
import requests
from PIL import Image, ImageTk
import io

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Timer")
        self.root.geometry("500x600")

        self.start_time = None
        self.running = False
        self.lap_counter = 0
        self.after_id = None

        # --- Background Image ---
        self.canvas = tk.Canvas(root, width=500, height=600)
        self.canvas.pack(fill="both", expand=True)

        try:
            image_url = "https://source.unsplash.com/random/500x600/?nature"
            response = requests.get(image_url)
            image_data = response.content
            self.bg_image = Image.open(io.BytesIO(image_data))
            self.bg_photo_image = ImageTk.PhotoImage(self.bg_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo_image)
        except requests.exceptions.RequestException as e:
            print(f"Could not download background image: {e}")
            self.canvas.configure(bg="#f0f0f0") # Fallback color

        # --- Main Frame with "Frosted Glass" effect ---
        # Tkinter doesn't have backdrop-filter, so we use a semi-transparent frame
        main_frame = tk.Frame(self.canvas, bg='#ffffff', bd=0)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)
        main_frame.config(bg='#DDDDDD') # A light grey fallback
        if 'system' in dir(main_frame): # More robust check for tk transparency
             main_frame.tk.call('wm', 'attributes', '.', '-transparentcolor', main_frame['bg'])


        # --- Widgets on the main_frame ---
        self.display_var = tk.StringVar(value="00:00:00.000")
        self.display_label = tk.Label(main_frame, textvariable=self.display_var, font=("Arial", 40), bg="#DDDDDD", fg="#333")
        self.display_label.pack(pady=(40, 20))

        controls_frame = tk.Frame(main_frame, bg="#DDDDDD")
        controls_frame.pack(pady=10)

        self.start_stop_btn = tk.Button(controls_frame, text="Start", width=10, command=self.toggle_start_stop, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.start_stop_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(controls_frame, text="Reset", width=10, command=self.reset, bg="#f44336", fg="white", font=("Arial", 12))
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        self.lap_btn = tk.Button(controls_frame, text="Lap", width=10, command=self.lap, bg="#2196F3", fg="white", font=("Arial", 12))
        self.lap_btn.pack(side=tk.LEFT, padx=5)

        self.laps_text = scrolledtext.ScrolledText(main_frame, width=35, height=10, font=("Arial", 12), state="disabled", relief="flat", bd=0)
        self.laps_text.pack(pady=10)


    def toggle_start_stop(self):
        if self.running:
            self.running = False
            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None
            self.start_stop_btn.config(text="Start", bg="#4CAF50")
        else:
            self.running = True
            self.start_stop_btn.config(text="Stop", bg="#FFA500")
            if self.start_time is None:
                self.start_time = time.time() - (self.last_elapsed if hasattr(self, 'last_elapsed') else 0)
            else: # Resuming
                self.start_time = time.time() - self.last_elapsed
            self.update_time()

    def reset(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.running = False
        self.start_time = None
        self.last_elapsed = 0
        self.lap_counter = 0
        self.display_var.set("00:00:00.000")
        self.start_stop_btn.config(text="Start", bg="#4CAF50")
        self.laps_text.config(state="normal")
        self.laps_text.delete(1.0, tk.END)
        self.laps_text.config(state="disabled")

    def lap(self):
        if self.running:
            self.lap_counter += 1
            lap_time = self.display_var.get()
            self.laps_text.config(state="normal")
            self.laps_text.insert(tk.END, f"Lap {self.lap_counter}: {lap_time}\n")
            self.laps_text.config(state="disabled")
            self.laps_text.see(tk.END)

    def update_time(self):
        if self.running:
            self.last_elapsed = time.time() - self.start_time
            hours, rem = divmod(self.last_elapsed, 3600)
            minutes, seconds = divmod(rem, 60)
            milliseconds = int((seconds - int(seconds)) * 1000)

            self.display_var.set(f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{milliseconds:03d}")
            self.after_id = self.root.after(50, self.update_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
