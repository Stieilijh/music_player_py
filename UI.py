import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from tkinter import filedialog
import tkinter as tk
import pygame



pygame.init()
pygame.mixer.init()


WINDOW_WIDTH = "600"
WINDOW_LENGTH = "400"
SONG_LENGTH = 0
MUSIC_SLIDER_CLICKED = False
SONG_POSITION = 0


def on_select_btn_clicked():
    file_path = filedialog.askopenfilename(title="Open a music file",
                                           filetypes=(("MP3 files", "*.mp3"),))
    if not os.path.exists(str(file_path)):
        return
    select_song(file_path)


def select_song(file_path):
    global SONG_LENGTH
    pygame.mixer.music.load(file_path)
    SONG_LENGTH = pygame.mixer.Sound(file_path).get_length()
    mus_slider.configure(to=SONG_LENGTH)
    on_restart_btn_clicked()


def on_restart_btn_clicked():
    global SONG_POSITION
    SONG_POSITION = 0
    pygame.mixer.music.play()
    mus_slider.configure(state="normal")
    change_mus_slider_label()


def on_pause_btn_clicked():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        mus_slider.configure(state="disabled")
    else:
        mus_slider.configure(state="normal")
        pygame.mixer.music.unpause()


def on_volume_slider_change(value):
    pygame.mixer.music.set_volume(int(value)/100)

def on_music_slider_change(pvalue):
    global SONG_LENGTH, MUSIC_SLIDER_CLICKED, SONG_POSITION
    if pygame.mixer.music.get_busy() and SONG_LENGTH != 0:
        value = mus_slider.get()
        position = value
        pygame.mixer.music.play()
        pygame.mixer.music.set_pos(position)
        SONG_POSITION = position * 1000
        change_mus_slider_label()
    MUSIC_SLIDER_CLICKED = False

def on_mus_slider_click(event):
    global MUSIC_SLIDER_CLICKED
    MUSIC_SLIDER_CLICKED = True

def change_mus_slider_label():
    if SONG_LENGTH==0:
        return
    value=convert_seconds_to_minutes(SONG_POSITION//1000)+"/"+convert_seconds_to_minutes(SONG_LENGTH)
    mus_slider_label.configure(text=value)

def convert_seconds_to_minutes(seconds):
    seconds=int(seconds)
    m=str(seconds//60)
    s=seconds%60
    if s<10:
        s="0"+str(s)
    else:
        s=str(s)
    return m+":"+s

#Process Methods
def update_music_slider():
    global SONG_LENGTH
    if pygame.mixer.music.get_busy() and SONG_LENGTH != 0 and not MUSIC_SLIDER_CLICKED:
        time = SONG_POSITION/1000
        mus_slider.set(time)
        change_mus_slider_label()
    window.after(1000, update_music_slider)

def update_pos_variable():
    global SONG_POSITION
    if pygame.mixer.music.get_busy() and SONG_LENGTH != 0:
        SONG_POSITION = SONG_POSITION+100
    window.after(100, update_pos_variable)


def on_closing():
    if pygame.mixer.music.get_busy:
        pygame.mixer.music.unload()
    window.destroy()


# Create a window
window = tk.Tk()

# set protocol for on close
window.protocol("WM_DELETE_WINDOW", on_closing)
# set the size of the window to 600x400 pixels
window.geometry(WINDOW_WIDTH+"x"+WINDOW_LENGTH)

# Set the window title
window.title("Music Player")

# Create button
select_button = tk.Button(window, text="Select & Play",
                          command=on_select_btn_clicked)
select_button.grid(row=0, column=0)
restart_button = tk.Button(window, text="Restart",
                        command=on_restart_btn_clicked)
restart_button.grid(row=0, column=1)
pause_button = tk.Button(window, text="Pause", command=on_pause_btn_clicked)
pause_button.grid(row=0, column=2)

# pause button pressed when space bar pressed
window.bind("<space>", lambda event: on_pause_btn_clicked())

# Create a label widget
label = tk.Label(window, text="Volume")
label.grid(row=0, column=3)

# create volume slider
VOLUME_SLIDER_WIDTH = 30*int(WINDOW_WIDTH)/100
vol_slider = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL,
                      command=on_volume_slider_change, length=VOLUME_SLIDER_WIDTH)
vol_slider.set(50)
pygame.mixer.music.set_volume(0.5)
vol_slider.grid(row=1, column=3, columnspan=4)

# create music slider and label
mus_slider_label = tk.Label(window,text="0:00/0:00")
mus_slider_label.grid(row=4,column=1)
MUSIC_SLIDER_WIDTH = 90*int(WINDOW_LENGTH)/100
mus_slider = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL,
                      length=MUSIC_SLIDER_WIDTH,tickinterval=0,showvalue=0)
mus_slider.set(0)
mus_slider.bind("<Button-1>", on_mus_slider_click)
mus_slider.bind("<ButtonRelease-1>", on_music_slider_change)
mus_slider.grid(row=6, column=1, columnspan=4)
# processes
window.after(1000, update_music_slider)
window.after(100, update_pos_variable)
# Start the event loop
window.mainloop()
