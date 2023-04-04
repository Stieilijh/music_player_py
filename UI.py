import tkinter as tk
import music_player
import pygame
from tkinter import filedialog
import os

pygame.init()
pygame.mixer.init()

WINDOW_WIDTH = "600"
WINDOW_LENGTH = "400"


def on_select_btn_clicked():
    file_path = filedialog.askopenfilename(title="Open a music file",
                                           filetypes=(("mp3 files", "*.mp3"),
                                                      ("wav files", "*.wav")))
    if not os.path.exists(str(file_path)):
        return
    select_song(file_path)


def select_song(file_path):
    output_file = music_player.convert(file_path)
    pygame.mixer.music.load(output_file)


def on_play_btn_clicked():
    pygame.mixer.music.play()


def on_pause_btn_clicked():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()


def on_volume_slider_change(value):
    pygame.mixer.music.set_volume(int(value)/100)


# Create a window
window = tk.Tk()

# set the size of the window to 600x400 pixels
window.geometry(WINDOW_WIDTH+"x"+WINDOW_LENGTH)

# Set the window title
window.title("Music Player")

# Create button
select_button = tk.Button(window, text="Select",
                          command=on_select_btn_clicked)
select_button.grid(row=0, column=0)
play_button = tk.Button(window, text="Play/Restart",
                        command=on_play_btn_clicked)
play_button.grid(row=0, column=1)
pause_button = tk.Button(window, text="Pause", command=on_pause_btn_clicked)
pause_button.grid(row=0, column=2)

# pause button pressed when space bar pressed
window.bind("<space>", lambda event: on_pause_btn_clicked())

# Create a label widget
label = tk.Label(window, text="Volume")
label.grid(row=0, column=3)

# create slider
SLIDER_WIDTH = 30*int(WINDOW_WIDTH)/100
slider = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL,
                  command=on_volume_slider_change, length=SLIDER_WIDTH)
slider.grid(row=1, column=3, columnspan=4)
# Start the event loop
window.mainloop()
