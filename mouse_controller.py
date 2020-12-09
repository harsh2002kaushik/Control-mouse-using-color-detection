import numpy as np
import pyautogui
import cv2
import time

cap=cv2.VideoCapture(0)
cv2.namedWindow('label', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('label', cv2.WND_PROP_FULLSCREEN, 1)


while True:
    ret,frame=cap.read()
    frame=cv2.resize(frame,(1920,1080))
    
    if ret==True: 
        hsv_img = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        kernel = np.ones((3,3))
        
        # thresholds are the colors in the lower and upper range of hsv model which will be detected by masking 
        green_lower = np.array([45,50,70])
        green_upper = np.array([75,255,255])

        yellow_lower = np.array([0,50,100])
        yellow_upper = np.array([5,255,255])
             
        blue_lower = np.array([25,50,50])
        blue_upper = np.array([32,255,255])

        # using green color for movement of the cursor
        motion_lower = green_lower
        motion_upper = green_upper
        curr_mask_motion=cv2.inRange(hsv_img, motion_lower, motion_upper)
        mask_motion = cv2.dilate(curr_mask_motion,kernel,iterations = 2)
        
        # using yellow color for clicking the cursor
        click_lower = yellow_lower
        click_upper = yellow_upper
        curr_mask_click = cv2.inRange(hsv_img,click_lower,click_upper)
        mask_click = cv2.dilate(curr_mask_click,kernel,iterations = 2)
        
        cv2.line(frame,(int(frame.shape[1]/2),0),(int(frame.shape[1]/2),frame.shape[0]),(255,0,0),4)  # drawing a line at the centre of the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,'Left Click',(int(frame.shape[1]/4),int(frame.shape[0]/10)), font,0.5, (0,0,255), 2, cv2.LINE_AA)
        cv2.putText(frame,'Right Click',(int(frame.shape[1]*3/4),int(frame.shape[0]/10)), font,0.5, (0,0,255), 2, cv2.LINE_AA)
        
        try:  
            cnt_motion = 0
            contours_motion,hierarchy = cv2.findContours(mask_motion,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cnt_motion = max(contours_motion, key = lambda x: cv2.contourArea(x))
            
            if cv2.contourArea(cnt_motion) >= 200.0 :    # 200 is min area of colored object assigned for clicking,it is to insure some small colored objects are not considered
                M_motion = cv2.moments(cnt_motion)
                cx_motion = int(M_motion['m10']/M_motion['m00'])
                cy_motion = int(M_motion['m01']/M_motion['m00'])
                point_motion = np.array([[cx_motion,cy_motion]],dtype=np.int32)
                pyautogui.moveTo(cx_motion, cy_motion )#, duration= 0.5)
                
            else:  
                pass
            
            try:
                cnt_click = 0
                contours_click,hierarchy = cv2.findContours(mask_click,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)               
                cnt_click = max(contours_click, key = lambda x: cv2.contourArea(x))
                
                if cv2.contourArea(cnt_click) >= 1000.0:         # 1000 is min area of colored object assigned for clicking 
                    M_click = cv2.moments(cnt_click)
                    cx_click = int(M_click['m10']/M_click['m00'])
                    cy_click = int(M_click['m01']/M_click['m00'])
                    point_click = np.array([[cx_click,cy_click]],dtype=np.int32)
                    time.sleep(1)
                    
                    if cx_click >= int(frame.shape[1]/2) :
                        pyautogui.leftClick(x=pyautogui.position().x, y=pyautogui.position().y) 
                    else:
                        pyautogui.rightClick(x=pyautogui.position().x, y=pyautogui.position().y)
            
    
            except:
                pass
            
            cv2.imshow('label',frame)
            cv2.imshow('mask_motion',mask_motion)
            cv2.imshow('mask_click',mask_click)
     
        except:
            
            try:
                cnt_click = 0
                contours_click,hierarchy = cv2.findContours(mask_click,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                cnt_click = max(contours_click, key = lambda x: cv2.contourArea(x))
                
                if cv2.contourArea(cnt_click) >= 1000.0:
                    M_click = cv2.moments(cnt_click)
                    cx_click = int(M_click['m10']/M_click['m00'])
                    cy_click = int(M_click['m01']/M_click['m00'])
                    point_click = np.array([[cx_click,cy_click]],dtype=np.int32)
                    time.sleep(1)
                    
                    if cx_click >= int(frame.shape[1]/2) :
                        pyautogui.leftClick(x=pyautogui.position().x, y=pyautogui.position().y)
                    else:
                        pyautogui.rightClick(x=pyautogui.position().x, y=pyautogui.position().y)
                
            except:
                    pass

            cv2.imshow('label',frame)
            cv2.imshow('mask_motion',mask_motion)
            cv2.imshow('mask_click',mask_click)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break 

cv2.destroyAllWindows()
