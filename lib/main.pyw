# pygame_widgets usage https://pygamewidgets.readthedocs.io/en/latest/

import pygame
import pygame_widgets as wg
from tkinter import filedialog as fd
from pygame_widgets.dropdown import Dropdown as Dropdown
from pygame_widgets.button import Button as Button
from pygame_widgets.textbox import TextBox as TextBox
from pages import get_remove_index
import screeninfo
import os
from random import choice
import subprocess

# Startup Clear Cache
for file in os.listdir(os.path.join(".", "lib", "bats")):
    os.remove(os.path.join(".", "lib", "bats", file))

# Set CWD
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

# Setup
WIN_WIDTH, WIN_HEIGHT = screeninfo.get_monitors()[0].width//2, screeninfo.get_monitors()[0].height//2 # Screen size
CHARS = list("abcdefghijklmnopqrstuvwxyz1234567890-_")
running = True
FFMPEG = os.path.join(".", "mpeg", "bin", "ffmpeg.exe")

FONT_SIZE_FILE = 15

page = "home"
convert_in = ""
convert_out = ""

rotate_in = ""
rotate_out = ""
rotate = 0

mirror_in = ""
mirror_out = ""
mirror_axis = ["Horizontal (Left-Right)", "hflip"]

clip_in = ""
clip_out = ""
start = "00:00:00.00"
end = "00:00:00.00"

scale_in = ""
scale_out = ""
keep_aspect_ratio = True
new_width = 0
new_height = 0

merge_in = []
merge_out = ""
merge_order = []

# Startup Pygame
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
CLOCK = pygame.time.Clock()

def change_page(new_page):
    global page
    if new_page is not None:
        page = new_page
    else:
        page = "home"

def set_rotate(txt):
    global rotate
    rotate = txt

def set_mirror(txt):
    global mirror_axis
    mirror_axis = txt

def validateScale(txt, scale):
    global new_height, new_width
    if scale == "width" and txt.isdigit() and int(txt) > 0:
        new_width = txt
    elif scale == "height" and txt.isdigit() and int(txt) > 0:
        new_height = txt

def validateTime(txt, time):
    txt = txt.lower()
    global start, end
    allowed_chars = "0123456789:."
    txt = txt.strip()
    if txt == "start" and time == "start":
        start = "start"
        return
    elif txt == "end" and time == "end":
        end = "end"
        return
    
    for c in txt:
        if c not in allowed_chars:
            return False
    parts = txt.split(":")
    if len(parts) != 3:
        return False
    if parts[2].count(".")!= 1:
        return False
    if len(parts[1])!= 2 or len(parts[2])!= 5:
        return False
    if int(parts[1]) > 59 or int(parts[1]) < 0 or float(parts[2]) > 59.99 or float(parts[2]) < 0.00:
        return False
    
    if time == "start":
        start = txt
    elif time == "end":
        end = txt

def change_aspect_ratio():
    global keep_aspect_ratio
    keep_aspect_ratio = not keep_aspect_ratio

def hide_all(btns):
    for btn in btns:
        btn.hide()

def toggle_ratio():
    global keep_aspect_ratio, scale_height
    keep_aspect_ratio = not keep_aspect_ratio

    if keep_aspect_ratio:
        scale_height.hide()
    else:
        scale_height.show()

def set_in_file(file_path, page):
    if page == "convert":
        global convert_in
        convert_in = file_path
    elif page == "clip":
        global clip_in
        clip_in = file_path
    elif page == "scale":
        global scale_in
        scale_in = file_path
    elif page == "rotate":
        global rotate_in
        rotate_in = file_path
    elif page == "mirror":
        global mirror_in
        mirror_in = file_path

def add_in_file(file_path):
    global merge_in, merge_order
    merge_in.append(file_path)
    merge_order.append(len(merge_in) - 1)

def remove_in_file(index: str):
    global merge_in, merge_order
    if not index.isnumeric():
        return
    else:
        index = int(index) - 1
    
    if index >= len(merge_in):
        return

    merge_in.pop(index)
    place = merge_order.index(index)
    merge_order.pop(place)
    for i in range(len(merge_order)):
        if merge_order[i] > index:
            merge_order[i] -= 1

    change_page("merge")

