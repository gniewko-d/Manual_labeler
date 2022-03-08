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

key_pressed = False
frameTime = 50
video_file = None
start_frame = None
start_frame_freezed = None
stop_frame = None
current_label = "test"

label_1_name = f"{None}"
label_2_name = f"{None}"
label_3_name = f"{None}"
label_4_name = f"{None}"
label_5_name = f"{None}"
label_6_name = f"{None}"
label_7_name = f"{None}"
label_8_name = f"{None}"
label_9_name = f"{None}"

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Manual Labeler")
        
        self.first_frame = tk.Frame(self.root)
        self.first_frame.pack()

        self.open_file = tk.Button(self.first_frame, text = "Load video", command = self.easy_open)
        self.open_file.pack(side= tk.LEFT)
        self.text = f"Current video: {None}"
        self.current_video = tk.Text(self.first_frame, height = 1, width = 20)
        self.current_video.insert(tk.INSERT, self.text)
        self.desired_font = tk.font.Font(size = 10, weight = "bold")
        self.current_video.configure(font = self.desired_font)
        self.current_video.pack(side=tk.LEFT)

        self.second_frame = tk.Frame(self.root)
        self.second_frame.pack(side = tk.TOP)

        self.keyboard = tk.Button(self.second_frame, text="Keyboard settings", command = self.keyboard_settings)
        self.keyboard.pack(side=tk.LEFT)
        
        self.label_1_9 = tk.Button(self.second_frame, text="Labels settings", command = self.label_settings)
        self.label_1_9.pack(side=tk.LEFT)
        
        self.third_frame_v1 = tk.Frame(self.root)
        self.third_frame_v1.pack(side = tk.TOP)
        
        self.start_labeling = tk.Button(self.third_frame_v1, text="Start labeling", command = start_vido1)
        self.start_labeling.pack(side=tk.LEFT)
        
    def easy_open(self):
        global video_file
        video_file = easygui.fileopenbox(title="Select An Video", filetypes= [".gif", ".flv", ".avi", ".amv", "*.mp4"])
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
        self.new_root = tk.Toplevel(self.root)
        self.new_root.title("Keyboard_settings")
        self.first_frame_v1 = tk.Frame(self.new_root)
        self.first_frame_v1.pack()
        self.instruction = tk.Text(self.first_frame_v1, height = 30, width = 70)
        self.text_v1 = "Press on your keyboard:\n a = move one frame backward\n d = move one frame forward\n q = escape from video and save markers\n p = pause the video\n r = restart the video (keep the markers applied)\n w = slow down video (have to be pressed constantly)\n e = frame to which (without it) all the preceding ones will\n\t be appropriately marked (depends on labels name set by user).\n\t Start point is set by key 1-9\n key 1-9 = label current frame and jumpt to next one or\n\t set the beginning of the range.\n\t Next you can move to whatever frame (backward or forward)\n\t and there set the end of the range by key e.\n\t All frames within that range will be labeled\n g = delete label of current frame\n h = removes the last labelled range\n"
        conteiner = [""*70, ""*70, self.text_v1, "="*70, "="*70]
        conteiner_v1 = ["green", "grey", "red", "grey", "green"]
        for i in range(len(conteiner)):
            self.instruction.insert(tk.INSERT, conteiner[i])
            self.instruction.pack(side=tk.TOP)
            self.instruction.configure(foreground="green", background= "black")
    def label_settings(self):
        global label_1_name, label_2_name, label_3_name, label_4_name, label_5_name, label_6_name, label_7_name, label_8_name, label_9_name
        self.new_root_2 = tk.Toplevel(self.root)
        self.new_root_2.title("Label_settings")
        
        self.first_frame_v2 = tk.Frame(self.new_root_2)
        self.first_frame_v2.pack()
        
        self.label_1 = tk.Label(self.first_frame_v2, text = "key_1 label:")
        self.label_1.pack(side=tk.LEFT)
        
        self.label_1_text_box = tk.Text(self.first_frame_v2, height = 1, width = 20)
        self.label_1_text_box.insert(tk.INSERT, label_1_name)
        self.label_1_text_box.pack(side=tk.LEFT)
        
        self.second_frame_v1 = tk.Frame(self.new_root_2)
        self.second_frame_v1.pack(side = tk.TOP)
        
        self.label_2 = tk.Label(self.second_frame_v1, text = "key_2 label:")
        self.label_2.pack(side=tk.LEFT)
        
        self.label_2_text_box = tk.Text(self.second_frame_v1, height = 1, width = 20)
        self.label_2_text_box.insert(tk.INSERT, label_2_name)
        self.label_2_text_box.pack(side=tk.LEFT)
        
        self.third_frame = tk.Frame(self.new_root_2)
        self.third_frame.pack(side = tk.TOP)
        
        self.label_3 = tk.Label(self.third_frame, text = "key_3 label:")
        self.label_3.pack(side=tk.LEFT)
        
        self.label_3_text_box = tk.Text(self.third_frame, height = 1, width = 20)
        self.label_3_text_box.insert(tk.INSERT, label_3_name)
        self.label_3_text_box.pack(side=tk.LEFT)

        self.fourth_frame = tk.Frame(self.new_root_2)
        self.fourth_frame.pack(side = tk.TOP)
        
        self.label_4 = tk.Label(self.fourth_frame, text = "key_4 label:")
        self.label_4.pack(side=tk.LEFT)
        
        self.label_4_text_box = tk.Text(self.fourth_frame, height = 1, width = 20)
        self.label_4_text_box.insert(tk.INSERT, label_4_name)
        self.label_4_text_box.pack(side=tk.LEFT)
        
        self.fifth_frame = tk.Frame(self.new_root_2)
        self.fifth_frame.pack(side = tk.TOP)
        
        self.label_5 = tk.Label(self.fifth_frame, text = "key_5 label:")
        self.label_5.pack(side=tk.LEFT)
        
        self.label_5_text_box = tk.Text(self.fifth_frame, height = 1, width = 20)
        self.label_5_text_box.insert(tk.INSERT, label_5_name)
        self.label_5_text_box.pack(side=tk.LEFT)
        
        self.sixth_frame = tk.Frame(self.new_root_2)
        self.sixth_frame.pack(side = tk.TOP)
        
        self.label_6 = tk.Label(self.sixth_frame, text = "key_6 label:")
        self.label_6.pack(side=tk.LEFT)
        
        self.label_6_text_box = tk.Text(self.sixth_frame, height = 1, width = 20)
        self.label_6_text_box.insert(tk.INSERT, label_6_name)
        self.label_6_text_box.pack(side=tk.LEFT)
        
        self.seventh_frame = tk.Frame(self.new_root_2)
        self.seventh_frame.pack(side = tk.TOP)
        
        self.label_7 = tk.Label(self.seventh_frame, text = "key_7 label:")
        self.label_7.pack(side=tk.LEFT)
        
        self.label_7_text_box = tk.Text(self.seventh_frame, height = 1, width = 20)
        self.label_7_text_box.insert(tk.INSERT, label_7_name)
        self.label_7_text_box.pack(side=tk.LEFT)
        
        self.eighth_frame = tk.Frame(self.new_root_2)
        self.eighth_frame.pack(side = tk.TOP)
        
        self.label_8 = tk.Label(self.eighth_frame, text = "key_8 label:")
        self.label_8.pack(side=tk.LEFT)
        
        self.label_8_text_box = tk.Text(self.eighth_frame, height = 1, width = 20)
        self.label_8_text_box.insert(tk.INSERT, label_8_name)
        self.label_8_text_box.pack(side=tk.LEFT)
        
        self.ninth_frame = tk.Frame(self.new_root_2)
        self.ninth_frame.pack(side = tk.TOP)
        
        self.label_9 = tk.Label(self.ninth_frame, text = "key_9 label:")
        self.label_9.pack(side=tk.LEFT)
        
        self.label_9_text_box = tk.Text(self.ninth_frame, height = 1, width = 20)
        self.label_9_text_box.insert(tk.INSERT, label_9_name)
        self.label_9_text_box.pack(side=tk.LEFT)
        
        self.submit_frame = tk.Frame(self.new_root_2)
        self.submit_frame.pack(side = tk.TOP)
        
        self.submit = tk.Button(self.submit_frame, text = "Submit", command = self.label_changer)
        self.submit.pack(side = tk.BOTTOM)

    def label_changer(self):
        global label_1_name, label_2_name, label_3_name, label_4_name, label_5_name, label_6_name, label_7_name, label_8_name, label_9_name

        label_1_name = self.label_1_text_box.get("1.0", "end")
        label_2_name = self.label_2_text_box.get("1.0", "end")
        label_3_name = self.label_3_text_box.get("1.0", "end")
        label_4_name = self.label_4_text_box.get("1.0", "end")
        label_5_name = self.label_5_text_box.get("1.0", "end")
        label_6_name = self.label_6_text_box.get("1.0", "end")
        label_7_name = self.label_7_text_box.get("1.0", "end")
        label_8_name = self.label_8_text_box.get("1.0", "end")
        label_9_name = self.label_9_text_box.get("1.0", "end")


