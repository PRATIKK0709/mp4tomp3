import os
import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip
from tkinter import ttk
from threading import Thread
import time

def mp4_to_mp3(input_file, output_file, progress_bar, status_label):
    video = VideoFileClip(input_file)
    audio = video.audio
    audio.write_audiofile(output_file, logger=None)
    audio.close()

def browse_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, file_path)

def browse_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, file_path)

def convert():
    input_file = input_file_entry.get()
    output_file = output_file_entry.get()
    
    if not input_file or not output_file:
        status_label.config(text="Please select input and output files.")
        return
    
    status_label.config(text="Converting...")
    progress_bar["value"] = 0

    def conversion_thread():
        mp4_to_mp3(input_file, output_file, progress_bar, status_label)
    
    thread = Thread(target=conversion_thread)
    thread.start()

    def update_progress():
        while thread.is_alive():
            video = VideoFileClip(input_file)
            progress = (video.reader.pos / video.reader.nframes) * 100
            progress_bar["value"] = progress
            app.update_idletasks()
            time.sleep(1)
        progress_bar["value"] = 100
        status_label.config(text="Conversion completed")
    
    Thread(target=update_progress).start()

# Create the main application window
app = tk.Tk()
app.title("MP4 to MP3 Converter")

# Input file selection
input_label = tk.Label(app, text="Input MP4 File:")
input_label.pack()
input_file_entry = tk.Entry(app, width=50)
input_file_entry.pack()
browse_input_button = tk.Button(app, text="Browse", command=browse_input_file)
browse_input_button.pack()

# Output file selection
output_label = tk.Label(app, text="Output MP3 File:")
output_label.pack()
output_file_entry = tk.Entry(app, width=50)
output_file_entry.pack()

# Create a frame for Browse Output and Convert buttons with some padding
button_frame = tk.Frame(app)
button_frame.pack(pady=10)  # Add padding at the top
browse_output_button = tk.Button(button_frame, text="Browse", command=browse_output_file)
browse_output_button.pack(side=tk.LEFT)
convert_button = tk.Button(button_frame, text="Convert", command=convert)
convert_button.pack(side=tk.LEFT)

# Progress bar with padding
progress_bar = ttk.Progressbar(app, length=300, mode="determinate")
status_label = tk.Label(app, text="")
progress_bar.pack(pady=10)  # Add padding at the bottom
status_label.pack()

# Run the application
app.mainloop()