def merge_swap(index1: str, index2: str):
    global merge_in, merge_order
    if not index1.isnumeric() or not index2.isnumeric():
        return
    index1 = int(index1) - 1
    index2 = int(index2) - 1
    if index1 >= len(merge_in) or index2 >= len(merge_in):
        return
    merge_in[index1], merge_in[index2] = merge_in[index2], merge_in[index1]

    

def set_out_file(file_path, page):
    if page == "convert":
        global convert_out
        convert_out = file_path
    elif page == "clip":
        global clip_out
        clip_out = file_path
    elif page == "scale":
        global scale_out
        scale_out = file_path
    elif page == "rotate":
        global rotate_out
        rotate_out = file_path
    elif page == "mirror":
        global mirror_out
        mirror_out = file_path
    elif page == "merge":
        global merge_out
        merge_out = file_path
    

def convert(in_file, out_file):
    if out_file == "":
        return
    names = list(os.listdir(os.path.join(".", "lib", "bats")))
    fname = ''.join([choice(CHARS) for _ in range(10)]) + ".bat"
    while fname in names:
        fname = ''.join([choice(CHARS) for _ in range(10)]) + ".bat"
    
    file = open(os.path.join(".", "lib", "bats", fname), "w")
    file.write(f"{FFMPEG} -i \"{in_file}\" \"{out_file}\"\nexit")
    file.close()
    subprocess.Popen(f"{FFMPEG} -i \"{in_file}\" \"{out_file}\"")
    

def clip(in_file, out_file, start, end):
    if out_file == "":
        return
    if start == "start" and end == "end":
        convert(in_file, out_file)
        return
    
        
    names = list(os.listdir(os.path.join(".", "lib", "bats")))
    fname = ''.join([choice(CHARS) for _ in range(10)]) + ".bat"
    while fname in names:
        fname = ''.join([choice(CHARS) for _ in range(10)]) + ".bat"
    
    file = open(os.path.join(".", "lib", "bats", fname), "w")
    if start == "start" and end!= "end":
        file.write(f"{FFMPEG} -to {end} -i \"{in_file}\" \"{out_file}\"\nexit")
        file.close()
        subprocess.Popen(f"{FFMPEG} -to {end} -i \"{in_file}\" \"{out_file}\"")
    elif start!= "start" and end == "end":
        file.write(f"{FFMPEG} -ss {start} -i \"{in_file}\" \"{out_file}\"\nexit")
        file.close()
        subprocess.Popen(f"{FFMPEG} -ss {start} -i \"{in_file}\" \"{out_file}\"")
    else:
        file.write(f"{FFMPEG} -ss {start} -to {end} -i \"{in_file}\" \"{out_file}\"\nexit")
        file.close()
        subprocess.Popen(f"{FFMPEG} -ss {start} -to {end} -i \"{in_file}\" \"{out_file}\"")

def scale(in_file, out_file, width, height, keep_aspect_ratio):
    if out_file == "":
        return
    if int(width) % 2!= 0:
        width = str(int(width) + 1)
    if int(height) % 2!= 0:
        width = str(int(height) + 1)
    names = list(os.listdir(os.path.join(".", "lib", "bats")))
    fname = ''.join([choice(CHARS) for _ in range(10)]) + ".bat"
    while fname in names:
        fname = ''.join([choice(CHARS) for _ in range(10)]) + ".bat"

    if keep_aspect_ratio:
        command = f"{FFMPEG} -i \"{in_file}\" -vf scale={width}:trunc(ow/a/2)*2 \"{out_file}\""
    else:
        command = f"{FFMPEG} -i \"{in_file}\" -vf scale={width}:{height} \"{out_file}\""

    file = open(os.path.join(".", "lib", "bats", fname), "w")
    file.write(command + "\nexit")
    file.close()
    subprocess.Popen(command)

def rotate_image(in_file, out_file, degrees):
    if out_file == "":
        return
    if degrees == 90: 
        vf = "transpose=1"
    elif degrees == 180:
        vf = "transpose=1,transpose=1"
    elif degrees == 270:
        vf = "transpose=2"
    else:
        return

    names = list(os.listdir(os.path.join(".", "lib", "bats")))
    fname = ''.join([choice(CHARS) for _ in range(10)]) + ".bat"
    while fname in names:
        fname = ''.join([choice(CHARS) for _ in range(10)]) + ".bat"


    command = f"{FFMPEG} -i \"{in_file}\" -vf \"{vf}\" \"{out_file}\""

    file = open(os.path.join(".", "lib", "bats", fname), "w")
    file.write(command + "\nexit")
    file.close()
    subprocess.Popen(command)