def getFrame(frame_nr):
    global cap
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_nr)


def key_restart(y):
    global key_pressed
    key_pressed = y


def frame_changer(video, direction, frame_num):
    next_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    current_frame = next_frame - 1
    previous_frame = current_frame - frame_num
    next_frame = current_frame + frame_num
    if direction == "back":
        cap.set(cv2.CAP_PROP_POS_FRAMES, previous_frame)
        cv2.setTrackbarPos('frame', title_window, previous_frame)
        cv2.waitKey(-1)  # wait until any key is pressed
    elif direction == "front":
        cap.set(cv2.CAP_PROP_POS_FRAMES, next_frame)
        cv2.setTrackbarPos('frame',title_window, next_frame)
        cv2.waitKey(-1) #wait un


def step_mode(data, label, video):
    global key_pressed, start_frame, current_label
    if key_pressed:
        current_label = label
        inital = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        next_frame = inital + 1
        data.iloc[inital-2, 0] = label
        video.set(cv2.CAP_PROP_POS_FRAMES, inital)
        cv2.setTrackbarPos('frame',title_window, inital)
        cv2.waitKey(0)
    else:
        start_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        inital = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        next_frame = inital + 1
        df.iloc[inital-1, 0] = label
        video.set(cv2.CAP_PROP_POS_FRAMES, next_frame)
        cv2.setTrackbarPos('frame',title_window, next_frame)
        key_restart(y = True)
        cv2.waitKey(0)


