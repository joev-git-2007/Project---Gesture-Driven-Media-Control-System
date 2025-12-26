import pyautogui #controls keyboard and mouse
import time #for smooth functioning, without being clashed.
from cvzone.HandTrackingModule import HandDetector #cvzone combines opencv & mediapipe
import cv2 #opencv - for accessing webcam, displaying frames, texts on frames, etc.

cap = cv2.VideoCapture(0) #opens webcam [ (0) means local cam ] using the function VideoCapture

detector = HandDetector(detectionCon=0.9, maxHands=2) #stores the detection concentration (90%) and number of max hands (2)

last_action_time = 0 #stores when the last key was pressed
cooldown = 1 #gives min 1 sec gap between actions.

while True: #an infinity loop untill esc is pressed.
    success, img = cap.read() #cap.read returns 2 values. Bool value in success and the running frame in img. Success tells whether access to cam is success or failed.
    hands, img = detector.findHands(img) #findHands captures the current snapshot of the frame (img) and add texts, details, etc on the frame and stores that snapshot in img. hands is list of dictionaries where all the details of captured snapshot is stored.

    y_positions = {"Right": 70, "Left": 170} #to locate the position of hands. 70 and 170 are coordinate points.

    if hands: #only true when atleast one hand is detected
        for hand in hands: 
            handType = hand['type'] #stores whether left or right
            fingers = detector.fingersUp(hand) #returns list of fingers along with their position (up/down) - eg: [0,0,0,0,0]
            
            cv2.putText(img, f"{handType} Hand Fingers: {fingers}", (10, y_positions[handType]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            #Details of what all to be shown on the frame - Right/Left Hand fingers: [,,,,], position, font, thickness, colour, size
            gesture = "None"  #displays the current gesture as None

            if time.time() - last_action_time > cooldown: #current time - last action time > 1: then only allow the new gesture action

                if fingers == [0,0,0,0,0]: #fist
                    gesture = "Play/Pause" #gesture to be displayed 
                    pyautogui.press("space") #clicks spacebar
                    last_action_time = time.time() #stores time when pressed to last_action_time

                elif fingers == [1,1,1,1,1]: #palm
                    gesture = "Volume Up"
                    pyautogui.press("volumeup")
                    last_action_time = time.time()

                elif fingers == [0,1,1,0,0]: #peace (2)
                    gesture = "Volume Down"
                    pyautogui.press("volumedown")
                    last_action_time = time.time()

                elif fingers == [0,1,0,0,0]: #index (1)
                    gesture = "Next Track"
                    pyautogui.press("nexttrack")
                    last_action_time = time.time()

                    cv2.putText(img, f"{gesture}", (10, y_positions[handType] + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 255), 3) #details

    cv2.imshow("Hand Gesture (Left + Right)", img) #Shows the live video window and the complete final frame

    if cv2.waitKey(1) & 0xFF == 27: #waits for 1 ms after the ESC (27-ASCII code) key is pressed
        break

cap.release() #releases webcam
cv2.destroyAllWindows() #closes all internal and external opencv windows
  
