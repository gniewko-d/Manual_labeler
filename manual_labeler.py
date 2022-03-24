# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 15:01:40 2022

@author: gniew
"""
import keyboard
import datetime
import cv2
import pandas as pd
import os
import numpy as np
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import easygui
import tkinter.scrolledtext as scrolledtext
from pandastable import Table
df_checker = False
df = None
frame_to_list = None
start_frame_bool = False
previous_column = None
column = None
frameTime = 500
video_file = None
start_frame = None
start_frame_freezed = None
stop_frame = None
current_label = "test"
fps = 5
current_label_list = "test1"
label_1_name = f"{None}"
label_2_name = f"{None}"
label_3_name = f"{None}"
label_4_name = f"{None}"
label_5_name = f"{None}"
label_6_name = f"{None}"
label_7_name = f"{None}"
label_8_name = f"{None}"
label_9_name = f"{None}"

label_1_list = []
label_2_list = []
label_3_list = []
label_4_list = []
label_5_list = []
label_6_list = []
label_7_list = []
label_8_list = []
label_9_list = []

key_pressed_list = [False, False, False, False, False, False, False, False, False]
key_label_controler = [False]
class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Manual Labeler")
        
        self.first_frame = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.first_frame.pack()
        self.first_frame.pack_propagate(0)
        
        self.open_file = tk.Button(self.first_frame, text = "Load video", command = self.easy_open, background="black", foreground="green", width = 26)
        self.open_file.pack(side= tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        self.text = f"Current video: {None}"
        self.current_video = tk.Text(self.first_frame, height = 1, width = 16, background="black", foreground="green", insertbackground = "white")
        self.current_video.insert(tk.INSERT, self.text)
        self.desired_font = tk.font.Font(size = 14)
        self.current_video.configure(font = self.desired_font)
        self.current_video.pack(side=tk.RIGHT, padx=1, pady=1, expand=True, fill='both')
        
        self.second_frame = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.second_frame.pack(side = tk.TOP)
        self.second_frame.pack_propagate(0)
        
        self.keyboard = tk.Button(self.second_frame, text="Keyboard settings", command = self.keyboard_settings, background="black", foreground="green", width = 13)
        self.keyboard.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.label_1_9 = tk.Button(self.second_frame, text="Labels settings", command = self.label_settings, background="black", foreground="green")
        self.label_1_9.pack(side=tk.RIGHT, padx=1, pady=1, expand=True, fill='both')
        
        self.third_frame_v1 = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.third_frame_v1.pack(side = tk.TOP)
        self.third_frame_v1.pack_propagate(0)
        
        self.start_labeling = tk.Button(self.third_frame_v1, text="Start labeling", command = start_vido1, background="black", foreground="green", width = 15)
        self.start_labeling.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.show_df = tk.Button(self.third_frame_v1, text="Show data frame", command = self.draw_table, background="black", foreground="green")
        self.show_df.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
    def easy_open(self):
        global video_file
        video_file = easygui.fileopenbox(title="Select An Video", filetypes= ["*.gif", "*.flv", "*.avi", "*.amv", "*.mp4"])
        if video_file != None:
            messagebox.showinfo("Information box", "Video uploaded")
            video_title = video_file.split("\\")
            self.current_video.delete("1.0","end")
            self.text = f"Current video: {video_title[-1]}"
            self.current_video.configure(width = len(self.text))
            self.current_video.insert(tk.INSERT, self.text)
        else:
            messagebox.showerror("Error box", "Video was not loaded")
    def keyboard_settings(self):
        global fps
        self.new_root = tk.Toplevel(self.root)
        self.new_root.title("Keyboard_settings")
        
        self.first_frame_v1 = tk.Frame(self.new_root, background="black")
        self.first_frame_v1.pack(expand=True, fill='both')
        self.instruction = tk.Text(self.first_frame_v1, height = 23, width = 70)
        self.text_v1 = "Press on your keyboard:\n a = move one frame backward\n d = move one frame forward\n q = escape from video and save markers\n p = pause the video\n r = restart the video (keep the markers applied)\n w = slow down video (have to be pressed constantly)\n e = frame to which (without it) all the preceding ones will\n\t be appropriately marked (depends on labels name set by user).\n\t Start point is set by key 1-9\n key 1-9 = label current frame and jumpt to next one or\n\t set the beginning of the range.\n\t Next you can move to whatever frame (backward or forward)\n\t and there set the end of the range by key e.\n\t All frames within that range will be labeled\n g = delete label of current frame\n h = removes the last labelled range\n z = move x (default = 5) frames backward\n c = move x (default = 5) frames forward\n"
        conteiner = ["~"*70, "~"*70, self.text_v1, "="*70, "="*70]
        
        for i in range(len(conteiner)):
            self.instruction.insert(tk.INSERT, conteiner[i])
            self.instruction.pack(side=tk.TOP, expand=True, fill='both')
            self.instruction.configure(foreground="green", background= "black")
        
        self.second_frame_v2 = tk.Frame(self.new_root)
        self.second_frame_v2.pack(side=tk.TOP, expand=True, fill='both')
        
        self.x_label = tk.Label(self.second_frame_v2, text = f"Set value of x:", foreground="green", background= "black", width = 15, bd = 2)
        self.x_label.pack(side=tk.LEFT,  expand=True, fill='both')
        self.x_text = tk.Text(self.second_frame_v2, foreground="green", background= "black", height = 1, width = 32, insertbackground = "white")
        self.x_text.pack(side=tk.LEFT, expand=True, fill='both')
        
        self.x_submit = tk.Button(self.second_frame_v2, text="Submit", command = self.set_x_value, background="black", foreground="green", width = 25)
        self.x_submit.pack(side=tk.LEFT, expand=True, fill='both')
    def label_settings(self):
        global label_1_name, label_2_name, label_3_name, label_4_name, label_5_name, label_6_name, label_7_name, label_8_name, label_9_name
        self.new_root_2 = tk.Toplevel(self.root, background= "black")
        self.new_root_2.title("Label_settings")
        
        self.first_frame_v2 = tk.Frame(self.new_root_2, background="black")
        self.first_frame_v2.pack()
        
        self.label_1 = tk.Label(self.first_frame_v2, text = "key_1 label:", foreground="green", background= "black")
        self.label_1.pack(side=tk.LEFT)
        
        self.label_1_text_box = tk.Text(self.first_frame_v2, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_1_text_box.insert(tk.INSERT, label_1_name)
        self.label_1_text_box.pack(side=tk.LEFT)
        
        self.second_frame_v1 = tk.Frame(self.new_root_2, background= "black")
        self.second_frame_v1.pack(side = tk.TOP)
        
        self.label_2 = tk.Label(self.second_frame_v1, text = "key_2 label:", foreground="green", background= "black")
        self.label_2.pack(side=tk.LEFT)
        
        self.label_2_text_box = tk.Text(self.second_frame_v1, height = 1, width = 20, foreground="green", background= "black",insertbackground = "white")
        self.label_2_text_box.insert(tk.INSERT, label_2_name)
        self.label_2_text_box.pack(side=tk.LEFT)
        
        self.third_frame = tk.Frame(self.new_root_2, background= "black")
        self.third_frame.pack(side = tk.TOP)
        
        self.label_3 = tk.Label(self.third_frame, text = "key_3 label:", foreground="green", background= "black")
        self.label_3.pack(side=tk.LEFT)
        
        self.label_3_text_box = tk.Text(self.third_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_3_text_box.insert(tk.INSERT, label_3_name)
        self.label_3_text_box.pack(side=tk.LEFT)
        
        self.fourth_frame = tk.Frame(self.new_root_2, background= "black")
        self.fourth_frame.pack(side = tk.TOP)
        
        self.label_4 = tk.Label(self.fourth_frame, text = "key_4 label:", foreground="green", background= "black")
        self.label_4.pack(side=tk.LEFT)
        
        self.label_4_text_box = tk.Text(self.fourth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_4_text_box.insert(tk.INSERT, label_4_name)
        self.label_4_text_box.pack(side=tk.LEFT)
        
        self.fifth_frame = tk.Frame(self.new_root_2, background= "black")
        self.fifth_frame.pack(side = tk.TOP)
        
        self.label_5 = tk.Label(self.fifth_frame, text = "key_5 label:", foreground="green", background= "black")
        self.label_5.pack(side=tk.LEFT)
        
        self.label_5_text_box = tk.Text(self.fifth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_5_text_box.insert(tk.INSERT, label_5_name)
        self.label_5_text_box.pack(side=tk.LEFT)
        
        self.sixth_frame = tk.Frame(self.new_root_2, background= "black")
        self.sixth_frame.pack(side = tk.TOP)
        
        self.label_6 = tk.Label(self.sixth_frame, text = "key_6 label:", foreground="green", background= "black")
        self.label_6.pack(side=tk.LEFT)
        
        self.label_6_text_box = tk.Text(self.sixth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_6_text_box.insert(tk.INSERT, label_6_name)
        self.label_6_text_box.pack(side=tk.LEFT)
        
        self.seventh_frame = tk.Frame(self.new_root_2, background= "black")
        self.seventh_frame.pack(side = tk.TOP)
        
        self.label_7 = tk.Label(self.seventh_frame, text = "key_7 label:", foreground="green", background= "black")
        self.label_7.pack(side=tk.LEFT)
        
        self.label_7_text_box = tk.Text(self.seventh_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_7_text_box.insert(tk.INSERT, label_7_name)
        self.label_7_text_box.pack(side=tk.LEFT)
        
        
        self.eighth_frame = tk.Frame(self.new_root_2, background= "black")
        self.eighth_frame.pack(side = tk.TOP)
        
        self.label_8 = tk.Label(self.eighth_frame, text = "key_8 label:", foreground="green", background= "black")
        self.label_8.pack(side=tk.LEFT)
        
        self.label_8_text_box = tk.Text(self.eighth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_8_text_box.insert(tk.INSERT, label_8_name)
        self.label_8_text_box.pack(side=tk.LEFT)
        
        self.ninth_frame = tk.Frame(self.new_root_2, background= "black")
        self.ninth_frame.pack(side = tk.TOP)
        
        self.label_9 = tk.Label(self.ninth_frame, text = "key_9 label:", foreground="green", background= "black")
        self.label_9.pack(side=tk.LEFT)
        
        self.label_9_text_box = tk.Text(self.ninth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_9_text_box.insert(tk.INSERT, label_9_name)
        self.label_9_text_box.pack(side=tk.LEFT)
        
        self.submit_frame = tk.Frame(self.new_root_2, background= "black")
        self.submit_frame.pack(side = tk.TOP)
        
        self.submit = tk.Button(self.submit_frame, text = "Submit", command = self.label_changer, foreground="green", background= "black")
        self.submit.pack(side = tk.BOTTOM)
    
    def label_changer(self):
        global label_1_name, label_2_name, label_3_name, label_4_name, label_5_name, label_6_name, label_7_name, label_8_name, label_9_name, label_list
        
        label_1_name = self.label_1_text_box.get("1.0", "end-1c")
        label_2_name = self.label_2_text_box.get("1.0", "end-1c")
        label_3_name = self.label_3_text_box.get("1.0", "end-1c")
        label_4_name = self.label_4_text_box.get("1.0", "end-1c")
        label_5_name = self.label_5_text_box.get("1.0", "end-1c")
        label_6_name = self.label_6_text_box.get("1.0", "end-1c")
        label_7_name = self.label_7_text_box.get("1.0", "end-1c")
        label_8_name = self.label_8_text_box.get("1.0", "end-1c")
        label_9_name = self.label_9_text_box.get("1.0", "end-1c")
        label_list = [label_1_name, label_2_name, label_3_name, label_4_name, label_5_name, label_6_name, label_7_name, label_8_name, label_9_name]
        messagebox.showinfo("Information box", "Labels added :):):)")

    def draw_table(self):
        global df, df_checker
        if df_checker == False:
            messagebox.showerror("Error box", "TO see your data frame")
            
        self.new_root_3 = tk.Toplevel(self.root)
        self.new_root_3.title("Labeled frames")
        self.tabel_frame = tk.Frame(self.new_root_3)
        self.tabel_frame.pack(fill='both', expand=True)
        pt = Table(self.tabel_frame, dataframe=df)
        pt.show()
    
    def set_x_value(self):
        global fps
        fps = int(self.x_text.get("1.0", "end-1c"))
        messagebox.showinfo("Information box", f"Value of x changed to {fps} :):):)")
def getFrame(frame_nr):
    global cap
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_nr)

def key_restart(bool_value, lista_bool, *args):
    for i, j in enumerate(lista_bool):
        if i in args:
            lista_bool[i] = not(bool_value)
        else:
            lista_bool[i] = bool_value

def draw_label(text, pos, bg_color):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.4
    color = (0, 0, 0)
    thickness = cv2.FILLED
    margin = 2

    txt_size = cv2.getTextSize(text, font_face, scale, thickness)

    end_x = pos[0] + txt_size[0][0] + margin
    end_y = pos[1] - txt_size[0][1] - margin

    cv2.rectangle(frame, pos, (end_x, end_y), bg_color, thickness)
    cv2.putText(frame, text, pos, font_face, scale, color, 1, cv2.LINE_AA)


def frame_changer(video, direction, frame_num):
    next_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    current_frame = next_frame - 1
    previous_frame = current_frame - frame_num
    next_frame = current_frame + frame_num
    if direction == "back":
        cap.set(cv2.CAP_PROP_POS_FRAMES, previous_frame)
        cv2.setTrackbarPos('frame', title_window, previous_frame)
        cv2.waitKey(0)  # wait until any key is pressed
    elif direction == "front":
        cap.set(cv2.CAP_PROP_POS_FRAMES, next_frame)
        cv2.setTrackbarPos('frame',title_window, next_frame)
        cv2.waitKey(0) #wait un
def add_to_list(frame, list_of_labels):
    if frame not in list_of_labels:
        list_of_labels.append(frame)

def step_mode(data, label, video, key_pressed, column, previous_column, list_of_frames):
    global start_frame, current_label, start_frame_bool, x, frame, frame_to_list, current_label_list
    current_label = label
    current_label_list = list_of_frames
    if key_pressed and x == 0 and previous_column < column:
        start_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        inital = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        next_frame = inital
        data.iloc[inital-1, column] = label
        video.set(cv2.CAP_PROP_POS_FRAMES, next_frame+1)
        cv2.setTrackbarPos('frame',title_window, next_frame+1)
        x += 1 
        frame_to_list = inital-1
        cv2.waitKey(0)
    elif key_pressed:
        start_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        inital = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        next_frame = inital + 1
        data.iloc[inital-2,column] = label
        video.set(cv2.CAP_PROP_POS_FRAMES, inital)
        cv2.setTrackbarPos('frame',title_window, inital)
        frame_to_list = inital-1
        cv2.waitKey(0)
        x += 1 
        
        
    else:
        x = 0
        start_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        inital = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        next_frame = inital + 1
        df.iloc[inital-1, column] = label
        video.set(cv2.CAP_PROP_POS_FRAMES, next_frame)
        cv2.setTrackbarPos('frame',title_window, next_frame)
        start_frame_bool = True
        frame_to_list = inital 
        
        cv2.waitKey(0)


def end_key(data, column):
    global start_frame, start_frame_freezed, stop_frame, start_frame_bool, current_label, current_label_list
    if start_frame_bool:
        stop_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        start_frame_freezed = start_frame
        if stop_frame >= start_frame:
            data.iloc[start_frame-1:stop_frame-1, column] = current_label
            x = [current_label_list.append(i) for i in range(start_frame, stop_frame) if i not in current_label_list]
            start_frame_bool = False
            cv2.waitKey(-1)
        elif stop_frame < start_frame:
            data.iloc[stop_frame:start_frame-1, column] = current_label
            y = [current_label_list.append(i) for i in range(stop_frame+1, start_frame) if i not in current_label_list]
            start_frame_bool = False
            cv2.waitKey(-1)
    else:
        messagebox.showerror("Error box", "First, set the beginning of range")

def delete_mode(data, label, column):
    
    current_frames = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    df.iloc[current_frames-1, column] = label
    cv2.waitKey(-1)

def ctrl_alt_delet(data):
    global stop_frame, start_frame_freezed
    if stop_frame >= start_frame_freezed:
            data.iloc[start_frame_freezed-2:stop_frame, column] = np.nan
            cv2.waitKey(-1)
    elif stop_frame < start_frame_freezed:
        data.iloc[stop_frame:start_frame_freezed, column] = np.nan
        cv2.waitKey(-1)



def start_vido1():
    global label_1_name, xd, cap, title_window, frameTime, df, fps, key_pressed_list, previous_column, column, frame, df_checker, label_1_list, label_2_list, label_3_list, label_4_list, label_5_list, label_6_list, label_7_list, label_8_list, label_9_list, key_label_controler, label_1_list_key_a
    if video_file == None:
        messagebox.showerror("Error box", "Upload the video first")
    else:
        title_window = "Mnimalistic Player"
        cv2.namedWindow(title_window)
        cv2.moveWindow(title_window,750,150)
        cap = cv2.VideoCapture(video_file)
        tots = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        cv2.createTrackbar('frame', title_window, 0,int(tots)-1, getFrame)
        if df_checker == False:
            df = pd.DataFrame(columns = label_list, index = range(1, int(tots) + 1))
            df.index.name="Frame No."
            df["Frame No."] = range(1, int(tots) + 1)
            df_checker = True
        else:
            messagebox.showinfo("Information box", "Labels uploaded")
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                current_frames = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                if current_frames in label_1_list and key_label_controler[0] == False:
                    draw_label(label_1_name, (10,20), (255,0,0))
                if current_frames in label_2_list and key_label_controler[0] == False:
                    draw_label(label_2_name, (10,40), (0,0,255))
                if current_frames in label_3_list and key_label_controler[0] == False:
                    draw_label(label_3_name, (10,60), (0,102,0))
                if current_frames in label_4_list and key_label_controler[0] == False:
                    draw_label(label_4_name, (10,80), (204,0,102))
                if current_frames in label_5_list and key_label_controler[0] == False:
                    draw_label(label_5_name, (10,100), (153,153,255))
                if current_frames in label_6_list and key_label_controler[0] == False:
                    draw_label(label_6_name, (10,120), (255,255,153))
                if current_frames in label_7_list and key_label_controler[0] == False:
                    draw_label(label_7_name, (10,140), (0,128,255))
                if current_frames in label_8_list and key_label_controler[0] == False:
                    draw_label(label_8_name, (10,160), (153,153,0))
                if current_frames in label_9_list and key_label_controler[0] == False:
                    draw_label(label_9_name, (10,180), (128,128,128))
                elif current_frames in label_1_list and key_label_controler[0] == True:
                    cv2.imshow(title_window, frame)
                    key_restart(False ,key_label_controler)
                
                else:
                    cv2.imshow(title_window, frame)
                
                cv2.imshow(title_window, frame)
                
                cv2.setTrackbarPos('frame',title_window, int(current_frames))
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
                    cap.release()
                    cv2.destroyAllWindows()
                if keyboard.is_pressed('a'):
                    key_restart(True ,key_label_controler)
                    
                    frame_changer(cap, "back", 1)
                    key_restart(False,key_pressed_list)
                 
                if keyboard.is_pressed('d'):
                    frame_changer(cap, "front", 1)
                    key_restart(False,key_pressed_list)
                    key_restart(False ,key_label_controler)
                    
                if keyboard.is_pressed('p'):
                    cv2.waitKey(-1) #wait until any key is pressed
                    key_restart(False,key_pressed_list)
                if keyboard.is_pressed("r"):
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    cv2.setTrackbarPos('frame',title_window, 0)
                    cv2.waitKey(-1)
                    key_restart(False,key_pressed_list)
                if keyboard.is_pressed('w'):
                    cv2.waitKey(frameTime)
                    key_restart(False,key_pressed_list)
                if keyboard.is_pressed('e'):
                    end_key(df, column)
                if keyboard.is_pressed('1'):
                    previous_column = column
                    column = 0
                    step_mode(df, label_1_name, cap, key_pressed_list[0], column, previous_column, label_1_list)
                    add_to_list( frame_to_list, label_1_list)
                    if key_pressed_list[0] == False:
                        key_restart(True,key_pressed_list)
                    else:
                        continue
                if keyboard.is_pressed('2'):
                    previous_column = column
                    column = 1
                    step_mode(df, label_2_name, cap, key_pressed_list[1], column, previous_column, label_2_list)
                    add_to_list( frame_to_list, label_2_list)
                    if key_pressed_list[1] == False:
                        key_restart(True, key_pressed_list)
                    else:
                        continue
                        
                if keyboard.is_pressed('3'):
                    previous_column = column
                    column = 2
                    step_mode(df, label_3_name, cap, key_pressed_list[2], column, previous_column, label_3_list)
                    add_to_list( frame_to_list, label_3_list)
                    if key_pressed_list[2] == False:
                        key_restart(True,key_pressed_list)
                    else:
                        continue
                if keyboard.is_pressed('4'):
                    previous_column = column
                    column = 3
                    step_mode(df, label_4_name, cap, key_pressed_list[3], column, previous_column, label_4_list)
                    add_to_list( frame_to_list, label_4_list)
                    if key_pressed_list[3] == False:
                        key_restart(True,key_pressed_list)
                    else:
                        continue
                if keyboard.is_pressed('5'):
                    previous_column = column
                    column = 4
                    step_mode(df, label_5_name, cap, key_pressed_list[4], column, previous_column, label_5_list)
                    add_to_list( frame_to_list, label_5_list)
                    if key_pressed_list[4] == False:
                        key_restart(True,key_pressed_list)
                    else:
                        continue
                if keyboard.is_pressed('6'):
                    previous_column = column
                    column = 5
                    step_mode(df, label_6_name, cap, key_pressed_list[5], column, previous_column, label_6_list)
                    add_to_list( frame_to_list, label_6_list)
                    if key_pressed_list[5] == False:
                        key_restart(True,key_pressed_list)
                    else:
                        continue
                if keyboard.is_pressed('7'):
                    previous_column = column
                    column = 6
                    step_mode(df, label_7_name, cap, key_pressed_list[6], column, previous_column, label_7_list)
                    add_to_list( frame_to_list, label_7_list)
                    if key_pressed_list[6] == False:
                        key_restart(True,key_pressed_list)
                    else:
                        continue
                if keyboard.is_pressed('8'):
                    previous_column = column
                    column = 7
                    step_mode(df, label_8_name, cap, key_pressed_list[7], column, previous_column, label_8_list)
                    add_to_list( frame_to_list, label_8_list)
                    if key_pressed_list[7] == False:
                        key_restart(True,key_pressed_list)
                    else:
                        continue
                if keyboard.is_pressed('9'):
                    previous_column = column
                    column = 8
                    step_mode(df, label_9_name, cap, key_pressed_list[8], column, previous_column, label_9_list)
                    add_to_list( frame_to_list, label_9_list)
                    if key_pressed_list[8] == False:
                        key_restart(True,key_pressed_list)
                    else:
                        continue
                if keyboard.is_pressed('g'):
                    delete_mode(df, np.nan, column)
                    key_restart(False,key_pressed_list)
                if keyboard.is_pressed('h'):
                    ctrl_alt_delet(df)
                    key_restart(False,key_pressed_list)
                if keyboard.is_pressed("z"):
                    frame_changer(cap, "back", fps)
                    key_restart(True ,key_label_controler)
                if keyboard.is_pressed("c"):
                    frame_changer(cap, "front", fps)
                    key_restart(True ,key_label_controler)
        xd = df
        cap.release()
        cv2.destroyAllWindows()

video_object = Application()
video_object.root.mainloop()