def end_key(data, label):
    global start_frame, key_pressed, start_frame_freezed, stop_frame
    if key_pressed:
        
        stop_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        start_frame_freezed = start_frame
        if stop_frame >= start_frame:
            data.iloc[start_frame-1:stop_frame-1, 0] = label
            cv2.waitKey(-1)
        elif stop_frame < start_frame:
            data.iloc[stop_frame:start_frame-1, 0] = label
            cv2.waitKey(-1)
    else:
        print("First, set the beginning of range")

def delete_mode(data, label):
    current_frames = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    df.iloc[current_frames-1, 0] = label
    cv2.waitKey(-1)
def ctrl_alt_delet(data):
    global stop_frame, start_frame_freezed
    if stop_frame >= start_frame_freezed:
            data.iloc[start_frame_freezed-1:stop_frame, 0] = np.nan
            cv2.waitKey(-1)
    elif stop_frame < start_frame_freezed:
        print("Putin huj")    
        data.iloc[stop_frame:start_frame_freezed, 0] = np.nan
        cv2.waitKey(-1)

xd = None
# Closes all the frames
cv2.destroyAllWindows()
video_object = Application()
video_object.root.mainloop()
def start_vido1():
    global label_1_name, xd, cap, title_window, frameTime, df
    title_window = "Mnimalistic Player"
    cv2.namedWindow(title_window)
    cv2.moveWindow(title_window,750,150)
    if video_file == None:
        messagebox.showerror("Error box", "Upload the video first ")
    else:
        cap = cv2.VideoCapture(video_file)
        tots = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        cv2.createTrackbar('frame', title_window, 0,int(tots)-1, getFrame)
        df = pd.DataFrame(columns = [label_1_name], index = range(1, int(tots) + 1))
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                cv2.imshow(title_window, frame)
                current_frames = cap.get(cv2.CAP_PROP_POS_FRAMES)
                cv2.setTrackbarPos('frame',title_window, int(current_frames))
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
                    cap.release()
                    cv2.destroyAllWindows()
                if keyboard.is_pressed('a'):
                    frame_changer(cap, "back", 1)
                if keyboard.is_pressed('d'):
                    frame_changer(cap, "front", 1)
                if keyboard.is_pressed('p'):
                    cv2.waitKey(-1) #wait until any key is pressed
                if keyboard.is_pressed("r"):
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    cv2.setTrackbarPos('frame',title_window, 0)
                    cv2.waitKey(-1)
                if keyboard.is_pressed('w'):
                    cv2.waitKey(frameTime)
                if keyboard.is_pressed('e'):
                    end_key(df, current_label)
                if keyboard.is_pressed('1'):
                    step_mode(df, label_1_name, cap)
                if keyboard.is_pressed('g'):
                    delete_mode(df, np.nan)
                if keyboard.is_pressed('h'):
                    ctrl_alt_delet(df)
        xd = df
        cap.release()
        cv2.destroyAllWindows()