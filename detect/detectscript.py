import cv2
import numpy as np
import requests
from datetime import datetime, timedelta

backend_url = "http://localhost:3000/logs" 
cooldown_seconds = 60  

last_logged = {
    "apple": datetime.min,
    "banana": datetime.min,
    "cucumber": datetime.min
}


cap = cv2.VideoCapture(1) 

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    kernel = np.ones((5, 5), np.uint8)


    lower_red1 = np.array([0, 150, 170])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 150, 170])
    upper_red2 = np.array([180, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)


    lower_banana = np.array([15, 100, 100])
    upper_banana = np.array([35, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_banana, upper_banana)
    mask_yellow = cv2.erode(mask_yellow, kernel, iterations=2)
    mask_yellow = cv2.dilate(mask_yellow, kernel, iterations=2)


    lower_cucumber = np.array([35, 40, 40])
    upper_cucumber = np.array([85, 255, 180])
    mask_green = cv2.inRange(hsv, lower_cucumber, upper_cucumber)


    mask_red = cv2.erode(mask_red, kernel, iterations=2)
    mask_red = cv2.dilate(mask_red, kernel, iterations=2)


    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



    def handle_detection(fruit_name, contours, min_area, color_bgr, y_offset):
        global last_logged
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_area:
                cv2.drawContours(frame, [contour], -1, color_bgr, 3)
                cv2.putText(frame, f"{fruit_name} detected", (50, 50 + y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color_bgr, 2)

                
                now = datetime.now()
                if now - last_logged[fruit_name] >= timedelta(seconds=cooldown_seconds):
                    last_logged[fruit_name] = now
                    
                    try:
                        requests.post(
                            backend_url,
                            json={
                                "fruit": fruit_name,
                                "area": float(area),
                                "timestamp": now.isoformat()
                            },
                            timeout=1  
                        )
                    except Exception as e:
                        print(f"[Error] Sending {fruit_name} to backend:", e)

    handle_detection("apple", contours_red, 1000, (0, 0, 255), 0)
    handle_detection("banana", contours_yellow, 2000, (0, 255, 255), 50)
    handle_detection("cucumber", contours_green, 2000, (0, 255, 0), 100)

    
    cv2.imshow("Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('0'):
        break


cap.release()
cv2.destroyAllWindows()
