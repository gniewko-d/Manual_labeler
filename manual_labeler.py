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


video_file = None


class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Manual Labeler")
        
        self.first_frame = tk.Frame(self.root)
        self.first_frame.pack()

        self.open_file = tk.Button(self.first_frame, text = "Open video", command = self.easy_open)
        self.open_file.pack(side= tk.LEFT)
        self.text = f"Current video: {None}"
        self.current_video = tk.Text(self.first_frame, height = 1, width = 20)
        self.current_video.insert(tk.INSERT, self.text)
        self.desired_font = tk.font.Font( size = 10, weight = "bold")
        self.current_video.configure(font = self.desired_font)
        self.current_video.pack(side=tk.LEFT)

        self.second_frame = tk.Frame(self.root)
        self.second_frame.pack(side = tk.BOTTOM)

        self.keyboard = tk.Button(self.second_frame, text="Keyboard settings", command = self.keyboard_settings)
        self.keyboard.pack(side=tk.LEFT)
        
        self.label_settings = tk.Button(self.second_frame, text="Labels settings")
        self.label_settings.pack(side=tk.LEFT)
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
        self.new_root = tk.Toplevel(self.root)
        self.new_root.title("Keyboard_settings")
        self.first_frame_v1 = tk.Frame(self.new_root)
        self.first_frame_v1.pack()
        self.instruction = tk.Text(self.first_frame_v1, height = 30, width = 62)
        self.text_v1 = "Press on your keyboard:\n a = move one frame backward\n d = move one frame forward\n q = escape from video and save markers\n p = pause the video\n r = restart the video (keep the markers applied)\n w = slow down video (have to be pressed constantly)\n e = frame to which (without it) all the preceding ones will\n be appropriately marked (depends on labels name set by user).\n Start point is set by key 1-10\n key 1-10 = label current frame and jumpt to next one or\n set the beginning of the range.\n Next you can move to whatever frame (backward or forward) and\n there set the end of the range by key e.\n All frames within that range will be labeled\n g = delete label of current frame\n h = removes the last labelled range"
        self.instruction.insert(tk.INSERT, self.text_v1)
        self.instruction.pack(side=tk.TOP)
def flick(x):
    pass


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
    global key_pressed, start_frame
    if key_pressed:
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
video_file = easygui.fileopenbox(title="Select An Video", filetypes= ["*.gif", "*.flv", "*.avi", "*.amv", "*.mp4"])

title_window = "Mnimalistic Player"
cv2.namedWindow(title_window)
cv2.moveWindow(title_window,750,150)
cap = cv2.VideoCapture(video_file)
tots = cap.get(cv2.CAP_PROP_FRAME_COUNT)
cv2.createTrackbar('frame', title_window, 0,int(tots)-1, getFrame)



label = None
frameTime = 50
start_frame = None
stop_frame = None
start_frame_freezed = None
key_pressed = False
df = pd.DataFrame(columns = ["Label1"], index = range(1, int(tots) + 1))

delete_mode = np.nan
df = pd.DataFrame(columns = ["Label1"], index = range(1, int(tots) + 1))

print("File exist:", os.path.exists(video_file))




while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        cv2.imshow(title_window, frame)
        current_frames = cap.get(cv2.CAP_PROP_POS_FRAMES)
        cv2.setTrackbarPos('frame',title_window, int(current_frames))
        if keyboard.is_pressed('a'):
            frame_changer(cap, "back", 1)
        if keyboard.is_pressed('d'):
             frame_changer(cap, "front", 1)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
        if keyboard.is_pressed('p'):
            cv2.waitKey(-1) #wait until any key is pressed
        if keyboard.is_pressed("r"):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            cv2.setTrackbarPos('frame',title_window, 0)
            cv2.waitKey(-1)
        if keyboard.is_pressed('w'):
           cv2.waitKey(frameTime)
        if keyboard.is_pressed('e'):
            end_key(df, "test")
        if keyboard.is_pressed('1'):
            step_mode(df, "test",cap)
        if keyboard.is_pressed('g'):
            delete_mode(df, np.nan)
        if keyboard.is_pressed('h'):
            ctrl_alt_delet(df)
        if keyboard.is_pressed('g'):
            test = cap.get(cv2.CAP_PROP_POS_FRAMES)
            df.iloc[int(test), 0] = delete_mode
            cv2.waitKey(-1)
    else: 

        break

# When everything done, release 
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
video_object = Application()
video_object.root.mainloop()