def mirror_image(in_file, out_file, axis):
    if out_file == "":
        return
    names = list(os.listdir(os.path.join(".", "lib", "bats")))
    fname = ''.join([choice(CHARS) for _ in range(10)]) + ".bat"
    while fname in names:
        fname = ''.join([choice(CHARS) for _ in range(10)]) + ".bat"


    command = f"{FFMPEG} -i \"{in_file}\" -vf \"{axis}\" \"{out_file}\""

    file = open(os.path.join(".", "lib", "bats", fname), "w")
    file.write(command + "\nexit")
    file.close()
    subprocess.Popen(command)

def merge(in_files, out_file, order):
    # ffmpeg -i opening.mkv -i episode.mkv -i ending.mkv \
    # -filter_complex "[0:v] [0:a] [1:v] [1:a] [2:v] [2:a] \
    # concat=n=3:v=1:a=1 [v] [a]" \
    # -map "[v]" -map "[a]" output.mkv
    if out_file == "":
        return
    names = list(os.listdir(os.path.join(".", "lib", "bats")))
    fname = ''.join([choice(CHARS) for _ in range(10)]) + ".bat"
    while fname in names:
        fname = ''.join([choice(CHARS) for _ in range(10)]) + ".bat"

    command = f"{FFMPEG} "
    for file in in_files:
        command += f"-i \"{file}\" "
    command += f"-filter_complex \""

    for i in range(len(in_files)):
        command += f"[{i}:v:0] [{i}:a:0] "
    command += f"concat=n={len(in_files)}:v=1:a=1 [v] [a]\" -map \"[v]\" -map \"[a]\" \"{out_file}\""
    file = open(os.path.join(".", "lib", "bats", fname), "w")
    file.write(command + "\nexit")
    file.close()
    subprocess.Popen(command)

# Home Page Dropdown Selection
home_dropdown = Dropdown(screen, WIN_WIDTH // 64, WIN_HEIGHT // 40, WIN_WIDTH / 4.6, WIN_HEIGHT / 10.666, "Select Operation",  
                         ["Convert", "Clip", "Scale", "Merge", "Rotate", "Mirror"], 
                         borderRadius=3, 
                         colour=pygame.Color('gray'), 
                         font=pygame.font.SysFont('calibri', WIN_WIDTH // 32) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 20), 
                         values=["convert", "clip", "scale", "merge", "rotate", "mirror"], 
                         direction='down', 
                         textHAlign='left',
                         onRelease=(lambda: change_page(home_dropdown.getSelected())),)

home_button = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 40, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                     text="Home",
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 32) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 20), 
                     onRelease=(lambda: [change_page("home"), home_dropdown.reset()]),
                     textHAlign='centre', textVAlign='centre',
                     radius=3,
                     colour=pygame.Color('gray'),
                     pressedColour=(90, 90, 255),
                     inactiveColour=(176, 176, 176))

# Convert Page
convert_input = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 6, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                       text="Input",
                       font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                       onRelease=(lambda: set_in_file(fd.askopenfilename(), "convert")),
                       textHAlign='centre', textVAlign='centre',
                       radius=3,
                       colour=pygame.Color('gray'),
                       pressedColour=(90, 90, 255),
                       inactiveColour=(176, 176, 176))
convert_output = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 3, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                       text="Output",
                       font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                       onRelease=(lambda: set_out_file(fd.asksaveasfilename(), "convert")),
                       textHAlign='centre', textVAlign='centre',
                       radius=3,
                       colour=pygame.Color('gray'),
                       pressedColour=(90, 90, 255),
                       inactiveColour=(176, 176, 176))
convert_run = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT - WIN_HEIGHT / 10.4, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.6,
                     text="Run",
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                     onRelease=(lambda: convert(convert_in, convert_out)),
                     textHAlign='centre', textVAlign='centre',
                     radius=3,
                     colour=pygame.Color('gray'),
                     pressedColour=(90, 90, 255),
                     inactiveColour=(176, 176, 176))

