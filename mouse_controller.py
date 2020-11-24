import numpy as np
import pyautogui
import cv2
import time

cap=cv2.VideoCapture(0)
cv2.namedWindow('label', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('label', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


while True:
    ret,frame=cap.read()
    
    if ret==True: 
        hsv_img = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        kernel = np.ones((3,3))
        
        # thresholds are the colors in the lower and upper range of hsv model which will be detected by masking 
        green_lower = np.array([45,50,70])
        green_upper = np.array([75,255,255])     
        curr_mask_green = cv2.inRange(hsv_img, green_lower, green_upper)
        mask_green = cv2.dilate(curr_mask_green,kernel,iterations = 2)
        
        # 2 masks are used to avoid detection of skin as red color
        red_lower = np.array([0,120,70])
        red_upper = np.array([10,255,255])
        curr_mask_red_1 = cv2.inRange(hsv_img, red_lower, red_upper)
        mask_red_1 = cv2.dilate(curr_mask_red_1,kernel,iterations = 2)
        red_lower = np.array([170,120,70])
        red_upper = np.array([180,255,255])
        curr_mask_red_2 = cv2.inRange(hsv_img,red_lower,red_upper)
        mask_red_2 = cv2.dilate(curr_mask_red_2,kernel,iterations = 2)
        mask_red = mask_red_1+mask_red_2
    
        cv2.line(frame,(320,0),(320,640),(255,0,0),4)  # drawing a line at the centre of the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,'Left Click',(160,60), font,0.5, (0,0,255), 2, cv2.LINE_AA)
        cv2.putText(frame,'Right Click',(480,60), font,0.5, (0,0,255), 2, cv2.LINE_AA)
        
        try:  
            cnt_green = 0
            contours_green,hierarchy = cv2.findContours(mask_green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cnt_green = max(contours_green, key = lambda x: cv2.contourArea(x))
            
            if cv2.contourArea(cnt_green) >= 200.0 : 
                M_green = cv2.moments(cnt_green)
                cx_green = int(M_green['m10']/M_green['m00'])
                cy_green = int(M_green['m01']/M_green['m00'])
                point_green=np.array([[cx_green,cy_green]],dtype=np.int32)
                pyautogui.moveTo(cx_green*4, cy_green*2.5 )#, duration= 0.5)   
            else:  
                pass
            
            try:
                cnt_red = 0
                contours_red,hierarchy= cv2.findContours(mask_red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)               
                cnt_red = max(contours_red, key = lambda x: cv2.contourArea(x))
                
                if cv2.contourArea(cnt_red) >= 600.0:
                    M_red = cv2.moments(cnt_red)
                    cx_red = int(M_red['m10']/M_red['m00'])
                    cy_red = int(M_red['m01']/M_red['m00'])
                    point_red = np.array([[cx_red,cy_red]],dtype=np.int32)
                    time.sleep(1)
                    
                    if cx_red >= 320 :
                        pyautogui.leftClick(x=pyautogui.position().x, y=pyautogui.position().y) 
                    else:
                        pyautogui.rightClick(x=pyautogui.position().x, y=pyautogui.position().y)
                
            except:
                pass
            
            cv2.imshow('label',frame)
            cv2.imshow('mask_green',mask_green)
            cv2.imshow('mask_red',mask_red)
     
        except:
            
            try:
                cnt_red = 0
                contours_red,hierarchy = cv2.findContours(mask_red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                cnt_red = max(contours_red, key = lambda x: cv2.contourArea(x))
                if cv2.contourArea(cnt_red) >= 1000.0:
                    M_red = cv2.moments(cnt_red)
                    cx_red = int(M_red['m10']/M_red['m00'])
                    cy_red = int(M_red['m01']/M_red['m00'])
                    point_red = np.array([[cx_red,cy_red]],dtype=np.int32)
                    time.sleep(1)
                    
                    if cx_red >= 320 :
                        pyautogui.leftClick(x=pyautogui.position().x, y=pyautogui.position().y)
                    else:
                        pyautogui.rightClick(x=pyautogui.position().x, y=pyautogui.position().y)
                
            except:
                    pass

            cv2.imshow('label',frame)
            cv2.imshow('mask_green',mask_green)
            cv2.imshow('mask_red',mask_red)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break 

cv2.destroyAllWindows()
