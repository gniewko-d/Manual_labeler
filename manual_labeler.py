# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 15:01:40 2022

@author: gniew
"""
import keyboard
import cv2
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox
import easygui
from pandastable import Table
import csv
import pyttsx3
import random
from PIL import Image, ImageTk
import time
import requests
from io import BytesIO


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
label_list = None
available_formats = ["flv", "avi", "amv", "mp4"]



def advert():
    root_v1 = tk.Tk()
    root_v1.title("Ad")
    url = "https://i.postimg.cc/hjpLn1gY/image-v1-1.png"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = ImageTk.PhotoImage(img)
    label1 = tk.Label(root_v1,image= img, bg = "black")
    label1.pack()
    root_v1.after(3000, lambda: root_v1.destroy())
    root_v1.mainloop()
advert()

label_1_name = f"{None}"
label_2_name = f"{None}"
label_3_name = f"{None}"
label_4_name = f"{None}"
label_5_name = f"{None}"
label_6_name = f"{None}"
label_7_name = f"{None}"
label_8_name = f"{None}"
label_9_name = f"{None}"
configruation_title = f"{None}"

label_1_list = []
label_2_list = []
label_3_list = []
label_4_list = []
label_5_list = []
label_6_list = []
label_7_list = []
label_8_list = []
label_9_list = []
key_unlocker = [False, False, False, False, False, False, False, False, False]
key_pressed_list = [False, False, False, False, False, False, False, False, False]
key_label_controler = [False]

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Manual Labeler")
        self.root.protocol("WM_DELETE_WINDOW", disable_event)
    
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
        
    
        self.fifth_frame_v1 = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.fifth_frame_v1.pack(side = tk.TOP)
        self.fifth_frame_v1.pack_propagate(0)
    
        self.save_machine_state = tk.Button(self.fifth_frame_v1, text = "Save current state", command = run_save_machine_state, background="black", foreground="green", width = 17)
        self.save_machine_state.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.load_machine_state = tk.Button(self.fifth_frame_v1, text = "Load state from file", command = load_machine_state_fun, background="black", foreground="green")
        self.load_machine_state.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.sixth_frame = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.sixth_frame.pack(side = tk.TOP)
        self.sixth_frame.pack_propagate(0)
        
        self.create_configuration = tk.Button(self.sixth_frame, text = "Create configuration", command = self.creat_configuration_fun, background="black", foreground="green", width = 19)
        self.create_configuration.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.load_configuration = tk.Button(self.sixth_frame, text = "Load configuration", command = lambda:[load_configuration_fun(), self.label_changer()], background="black", foreground="green", width = 17)
        self.load_configuration.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.fourth_frame_v1 = tk.Frame(self.root, background="#116562", width=400, height = 30)
        self.fourth_frame_v1.pack(side = tk.TOP)
        self.fourth_frame_v1.pack_propagate(0)
        
        self.save_labeled_video = tk.Button(self.fourth_frame_v1, text= "Save data", command = start_vido3, background="black", foreground="green", width = 5)
        self.save_labeled_video.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.close_gui = tk.Button(self.fourth_frame_v1, text= "Exit", command = self.close_gate, background="black", foreground="green", activebackground = "white")
        self.close_gui.pack(side=tk.LEFT, padx=1, pady=1, expand=True, fill='both')
        
        self.engine = pyttsx3.init()
        self.list_of_voices = ['Hello World', "welcome to the Labeling world", "hello friend", "I wish you fruitful work", "hello user", "I will try my best to help you work", "What a nice day to label something"]
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.say(random.choice(self.list_of_voices))
        self.engine.runAndWait()
    
    def close_gate(self):
        msgbox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the application? Unsaved data will be lost',icon = 'warning')
        if msgbox == "yes":
            self.root.destroy()
        else:
            pass
    
    
    def easy_open(self):
        global video_file, available_formats
        video_file = easygui.fileopenbox(title="Select An Video", filetypes= ["*.gif", "*.flv", "*.avi", "*.amv", "*.mp4"])
        if video_file != None:
            messagebox.showinfo("Information box", "Video uploaded")
            video_title = video_file.split("\\")
            video_format = video_title[-1].split(".")
            video_format = video_format[-1].lower()
            if video_format in available_formats:
                self.current_video.delete("1.0","end")
                self.text = f"Current video: {video_title[-1]}"
                self.current_video.configure(width = len(self.text))
                self.current_video.insert(tk.INSERT, self.text)
            else:
                messagebox.showerror("Error box", "Wrong format of video!")
                messagebox.showinfo("Information box", f'Currently available formats: .flv, .avi, .amv, .mp4, \nformat of your video : {video_format}')
        else:
            messagebox.showerror("Error box", "Video was not loaded")
    
    def keyboard_settings(self):
        global fps
        self.new_root = tk.Toplevel(self.root)
        self.new_root.title("Keyboard_settings")
        
        self.first_frame_v1 = tk.Frame(self.new_root, background="black")
        self.first_frame_v1.pack(expand=True, fill='both')
        self.instruction = tk.Text(self.first_frame_v1, height = 23, width = 70)
        self.text_v1 = "Press on your keyboard:\n a = move one frame backward\n d = move one frame forward\n q = escape from video and save markers\n p = pause the video\n r = restart the video (keep the markers applied)\n w = slow down video (have to be pressed constantly)\n e = frame to which (without it) all the preceding ones will\n\t be appropriately marked (depends on labels name set by user).\n\t Start point is set by key 1-9\n key 1-9 = label current frame and jumpt to next one or\n\t set the beginning of the range.\n\t Next you can move to whatever frame (backward or forward)\n\t and there set the end of the range by key e.\n\t All frames within that range will be labeled\n g = delete last used label from current frame\n h = removes the last labelled range\n z = move x (default = 5) frames backward\n c = move x (default = 5) frames forward\n"
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
        
        self.submit = tk.Button(self.submit_frame, text = "Submit", command =  self.label_changer, foreground="green", background= "black")
        self.submit.pack(side = tk.BOTTOM)
    
    def creat_configuration_fun(self):
        global label_1_name, label_2_name, label_3_name, label_4_name, label_5_name, label_6_name, label_7_name, label_8_name, label_9_name, configruation_title
        self.new_root_4 = tk.Toplevel(self.root, background= "black")
        self.new_root_4.title("Label_configuration")
        
        self.first_frame_v3 = tk.Frame(self.new_root_4, background="black")
        self.first_frame_v3.pack()
        
        self.label_1_v1 = tk.Label(self.first_frame_v3, text = "key_1 label:", foreground="green", background= "black")
        self.label_1_v1.pack(side=tk.LEFT)
        
        self.label_1_v1_text_box = tk.Text(self.first_frame_v3, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_1_v1_text_box.insert(tk.INSERT, label_1_name)
        self.label_1_v1_text_box.pack(side=tk.LEFT)
        
        self.second_frame_v2 = tk.Frame(self.new_root_4, background= "black")
        self.second_frame_v2.pack(side = tk.TOP)
        
        self.label_2_v1 = tk.Label(self.second_frame_v2, text = "key_2 label:", foreground="green", background= "black")
        self.label_2_v1.pack(side=tk.LEFT)
        
        self.label_2_v1_text_box = tk.Text(self.second_frame_v2, height = 1, width = 20, foreground="green", background= "black",insertbackground = "white")
        self.label_2_v1_text_box.insert(tk.INSERT, label_2_name)
        self.label_2_v1_text_box.pack(side=tk.LEFT)
        
        self.third_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.third_frame_v1.pack(side = tk.TOP)
        
        self.label_3_v1 = tk.Label(self.third_frame_v1, text = "key_3 label:", foreground="green", background= "black")
        self.label_3_v1.pack(side=tk.LEFT)
        
        self.label_3_v1_text_box = tk.Text(self.third_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_3_v1_text_box.insert(tk.INSERT, label_3_name)
        self.label_3_v1_text_box.pack(side=tk.LEFT)
        
        self.fourth_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.fourth_frame_v1.pack(side = tk.TOP)
        
        self.label_4_v1 = tk.Label(self.fourth_frame_v1, text = "key_4 label:", foreground="green", background= "black")
        self.label_4_v1.pack(side=tk.LEFT)
        
        self.label_4_v1_text_box = tk.Text(self.fourth_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_4_v1_text_box.insert(tk.INSERT, label_4_name)
        self.label_4_v1_text_box.pack(side=tk.LEFT)
        
        self.fifth_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.fifth_frame_v1.pack(side = tk.TOP)
        
        self.label_5_v1 = tk.Label(self.fifth_frame_v1, text = "key_5 label:", foreground="green", background= "black")
        self.label_5_v1.pack(side=tk.LEFT)
        
        self.label_5_v1_text_box = tk.Text(self.fifth_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_5_v1_text_box.insert(tk.INSERT, label_5_name)
        self.label_5_v1_text_box.pack(side=tk.LEFT)
        
        self.sixth_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.sixth_frame_v1.pack(side = tk.TOP)
        
        self.label_6_v1 = tk.Label(self.sixth_frame_v1, text = "key_6 label:", foreground="green", background= "black")
        self.label_6_v1.pack(side=tk.LEFT)
        
        self.label_6_v1_text_box = tk.Text(self.sixth_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_6_v1_text_box.insert(tk.INSERT, label_6_name)
        self.label_6_v1_text_box.pack(side=tk.LEFT)
        
        self.seventh_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.seventh_frame_v1.pack(side = tk.TOP)
        
        self.label_7_v1 = tk.Label(self.seventh_frame_v1, text = "key_7 label:", foreground="green", background= "black")
        self.label_7_v1.pack(side=tk.LEFT)
        
        self.label_7_v1_text_box = tk.Text(self.seventh_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_7_v1_text_box.insert(tk.INSERT, label_7_name)
        self.label_7_v1_text_box.pack(side=tk.LEFT)
        
        
        self.eighth_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.eighth_frame_v1.pack(side = tk.TOP)
        
        self.label_8_v1 = tk.Label(self.eighth_frame_v1, text = "key_8 label:", foreground="green", background= "black")
        self.label_8_v1.pack(side=tk.LEFT)
        
        self.label_8_v1_text_box = tk.Text(self.eighth_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_8_v1_text_box.insert(tk.INSERT, label_8_name)
        self.label_8_v1_text_box.pack(side=tk.LEFT)
        
        self.ninth_frame_v1 = tk.Frame(self.new_root_4, background= "black")
        self.ninth_frame_v1.pack(side = tk.TOP)
        
        self.label_9_v1 = tk.Label(self.ninth_frame_v1, text = "key_9 label:", foreground="green", background= "black")
        self.label_9_v1.pack(side=tk.LEFT)
        
        self.label_9_v1_text_box = tk.Text(self.ninth_frame_v1, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_9_v1_text_box.insert(tk.INSERT, label_9_name)
        self.label_9_v1_text_box.pack(side=tk.LEFT)
        
        self.tenth_frame = tk.Frame(self.new_root_4, background= "black")
        self.tenth_frame.pack(side = tk.TOP)
        
        self.label_10 = tk.Label(self.tenth_frame, text = "Configuration title:", foreground="green", background= "black")
        self.label_10.pack(side=tk.LEFT, pady=10)
        
        self.label_10_text_box = tk.Text(self.tenth_frame, height = 1, width = 20, foreground="green", background= "black", insertbackground = "white")
        self.label_10_text_box.insert(tk.INSERT, configruation_title)
        self.label_10_text_box.pack(side=tk.LEFT, pady=15)
        
        self.save_v1_frame = tk.Frame(self.new_root_4, background= "black")
        self.save_v1_frame.pack(side = tk.TOP)
        
        self.submit = tk.Button(self.save_v1_frame, text = "Save", command = self.label_configurator_save, foreground="green", background= "black")
        self.submit.pack(side = tk.BOTTOM)
        
    
    def label_changer(self):
        global label_1_name, label_2_name, label_3_name, label_4_name, label_5_name, label_6_name, label_7_name, label_8_name, label_9_name, label_list, key_unlocker
        
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
        messagebox.showinfo("Information box", "Labels updated")

    def label_configurator_save(self):
        
        list_configuration = []
        list_configuration.append(self.label_1_v1_text_box.get("1.0", "end-1c"))
        list_configuration.append(self.label_2_v1_text_box.get("1.0", "end-1c"))
        list_configuration.append(self.label_3_v1_text_box.get("1.0", "end-1c"))
        list_configuration.append(self.label_4_v1_text_box.get("1.0", "end-1c"))
        list_configuration.append(self.label_5_v1_text_box.get("1.0", "end-1c"))
        list_configuration.append(self.label_6_v1_text_box.get("1.0", "end-1c"))
        list_configuration.append(self.label_7_v1_text_box.get("1.0", "end-1c"))
        list_configuration.append(self.label_8_v1_text_box.get("1.0", "end-1c"))
        list_configuration.append(self.label_9_v1_text_box.get("1.0", "end-1c"))
        list_configuration.append(self.label_10_text_box.get("1.0", "end-1c"))
        save_file2 = None
        save_file2 = easygui.diropenbox(msg = "Select folder for a save location", title = "Typical window")
        if save_file2 == None:
            messagebox.showerror("Error box", "Folder was not selected, data unsaved")
        else:
            save_file2 = save_file2 + "\\" + list_configuration[9] + ".txt"
            text_for_conf = open(save_file2, "w")
            for i in list_configuration:
                text_for_conf.write(i + "\n")
            text_for_conf.close()
            messagebox.showinfo("Information box", "Configuration saved :):):)")
            messagebox.showinfo("Information box", "Do not change the content of created files")
    def draw_table(self):
        global df, df_checker
        
        if df_checker == False:
            messagebox.showerror("Error box", "To see your data frame first press start labeling")
        names_columns = df.columns.tolist()
        names_columns[0:9]= label_list
        df.columns = names_columns
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

def rescale_frame(percent):
    global cap, dim, width, height
    if percent != 100 and percent != 0:
        dif = percent/100
        width1 = width * dif
        height1 = height * dif
        dim = (int(width1), int(height1))
    elif percent == 0:
        dif = 1/100
        width1 = width * dif
        height1 = height * dif
        dim = (int(width1), int(height1))
def video_resolution(resolution):
    global slow_motion
    if resolution == 0:
        slow_motion = 1
    elif resolution == 1: 
        slow_motion = 10
    elif resolution == 2:
        slow_motion = 100
    elif resolution == 3:
        slow_motion = 200
        

def getFrame(frame_nr):
    global cap
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_nr)

def disable_event():
    pass

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
        start_frame_bool = True
        frame_to_list = inital
        cv2.waitKey(0)
    elif key_pressed:
        start_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        inital = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        next_frame = inital + 1
        data.iloc[inital-2,column] = label
        video.set(cv2.CAP_PROP_POS_FRAMES, inital)
        cv2.setTrackbarPos('frame',title_window, inital)
        frame_to_list = inital-1
        start_frame_bool = True
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
        range_frame = stop_frame - start_frame 
        if range_frame == 2 or range_frame == 1:
            messagebox.showerror("Error box", "Your range is too short (at least 4 frames). Use step method")
            start_frame_bool = False
        elif stop_frame >= start_frame:
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
    global current_label_list, current_label
    try:
        current_frames = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        df.iloc[current_frames-1, column] = label
        current_label_list.remove(current_frames)
        cv2.waitKey(-1)
    except ValueError:
        messagebox.showerror("Error box", f"Frame unlabeled or wrong label to delet (current label :{current_label})")
def ctrl_alt_delet(data):
    global stop_frame, start_frame_freezed, current_label_list
    try:
        if stop_frame >= start_frame_freezed:
            data.iloc[start_frame_freezed-2:stop_frame, column] = np.nan
            z = [current_label_list.remove(i) for i in range(start_frame_freezed-1, stop_frame) if i in current_label_list]
            cv2.waitKey(-1)
        elif stop_frame < start_frame_freezed:
            data.iloc[stop_frame:start_frame_freezed, column] = np.nan
            cv2.waitKey(-1)
    except TypeError:
        messagebox.showerror("Error box", "First, set the beginning (key 1-9) and the end (key e) of the range")

def save_machine_state_fun(mother_list, *args):
    
    mother_list = []
    zz = [mother_list.append(i) for i in args]
    xx = [i.append("exist") for i in mother_list if len(i) == 0]
    return mother_list

def run_save_machine_state():
    global df, video_file, label_list
    if video_file == None or label_list == None or df_checker == False:
        messagebox.showerror("Error box", "Before save current state:\n 1. Upload the video \n 2. Submit any label \n 3. Label something")
    else:
        mother_df = df
        mother_list = []
        save_file1 = None
        save_file1 = easygui.diropenbox(msg = "Select folder for a save location", title = "Typical window")
        if save_file1 == None:
            messagebox.showerror("Error box", "Folder was not selected, data unsaved")
        else:
            messagebox.showinfo("Information box", "Folder added :):):)")
            messagebox.showinfo("Information box", "Do not change the content of created files")
            video_title = video_file.split("\\")
            video_title = video_title[-1].split(".")
            save_mother_df = save_file1 + "\\" + video_title[0] + "_mother_A.xlsx"
            mother_df.to_excel(save_mother_df)
            mother_list = save_machine_state_fun(mother_list, label_1_list, label_2_list, label_3_list, label_4_list, label_5_list, label_6_list, label_7_list, label_8_list, label_9_list)
            with open(save_file1 + "\\" + video_title[0] + "_mother_B.csv", "w", newline = "") as f:
                mother_list_writer = csv.writer(f)
                mother_list_writer.writerows(mother_list)
 
def load_machine_state_fun():
    global df, label_1_name, label_2_name, label_3_name, label_4_name, label_5_name, label_6_name, label_7_name, label_8_name, label_9_name, label_1_list, label_2_list, label_3_list, label_4_list, label_5_list, label_6_list, label_7_list, label_8_list, label_9_list, df_checker, label_list
    if video_file == None:
        messagebox.showerror("Error box", "Before you load state from file: Upload the video first")
    else:
        video_title = video_file.split("\\")
        video_title = video_title[-1].split(".")
        messagebox.showinfo("Information box", f"Load file named: {video_title[0]}_mother_A")
        df_loaded = easygui.fileopenbox(title="Select a file", filetypes= ["*.gif", "*.flv", "*.avi", "*.amv", "*.mp4"])
        
        df_loaded_checker = df_loaded.split("\\")
        df_loaded_checker = df_loaded_checker[-1].split(".")
        

        
        df_loaded = pd.read_excel(df_loaded)
        df_loaded = df_loaded.set_index("Frame No.")
        cap2 = cv2.VideoCapture(video_file)
        tots2 = int(cap2.get(cv2.CAP_PROP_FRAME_COUNT))
        cap2.release()
        if df_loaded_checker[0] == f"{video_title[0]}_mother_A" and tots2 == len(df_loaded):
            
            df = df_loaded
            list_of_columns = list(df.columns)
            list_of_columns = ["None" if "None" in i else i for i in list_of_columns]
            list_of_columns = ["Frame No." if "Frame No" in i else i for i in list_of_columns]
            df.columns = list_of_columns
            list_of_columns = list(df.columns)
            df_checker = True
            if list_of_columns[0] != "None":
                label_1_name = list_of_columns[0]
            if list_of_columns[1] != "None":
                label_2_name = list_of_columns[1]
            if list_of_columns[2] != "None":
                label_3_name = list_of_columns[2]
            if list_of_columns[3] != "None":
                label_4_name = list_of_columns[3]
            if list_of_columns[4] != "None":
                label_5_name = list_of_columns[4]
            if list_of_columns[5] != "None":
                label_6_name = list_of_columns[5]
            if list_of_columns[6] != "None":
                label_7_name = list_of_columns[6]
            if list_of_columns[7] != "None":
                label_8_name = list_of_columns[7]
            if list_of_columns[8] != "None":
                label_9_name = list_of_columns[8]
        
            label_list = [label_1_name, label_2_name, label_3_name, label_4_name, label_5_name, label_6_name, label_7_name, label_8_name, label_9_name]
            messagebox.showinfo("Information box", f"Next, load file named: {video_title[0]}_mother_B")
            csv_label_list = easygui.fileopenbox(title="Select a file", filetypes= ["*.gif", "*.flv", "*.avi", "*.amv", "*.mp4"])
            csv_label_list_split = csv_label_list.split("\\")
            csv_label_list_split = csv_label_list_split[-1].split(".")
            if csv_label_list_split[0] == f"{video_title[0]}_mother_B":
                with open (csv_label_list) as csv_file_mother_b:
                    csv_reader = csv.reader(csv_file_mother_b, delimiter=',')
                    for i,j in enumerate(csv_reader):
                        if i == 0 and j[0] != "exist":
                            j = [int(d) for d in j]
                            label_1_list = j
                        elif i == 1 and j[0] != "exist":
                            j = [int(d) for d in j]
                            label_2_list = j
                        elif i == 2 and j[0] != "exist":
                            j = [int(d) for d in j]
                            label_3_list = j
                        elif i == 3 and j[0] != "exist":
                            j = [int(d) for d in j]
                            label_4_list = j
                        elif i == 4 and j[0] != "exist":
                            j = [int(d) for d in j]
                            label_5_list = j
                        elif i == 5 and j[0] != "exist":
                            j = [int(d) for d in j]
                            label_6_list = j
                        elif i == 6 and j[0] != "exist":
                            j = [int(d) for d in j]
                            label_7_list = j
                        elif i == 7 and j[0] != "exist":
                            j = [int(d) for d in j]
                            label_8_list = j
                        elif i == 8 and j[0] != "exist":
                            j = [int(d) for d in j]
                            label_9_list = j
                messagebox.showinfo("Information box", "Data and labels loaded")
            else:
                messagebox.showerror("Error box", "Wrong file uploaded. Try again")
        else:
            messagebox.showerror("Error box", "Wrong file uploaded. Try again")
            
    
def start_vido1():
    global label_1_name, xd, cap, title_window, frameTime, df, fps, key_pressed_list, previous_column, column, frame, df_checker, label_1_list, label_2_list, label_3_list, label_4_list, label_5_list, label_6_list, label_7_list, label_8_list, label_9_list, key_label_controler, label_1_list_key_a, width, height, dim, slow_motion
    if video_file == None:
        messagebox.showerror("Error box", "Upload the video first")
    elif label_list == None:
        messagebox.showerror("Error box", "Before you start labeling you have to submit any label first")
    else:
        title_window = "Mnimalistic Player"
        cv2.namedWindow(title_window)
        cv2.moveWindow(title_window,750,150)
        cap = cv2.VideoCapture(video_file)
        tots = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps =  cap.get(cv2.CAP_PROP_FPS)
        print(fps)
        width = float(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = float(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cv2.createTrackbar('frame', title_window, 0,int(tots)-1, getFrame)
        cv2.createTrackbar('video size', title_window, 100, 200, rescale_frame)
        cv2.createTrackbar('video spped', title_window, 0, 3, video_resolution)
        dim = (int(width), int(height))
        slow_motion = 1
        if df_checker == False:
            df = pd.DataFrame(columns = label_list, index = range(1, int(tots) + 1))
            df.index.name="Frame No."
            df["Frame No."] = range(1, int(tots) + 1)
            df_checker = True
        else:
            messagebox.showinfo("Information box", "Labels uploaded")
            names_columns = df.columns.tolist()
            names_columns[0:9]= label_list
            df.columns = names_columns
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
                elif (current_frames in label_1_list or current_frames in label_2_list or current_frames in label_3_list or current_frames in label_4_list or current_frames in label_5_list or current_frames in label_6_list or current_frames in label_7_list or current_frames in label_8_list or current_frames in label_9_list) and key_label_controler[0] == True:
                    frame1 = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
                    cv2.imshow(title_window, frame1)
                    cv2.waitKey(slow_motion)
                    key_restart(False ,key_label_controler)
                    
                else:

                    frame1 = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
                    cv2.imshow(title_window, frame1)
                    cv2.waitKey(slow_motion)
                frame1 = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
                cv2.imshow(title_window, frame1)
                cv2.waitKey(slow_motion)
                cv2.setTrackbarPos('frame',title_window, int(current_frames))
                if cv2.waitKey(25) & 0xFF == ord('q'):
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
                
                if label_1_name != "None":
                    if keyboard.is_pressed('1'):
                        previous_column = column
                        column = 0
                        step_mode(df, label_1_name, cap, key_pressed_list[0], column, previous_column, label_1_list)
                        add_to_list(frame_to_list, label_1_list)
                        if key_pressed_list[0] == False:
                            key_restart(True,key_pressed_list)
                        else:
                            continue
                
                if label_2_name != "None":
                    if keyboard.is_pressed('2'):
                        previous_column = column
                        column = 1
                        step_mode(df, label_2_name, cap, key_pressed_list[1], column, previous_column, label_2_list)
                        add_to_list(frame_to_list, label_2_list)
                        if key_pressed_list[1] == False:
                            key_restart(True,key_pressed_list)
                        else:
                            continue
                
                if label_3_name != "None":
                    if keyboard.is_pressed('3'):
                        previous_column = column
                        column = 2
                        step_mode(df, label_3_name, cap, key_pressed_list[2], column, previous_column, label_3_list)
                        add_to_list(frame_to_list, label_3_list)
                        if key_pressed_list[2] == False:
                            key_restart(True,key_pressed_list)
                        else:
                            continue
                        
                if label_4_name != "None":
                    if keyboard.is_pressed('4'):
                        previous_column = column
                        column = 3
                        step_mode(df, label_4_name, cap, key_pressed_list[3], column, previous_column, label_4_list)
                        add_to_list(frame_to_list, label_4_list)
                        if key_pressed_list[3] == False:
                            key_restart(True,key_pressed_list)
                        else:
                            continue
                
                if label_5_name != "None":
                    if keyboard.is_pressed('5'):
                        previous_column = column
                        column = 4
                        step_mode(df, label_5_name, cap, key_pressed_list[4], column, previous_column, label_5_list)
                        add_to_list(frame_to_list, label_5_list)
                        if key_pressed_list[4] == False:
                            key_restart(True,key_pressed_list)
                        else:
                            continue
                
                if label_6_name != "None":
                    if keyboard.is_pressed('6'):
                        previous_column = column
                        column = 5
                        step_mode(df, label_6_name, cap, key_pressed_list[5], column, previous_column, label_6_list)
                        add_to_list(frame_to_list, label_6_list)
                        if key_pressed_list[5] == False:
                            key_restart(True,key_pressed_list)
                        else:
                            continue
                
                if label_7_name != "None":
                    if keyboard.is_pressed('7'):
                        previous_column = column
                        column = 6
                        step_mode(df, label_7_name, cap, key_pressed_list[6], column, previous_column, label_7_list)
                        add_to_list(frame_to_list, label_7_list)
                        if key_pressed_list[6] == False:
                            key_restart(True,key_pressed_list)
                        else:
                            continue
                
                if label_8_name != "None":
                    if keyboard.is_pressed('8'):
                        previous_column = column
                        column = 7
                        step_mode(df, label_8_name, cap, key_pressed_list[7], column, previous_column, label_8_list)
                        add_to_list(frame_to_list, label_8_list)
                        if key_pressed_list[7] == False:
                            key_restart(True,key_pressed_list)
                        else:
                            continue
                
                if label_9_name != "None":
                    if keyboard.is_pressed('9'):
                        previous_column = column
                        column = 8
                        step_mode(df, label_9_name, cap, key_pressed_list[8], column, previous_column, label_9_list)
                        add_to_list(frame_to_list, label_9_list)
                        if key_pressed_list[7] == False:
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
                    frame_changer(cap, "back", int(fps))
                    key_restart(True ,key_label_controler)
                if keyboard.is_pressed("c"):
                    frame_changer(cap, "front", int(fps))
                    key_restart(True ,key_label_controler)
            else:
                print("koniec")
                xd = df
                cap.release()
                cv2.destroyAllWindows()
def start_vido3():
    global label_1_name, xd, cap, title_window, frameTime, df, fps, key_pressed_list, previous_column, column, frame, df_checker, label_1_list, label_2_list, label_3_list, label_4_list, label_5_list, label_6_list, label_7_list, label_8_list, label_9_list, key_label_controler, label_1_list_key_a, video_title
    if video_file == None:
        messagebox.showerror("Error box", "Upload the video first")
    else:
        cap = cv2.VideoCapture(video_file)
        tots = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        video_title = video_file.split("\\")
        video_title = video_title[-1].split(".")
        save_file = None
        save_file = easygui.diropenbox(msg = "Select folder for a save location", title = "Typical window")
        if save_file == None:
            messagebox.showerror("Error box", "Folder was not selected")
        else:
            messagebox.showinfo("Information box", "Folder added :):):)")
        if df_checker == False:
            df = pd.DataFrame(columns = label_list, index = range(1, int(tots) + 1))
            df.index.name="Frame No."
            df["Frame No."] = range(1, int(tots) + 1)
            df_checker = True
        else:
            messagebox.showinfo("Information box", "Labels uploaded")
        save_file_excel = save_file + "\\" + video_title[0] + ".xlsx"
        df.to_excel(save_file_excel)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        size = (frame_width, frame_height)
        save_file = save_file + "\\" + video_title[0] + "_labeled.mp4"
        out = cv2.VideoWriter(save_file, fourcc, 30.0, size)
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
                out.write(frame)
            else:
                messagebox.showinfo("Information box", "Video and data were saved successfully :):):)")
                xd = df
                cap.release()
                out.release()
                cv2.destroyAllWindows()
def load_configuration_fun():
    global df, label_1_name, label_2_name, label_3_name, label_4_name, label_5_name, label_6_name, label_7_name, label_8_name, label_9_name, label_1_list, label_2_list, label_3_list, label_4_list, label_5_list, label_6_list, label_7_list, label_8_list, label_9_list, df_checker,label_list 
    configuration_labels_v1 = []
    configuration_loaded = None
    messagebox.showinfo("Information box", "Load configuration file (.txt)")
    configuration_loaded = easygui.fileopenbox(title="Select a file", filetypes= ["*.txt"])
    if configuration_loaded == None:
            messagebox.showerror("Error box", "Configuration not loaded")
    else:
        with open (configuration_loaded) as content:
            configuration_labels_v1 = content.readlines()
            for i, j in enumerate(configuration_labels_v1):
                configuration_labels_v1[i] = j.replace("\n", "")
        
        if configuration_labels_v1[0] != "None":
            label_1_name = configuration_labels_v1[0]
        if configuration_labels_v1[1] != "None":
            label_2_name = configuration_labels_v1[1]
        if configuration_labels_v1[2] != "None":
            label_3_name = configuration_labels_v1[2]
        if configuration_labels_v1[3] != "None":
            label_4_name = configuration_labels_v1[3]
        if configuration_labels_v1[4] != "None":
            label_5_name = configuration_labels_v1[4]
        if configuration_labels_v1[5] != "None":
            label_6_name = configuration_labels_v1[5]
        if configuration_labels_v1[6] != "None":
            label_7_name = configuration_labels_v1[6]
        if configuration_labels_v1[7] != "None":
            label_8_name = configuration_labels_v1[7]
        if configuration_labels_v1[8] != "None":
            label_9_name = configuration_labels_v1[8]
        label_list = [label_1_name, label_2_name, label_3_name, label_4_name, label_5_name, label_6_name, label_7_name, label_8_name, label_9_name]
        messagebox.showinfo("Information box", "Labels updated")

video_object = Application()
video_object.root.mainloop()