# CLip Page
clip_input = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 6, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                       text="Input",
                       font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                       onRelease=(lambda: set_in_file(fd.askopenfilename(), "clip")),
                       textHAlign='centre', textVAlign='centre',
                       radius=3,
                       colour=pygame.Color('gray'),
                       pressedColour=(90, 90, 255),
                       inactiveColour=(176, 176, 176))
clip_output = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 3.8, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                       text="Output",
                       font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                       onRelease=(lambda: set_out_file(fd.asksaveasfilename(), "clip")),
                       textHAlign='centre', textVAlign='centre',
                       radius=3,
                       colour=pygame.Color('gray'),
                       pressedColour=(90, 90, 255),
                       inactiveColour=(176, 176, 176))
clip_start = TextBox(screen, WIN_WIDTH // 64, WIN_HEIGHT // 2.5, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25),
                     onSubmit=(lambda: validateTime(clip_start.getText(), "start")),
                     placeholderText="Start Time")
clip_end = TextBox(screen, WIN_WIDTH // 64, WIN_HEIGHT // 2, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25),
                     onSubmit=(lambda: validateTime(clip_end.getText(), "end")),
                     placeholderText="End Time")
clip_run = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT - WIN_HEIGHT / 10.4, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.6,
                     text="Run",
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                     onRelease=(lambda: clip(clip_in, clip_out, start, end)),
                     textHAlign='centre', textVAlign='centre',
                     radius=3,
                     colour=pygame.Color('gray'),
                     pressedColour=(90, 90, 255),
                     inactiveColour=(176, 176, 176))

# Scale Page
scale_input = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 6, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                       text="Input",
                       font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                       onRelease=(lambda: set_in_file(fd.askopenfilename(), "scale")),
                       textHAlign='centre', textVAlign='centre',
                       radius=3,
                       colour=pygame.Color('gray'),
                       pressedColour=(90, 90, 255),
                       inactiveColour=(176, 176, 176))
scale_output = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 3.8, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                       text="Output",
                       font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                       onRelease=(lambda: set_out_file(fd.asksaveasfilename(), "scale")),
                       textHAlign='centre', textVAlign='centre',
                       radius=3,
                       colour=pygame.Color('gray'),
                       pressedColour=(90, 90, 255),
                       inactiveColour=(176, 176, 176))
scale_width = TextBox(screen, WIN_WIDTH // 64, WIN_HEIGHT // 2.5, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25),
                     onSubmit=(lambda: validateScale(scale_width.getText(), "width")),
                     placeholderText="Width")
scale_height = TextBox(screen, WIN_WIDTH // 64, WIN_HEIGHT // 2, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25),
                     onSubmit=(lambda: validateScale(scale_height.getText(), "height")),
                     placeholderText="Height")
scale_toggle_ration = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 1.5, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                     text="Keep Ratio",
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                     onRelease=(lambda: toggle_ratio()),
                     textHAlign='centre', textVAlign='centre',
                     radius=3,
                     colour=pygame.Color('gray'),)
scale_run = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT - WIN_HEIGHT / 10.4, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.6,
                     text="Run",
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                     onRelease=(lambda: scale(scale_in, scale_out, new_width, new_height, keep_aspect_ratio)),
                     textHAlign='centre', textVAlign='centre',
                     radius=3,
                     colour=pygame.Color('gray'),
                     pressedColour=(90, 90, 255),
                     inactiveColour=(176, 176, 176))

rotate_90 = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 6, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                   text="Rotate 90°",
                   font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                   onRelease=(lambda: set_rotate(90)),
                   textHAlign='centre', textVAlign='centre',
                   radius=3,
                   colour=pygame.Color('gray'),
                   pressedColour=(90, 90, 255),
                   inactiveColour=(176, 176, 176))
rotate_180 = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 3.8, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                   text="Rotate 180°",
                   font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                   onRelease=(lambda: set_rotate(180)),
                   textHAlign='centre', textVAlign='centre',
                   radius=3,
                   colour=pygame.Color('gray'),
                   pressedColour=(90, 90, 255),
                   inactiveColour=(176, 176, 176))
rotate_270 = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 2.78, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                   text="Rotate 270°",
                   font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                   onRelease=(lambda: set_rotate(270)),
                   textHAlign='centre', textVAlign='centre',
                   radius=3,
                   colour=pygame.Color('gray'),
                   pressedColour=(90, 90, 255),
                   inactiveColour=(176, 176, 176))
