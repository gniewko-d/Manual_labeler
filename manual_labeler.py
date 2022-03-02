import keyboard
import datetime
import cv2
import pandas as pd
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class Application:
    def __init__(self):
        global video_file
        self.cap = cv2.VideoCapture(video_file)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.current_image = None
        self.root = tk.Tk()
        self.root.title("Mnimalistic Player")
        self.screen = tk.Label(self.root)
        self.screen.pack(padx=10, pady=10)
        self.video_stream()
    def video_stream(self):
        ret, frame = self.cap.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.screen.imgtk = imgtk
            self.screen.config(image=imgtk)
        self.root.after(30, self.video_stream)
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

video_file = filedialog.askopenfilename(title="Select An Video", filetypes= (("gif files", "*.gif"), ("flv files", "*.flv"), ("avi files", "*.avi"), ("amv files", "*.amv"), ("mp4 files", "*.mp4")))
video_file = r"C:\Users\gniew\OneDrive\Pulpit\python\moje\manual_marker\finek_v1.mp4"
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
    else:
        break

# When everything done, release 
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
video_object = Application()
video_object.root.mainloop()