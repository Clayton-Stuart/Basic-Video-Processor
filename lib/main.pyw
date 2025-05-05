# pygame_widgets usage https://pygamewidgets.readthedocs.io/en/latest/

import pygame
import pygame_widgets as wg
from tkinter import filedialog as fd
from pygame_widgets.dropdown import Dropdown as Dropdown
from pygame_widgets.button import Button as Button
from pygame_widgets.textbox import TextBox as TextBox
from pages import *
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

mirror_input = ""
mirror_output = ""

clip_in = ""
clip_out = ""
start = "00:00:00.00"
end = "00:00:00.00"

scale_in = ""
scale_out = ""
keep_aspect_ratio = True
new_width = 0
new_height = 0

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

def convert(in_file, out_file):
    names = list(os.listdir(os.path.join(".", "lib", "bats")))
    fname = ''.join([choice(CHARS) for _ in range(10)]) + ".bat"
    while fname in names:
        fname = ''.join([choice(CHARS) for _ in range(10)]) + ".bat"
    
    file = open(os.path.join(".", "lib", "bats", fname), "w")
    file.write(f"{FFMPEG} -i \"{in_file}\" \"{out_file}\"\nexit")
    file.close()
    subprocess.Popen(f"{FFMPEG} -i \"{in_file}\" \"{out_file}\"")
    

def clip(in_file, out_file, start, end):
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



# Home Page Dropdown Selection
home_dropdown = Dropdown(screen, WIN_WIDTH // 64, WIN_HEIGHT // 40, WIN_WIDTH / 4.6, WIN_HEIGHT / 10.666, "Select Operation",  
                         ["Convert", "Clip", "Scale", "Merge", "Rotate", "Mirror"], 
                         borderRadius=3, 
                         colour=pygame.Color('gray'), 
                         font=pygame.font.SysFont('calibri', WIN_WIDTH // 32) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 20), 
                         values=["convert", "clip", "scale", "merge", "rotate", "Mirror"], 
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
                   onRelease=(lambda: lambda: set_out_file(fd.asksaveasfilename(), "rotate")),
                   textHAlign='centre', textVAlign='centre',
                   radius=3,
                   colour=pygame.Color('gray'),
                   pressedColour=(90, 90, 255),
                   inactiveColour=(176, 176, 176))
rotate_run = Button(screen, WIN_WIDTH // 64, WIN_HEIGHT - WIN_HEIGHT / 10.4, WIN_WIDTH / 8.533, WIN_HEIGHT / 10.6,
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
                   onRelease=(lambda: lambda: set_out_file(fd.asksaveasfilename(), "mirror")),
                   textHAlign='centre', textVAlign='centre',
                   radius=3,
                   colour=pygame.Color('gray'),
                   pressedColour=(90, 90, 255),
                   inactiveColour=(176, 176, 176))
                      
                    

opperation_buttons = [convert_input, convert_output, convert_run, 
                      clip_input, clip_output, clip_run, clip_start, clip_end,
                      scale_input, scale_output, scale_width, scale_height, scale_toggle_ration, scale_run,
                      rotate_90, rotate_180, rotate_270, rotate_input, rotate_output, rotate_run]
convert_indexes = [0, 1, 2]
clip_indexes = [3, 4, 5, 6, 7]
scale_indexes = [8, 9, 10, 11, 12, 13]
rotate_indexes = [14, 15, 16, 17, 18, 19]
mirror_indexes = []

cur_font = pygame.font.SysFont('calibri', WIN_WIDTH // 40) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 25)
file_font = pygame.font.SysFont('calibri', WIN_WIDTH // 64) if WIN_HEIGHT < WIN_WIDTH else pygame.font.SysFont('calibri', WIN_HEIGHT // 40)

while running:
    screen.fill((255, 255, 255))
    change_page(home_dropdown.getSelected())
    

    # Event Loop
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if page == "home":
        draw_home(pygame)
        home_button.hide()
        home_dropdown.show()
        hide_all(opperation_buttons)

    if page != "home":
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


    

    wg.update(events)
    pygame.display.update()
    CLOCK.tick(30)