rotate_input = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 2, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                   text="Input",
                   font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                   onRelease=(lambda: set_in_file(fd.askopenfilename(), "rotate")),
                   textHAlign='centre', textVAlign='centre',
                   radius=3,
                   colour=pygame.Color('gray'),
                   pressedColour=(90, 90, 255),
                   inactiveColour=(176, 176, 176))
rotate_output = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 1.675, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                   text="Output",
                   font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                   onRelease=(lambda: set_out_file(fd.asksaveasfilename(), "rotate")),
                   textHAlign='centre', textVAlign='centre',
                   radius=3,
                   colour=pygame.Color('gray'),
                   pressedColour=(90, 90, 255),
                   inactiveColour=(176, 176, 176))
rotate_run = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT - WIN_HEIGHT / 10.4, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                     text="Run",
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                     onRelease=(lambda: rotate_image(rotate_in, rotate_out, rotate)),
                     textHAlign='centre', textVAlign='centre',
                     radius=3,
                     colour=pygame.Color('gray'),
                     pressedColour=(90, 90, 255),
                     inactiveColour=(176, 176, 176))

mirror_input = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 2, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                   text="Input",
                   font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                   onRelease=(lambda: set_in_file(fd.askopenfilename(), "mirror")),
                   textHAlign='centre', textVAlign='centre',
                   radius=3,
                   colour=pygame.Color('gray'),
                   pressedColour=(90, 90, 255),
                   inactiveColour=(176, 176, 176))
mirror_output = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 1.675, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                   text="Output",
                   font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                   onRelease=(lambda: set_out_file(fd.asksaveasfilename(), "mirror")),
                   textHAlign='centre', textVAlign='centre',
                   radius=3,
                   colour=pygame.Color('gray'),
                   pressedColour=(90, 90, 255),
                   inactiveColour=(176, 176, 176))
mirror_axis_lr = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 2.7, WIN_WIDTH / 5.5, WIN_HEIGHT / 10.666,
                   text="Mirror (Left-Right)",
                   font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                   onRelease=(lambda: set_mirror(["Horizontal (Left-Right)", "hflip"])),
                   textHAlign='centre', textVAlign='centre',
                   radius=3,
                   colour=pygame.Color('gray'),
                   pressedColour=(90, 90, 255),
                   inactiveColour=(176, 176, 176))
mirror_axis_ud = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 4, WIN_WIDTH / 5.5, WIN_HEIGHT / 10.666,
                   text="Mirror (Up-Down)",
                   font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                   onRelease=(lambda: set_mirror(["Vertical (Up-Down)", "vflip"])),
                   textHAlign='centre', textVAlign='centre',
                   radius=3,
                   colour=pygame.Color('gray'),
                   pressedColour=(90, 90, 255),
                   inactiveColour=(176, 176, 176))
mirror_run = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT - WIN_HEIGHT / 10.4, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                     text="Run",
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                     onRelease=(lambda: mirror_image(mirror_in, mirror_out, mirror_axis[1])),
                     textHAlign='centre', textVAlign='centre',
                     radius=3,
                     colour=pygame.Color('gray'),
                     pressedColour=(90, 90, 255),
                     inactiveColour=(176, 176, 176))
merge_add_input = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 4, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                     text="Add Input",
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                     onRelease=(lambda: add_in_file(fd.askopenfilename())),
                     textHAlign='centre', textVAlign='centre',
                     radius=3,
                     colour=pygame.Color('gray'),
                     pressedColour=(90, 90, 255),
                     inactiveColour=(176, 176, 176))
merge_output = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 2.8, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                   text="Output",
                   font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                   onRelease=(lambda: set_out_file(fd.asksaveasfilename(), "merge")),
                   textHAlign='centre', textVAlign='centre',
                   radius=3,
                   colour=pygame.Color('gray'),
                   pressedColour=(90, 90, 255),
                   inactiveColour=(176, 176, 176))
merge_remove_input = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 1.3, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                   text="Remove File",
                   font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                   onRelease=(lambda: [change_page("index")]),
                   textHAlign='centre', textVAlign='centre',
                   radius=3,
                   colour=pygame.Color('gray'),
                   pressedColour=(90, 90, 255),
                   inactiveColour=(176, 176, 176))
