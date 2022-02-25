import keyboard 
import datetime
import cv2
import pandas as pd 
frame_counter = 0
#video_file = r"C:\Users\malgo\Desktop\python\video_labeling\finek.mp4"
video_file = r"C:\Users\gniew\OneDrive\Pulpit\python\moje\manual_marker\finek_v1.mp4"
title_window = "Mnimalistic Player"
cv2.namedWindow(title_window)
cv2.moveWindow(title_window,750,150)
def flick(x):
    pass

def getFrame(frame_nr):
    global cap
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_nr)

cap = cv2.VideoCapture(video_file)
tots = cap.get(cv2.CAP_PROP_FRAME_COUNT)
cv2.createTrackbar('frame', title_window, 0,int(tots)-1, getFrame)


fps = int(cap.get(cv2.CAP_PROP_FPS))
label = None
frameTime = 50
start_frame = None
df = pd.DataFrame(columns = ["Label1"], index = range(1, int(tots) + 1))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        cv2.imshow(title_window, frame)
        current_frames = cap.get(cv2.CAP_PROP_POS_FRAMES)
        cv2.setTrackbarPos('frame',title_window, int(current_frames))
        if keyboard.is_pressed('a'):
            next_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            current_frame = next_frame - 1
            previous_frame = current_frame - 1
            cap.set(cv2.CAP_PROP_POS_FRAMES, previous_frame)
            cv2.setTrackbarPos('frame',title_window, int(previous_frame))
            cv2.waitKey(-1) #wait until any key is pressed
        if keyboard.is_pressed('d'):
             next_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
             current_frame = next_frame - 1
             next_frame = current_frame + 1
             cap.set(cv2.CAP_PROP_POS_FRAMES, next_frame)
             cv2.setTrackbarPos('frame',title_window, int(next_frame))
             cv2.waitKey(-1) #wait until any key is pressed
        if cv2.waitKey(25) & 0xFF == ord('q'):
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
            global stop_frame
            stop_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            df.iloc[start_frame-1:stop_frame-1, 0] = label
            cv2.waitKey(-1)
        if keyboard.is_pressed('1'):
            start_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            label = "Test"
            
    else: 
        break

# When everything done, release 
# the video capture object
cap.release()
   
# Closes all the frames
cv2.destroyAllWindows()