merge_order_input = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 1.5, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                   text="Reorder Files",
                   font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                   onRelease=(lambda: [change_page("reorder")]),
                   textHAlign='centre', textVAlign='centre',
                   radius=3,
                   colour=pygame.Color('gray'),
                   pressedColour=(90, 90, 255),
                   inactiveColour=(176, 176, 176))
merge_run = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT - WIN_HEIGHT / 10.4, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                     text="Run",
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                     onRelease=(lambda: merge(merge_in, merge_out, merge_order)),
                     textHAlign='centre', textVAlign='centre',
                     radius=3,
                     colour=pygame.Color('gray'),
                     pressedColour=(90, 90, 255),
                     inactiveColour=(176, 176, 176))
index_exit = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 40, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                     text="Back",
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 32) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 20), 
                     onRelease=(lambda: [change_page("merge")]),
                     textHAlign='centre', textVAlign='centre',
                     radius=3,
                     colour=pygame.Color('gray'),
                     pressedColour=(90, 90, 255),
                     inactiveColour=(176, 176, 176))
index_select = TextBox(screen, WIN_WIDTH // 64, WIN_HEIGHT // 2.5, WIN_WIDTH / 7, WIN_HEIGHT / 10.666,
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25),
                     placeholderText="File Number")
index_run = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT - WIN_HEIGHT / 10.4, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                     text="Remove",
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                     onRelease=(lambda: remove_in_file(index_select.getText())),
                     textHAlign='centre', textVAlign='centre',
                     radius=3,
                     colour=pygame.Color('gray'),
                     pressedColour=(90, 90, 255),
                     inactiveColour=(176, 176, 176))
order_exit = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT // 40, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                     text="Back",
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 32) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 20), 
                     onRelease=(lambda: [change_page("merge")]),
                     textHAlign='centre', textVAlign='centre',
                     radius=3,
                     colour=pygame.Color('gray'),
                     pressedColour=(90, 90, 255),
                     inactiveColour=(176, 176, 176))
order_select_1 = TextBox(screen, WIN_WIDTH // 64, WIN_HEIGHT // 2.5, WIN_WIDTH / 7, WIN_HEIGHT / 10.666,
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25),
                     placeholderText="File Number")
order_select_2 = TextBox(screen, WIN_WIDTH // 64, WIN_HEIGHT // 2, WIN_WIDTH / 7, WIN_HEIGHT / 10.666,
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25),
                     placeholderText="File Number")
order_run = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT - WIN_HEIGHT / 10.4, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.666,
                     text="Swap",
                     font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), 
                     onRelease=(lambda: merge_swap(order_select_1.getText(), order_select_2.getText())),
                     textHAlign='centre', textVAlign='centre',
                     radius=3,
                     colour=pygame.Color('gray'),
                     pressedColour=(90, 90, 255),
                     inactiveColour=(176, 176, 176))

opperation_buttons = [convert_input, convert_output, convert_run, 
                      clip_input, clip_output, clip_run, clip_start, clip_end,
                      scale_input, scale_output, scale_width, scale_height, scale_toggle_ration, scale_run,
                      rotate_90, rotate_180, rotate_270, rotate_input, rotate_output, rotate_run,
                      mirror_input, mirror_output, mirror_axis_lr, mirror_axis_ud, mirror_run,
                      merge_add_input, merge_output, merge_remove_input, merge_order_input, merge_run,
                      index_exit, index_select, index_run,
                      order_exit, order_select_1, order_select_2, order_run]
convert_indexes = [0, 1, 2]
clip_indexes = [3, 4, 5, 6, 7]
scale_indexes = [8, 9, 10, 11, 12, 13]
rotate_indexes = [14, 15, 16, 17, 18, 19]
mirror_indexes = [20, 21, 22, 23, 24]
merge_indexes = [25, 26, 27, 28, 29]
index_indexes = [30, 31, 32]
order_indexes = [33, 34, 35, 36]

cur_font = pygame.font.SysFont('calibri', WIN_WIDTH // 40) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25)
file_font = pygame.font.SysFont('calibri', WIN_WIDTH // 64) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 40)

while running:
    screen.fill((255, 255, 255))
    if page != "index" and page != "reorder":
        change_page(home_dropdown.getSelected())
    
    

    # Event Loop
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if page == "home":
        home_button.hide()
        home_dropdown.show()
        hide_all(opperation_buttons)

    if page != "home" and page != "index" and page!= "reorder":
        home_dropdown.hide()
        home_button.show()
        text = cur_font.render(f"Current Page: {page}", True, (0, 0, 0))
        screen.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2, text.get_height() // 2))

    if page == "convert":
        hide_all(opperation_buttons)
        for i in convert_indexes:
            opperation_buttons[i].show()
        text1 = file_font.render(f"Input File: {convert_in}", True, (0, 0, 0))
        text2 = file_font.render(f"Output File: {convert_out}", True, (0, 0, 0))
        screen.blit(text1, (WIN_WIDTH // 2 - text1.get_width() // 2, WIN_HEIGHT // 4))
        screen.blit(text2, (WIN_WIDTH // 2 - text2.get_width() // 2, WIN_HEIGHT // 4 + text1.get_height()*1.5 + WIN_HEIGHT // 30))

    elif page == "clip":
        validateTime(clip_start.getText(), "start")
        validateTime(clip_end.getText(), "end")
        hide_all(opperation_buttons)
        for i in clip_indexes:
            opperation_buttons[i].show()
        text1 = file_font.render(f"Input File: {clip_in}", True, (0, 0, 0))
        text2 = file_font.render(f"Output File: {clip_out}", True, (0, 0, 0))
        text3 = cur_font.render(f"Start Time: {start}", True, (0, 0, 0))
        text4 = cur_font.render(f"End Time: {end}", True, (0, 0, 0))
        screen.blit(text1, (WIN_WIDTH // 2 - text1.get_width() // 2, WIN_HEIGHT // 4))
        screen.blit(text2, (WIN_WIDTH // 2 - text2.get_width() // 2, WIN_HEIGHT // 4 + text3.get_height() + WIN_HEIGHT // 30))
        screen.blit(text3, (WIN_WIDTH // 2 - text3.get_width() // 2, WIN_HEIGHT // 4 + text3.get_height() * 2.5 + WIN_HEIGHT // 30))
        screen.blit(text4, (WIN_WIDTH // 2 - text4.get_width() // 2, WIN_HEIGHT // 4 + text3.get_height() * 3.5 + WIN_HEIGHT // 30))

    elif page == "scale":
        hide_all(opperation_buttons)
        for i in scale_indexes:
            opperation_buttons[i].show()

        if keep_aspect_ratio:
            scale_height.hide()
        
        validateScale(scale_width.getText(), "width")
        validateScale(scale_height.getText(), "height")
        text1 = file_font.render(f"Input File: {scale_in}", True, (0, 0, 0))
        text2 = file_font.render(f"Output File: {scale_out}", True, (0, 0, 0))
        text3 = cur_font.render(f"Width: {new_width}", True, (0, 0, 0))
        if keep_aspect_ratio:
            text4 = cur_font.render(f"Maintaining Aspect Ratio", True, (0, 0, 0))
        else:
            text4 = cur_font.render(f"Height: {new_height}", True, (0, 0, 0))
        screen.blit(text1, (WIN_WIDTH // 2 - text1.get_width() // 2, WIN_HEIGHT // 4))
        screen.blit(text2, (WIN_WIDTH // 2 - text2.get_width() // 2, WIN_HEIGHT // 4 + text3.get_height() + WIN_HEIGHT // 30))
        screen.blit(text3, (WIN_WIDTH // 2 - text3.get_width() // 2, WIN_HEIGHT // 4 + text3.get_height() * 2 + WIN_HEIGHT // 30))
        screen.blit(text4, (WIN_WIDTH // 2 - text4.get_width() // 2, WIN_HEIGHT // 4 + text3.get_height() * 3 + WIN_HEIGHT // 30))

    elif page == "rotate":
        hide_all(opperation_buttons)
        for i in rotate_indexes:
            opperation_buttons[i].show()
        
        text1 = file_font.render(f"Input File: {rotate_in}", True, (0, 0, 0))
        text2 = file_font.render(f"Output File: {rotate_out}", True, (0, 0, 0))
        text3 = cur_font.render(f"Angle: {rotate}", True, (0, 0, 0))

        screen.blit(text1, (WIN_WIDTH // 2 - text1.get_width() // 2, WIN_HEIGHT // 4))
        screen.blit(text2, (WIN_WIDTH // 2 - text2.get_width() // 2, WIN_HEIGHT // 4 + text3.get_height() + WIN_HEIGHT // 30))
        screen.blit(text3, (WIN_WIDTH // 2 - text3.get_width() // 2, WIN_HEIGHT // 4 + text3.get_height() * 2.5 + WIN_HEIGHT // 30))

    elif page == "mirror":
        hide_all(opperation_buttons)
        for i in mirror_indexes:
            opperation_buttons[i].show()

        text1 = file_font.render(f"Input File: {mirror_in}", True, (0, 0, 0))
        text2 = file_font.render(f"Output File: {mirror_out}", True, (0, 0, 0))
        text3 = cur_font.render(f"Mirror Axis: {mirror_axis[0]}", True, (0, 0, 0))

        screen.blit(text1, (WIN_WIDTH // 2 - text1.get_width() // 2, WIN_HEIGHT // 4))
        screen.blit(text2, (WIN_WIDTH // 2 - text2.get_width() // 2, WIN_HEIGHT // 4 + text1.get_height() + WIN_HEIGHT // 30))
        screen.blit(text3, (WIN_WIDTH // 2 - text3.get_width() // 2, WIN_HEIGHT // 4 + text2.get_height() * 2.5 + WIN_HEIGHT // 30))

    elif page == "merge":
        hide_all(opperation_buttons)
        for i in merge_indexes:
            opperation_buttons[i].show()

        text2 = file_font.render(f"Output File: {merge_out}", True, (0, 0, 0))
        text3 = file_font.render(f"Video files must have the same dimensions. If the command is not run, use the scale feature to adjust.", True, (0, 0, 0))
        
        screen.blit(text3, ((WIN_WIDTH + WIN_WIDTH / 8.533 + WIN_WIDTH // 64) // 2 - text3.get_width() // 2, WIN_HEIGHT - text3.get_height() - 20))

        text_surfaces = [file_font.render(f"Input Files: ", True, (0, 0, 0))]
        for i in merge_order:
            text_surfaces.append(file_font.render(f"{i + 1}.  {os.path.split(merge_in[i])[-1]}", True, (0, 0, 0)))

        for i in range(len(text_surfaces)):
            screen.blit(text_surfaces[i], (WIN_WIDTH // 2 - text_surfaces[i].get_width() // 2, WIN_HEIGHT // 10 + i * (text_surfaces[i].get_height() + 10)))
        
        screen.blit(text2, (WIN_WIDTH // 2 - text2.get_width() // 2, WIN_HEIGHT // 10 + i * (text_surfaces[0].get_height() + 10) + text_surfaces[0].get_height()*2 + 10))
        

    elif page == "reorder":
        hide_all(opperation_buttons)
        home_button.hide()
        for i in order_indexes:
            opperation_buttons[i].show()

        text_surfaces = []
        for i in merge_order:
            text_surfaces.append(file_font.render(f"{i + 1}.  {os.path.split(merge_in[i])[-1]}", True, (0, 0, 0)))

        for i in range(len(text_surfaces)):
            screen.blit(text_surfaces[i], (WIN_WIDTH // 2 - text_surfaces[i].get_width() // 2 + WIN_WIDTH // 64 + 3, WIN_WIDTH // 10 + i * (text_surfaces[i].get_height() + 10)))

    elif page == "index":
        hide_all(opperation_buttons)
        home_button.hide()
        for i in index_indexes:
            opperation_buttons[i].show()
        
        text_surfaces = []
        for i in merge_order:
            text_surfaces.append(file_font.render(f"{i + 1}.  {merge_in[i]}", True, (0, 0, 0)))

        for i in range(len(text_surfaces)):
            screen.blit(text_surfaces[i], (WIN_WIDTH // 2 - text_surfaces[i].get_width() // 2 + WIN_WIDTH // 64 + 3, WIN_WIDTH // 10 + i * (text_surfaces[i].get_height() + 10)))

        # for i in merge_order:
        #     merge_buttons.append(Button(screen, Button(screen, WIN_WIDTH // 64, 15+merge_buttons[-1].getHeight + 2, 30, 30, text=merge_order.index(i), font=pygame.font.SysFont('calibri', WIN_WIDTH // 45) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25), onRelease=lambda: remove_in_file(str(i)), textHAlign='centre', textVAlign='centre', radius=3, colour=pygame.Color('gray'), pressedColour=(90, 90, 255), inactiveColour=(176, 176, 176))))


    wg.update(events)
    pygame.display.update()
    CLOCK.tick(30)
