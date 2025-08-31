import cv2
import numpy as np
import requests
from datetime import datetime, timedelta

cap = cv2.VideoCapture(1)  # 1 macbook, 0 phone

# Keep track of last log time for each fruit
last_logged = {
    "apple": datetime.min,
    "banana": datetime.min,
    "cucumber": datetime.min
}
cooldown = timedelta(minutes=1)  # 1 minute cooldown

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    # Red for apple
    lower_red1 = np.array([0, 150, 170])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 150, 170])
    upper_red2 = np.array([180, 255, 255])

    # Banana
    lower_banana = np.array([15, 100, 100])
    upper_banana = np.array([35, 255, 255])

    # Cucumber
    lower_cucumber = np.array([35, 40, 40])
    upper_cucumber = np.array([85, 255, 180])

    kernel = np.ones((5, 5), np.uint8)

    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    mask_red = cv2.erode(mask_red, kernel, iterations=2)
    mask_red = cv2.dilate(mask_red, kernel, iterations=2)

    mask_yellow = cv2.inRange(hsv, lower_banana, upper_banana)
    mask_yellow = cv2.erode(mask_yellow, kernel, iterations=2)
    mask_yellow = cv2.dilate(mask_yellow, kernel, iterations=2)

    mask_green = cv2.inRange(hsv, lower_cucumber, upper_cucumber)

    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def log_detection(fruit_name, area):
        now = datetime.now()
        if now - last_logged[fruit_name] > cooldown:
            payload = {
                "fruit": fruit_name,
                "area": area,
                "timestamp": now.isoformat()
            }
            try:
                response = requests.post("http://localhost:3000/log-detection", json=payload)
                if response.status_code == 200:
                    print(f"Logged to DB: {response.json()}")
                    last_logged[fruit_name] = now
                else:
                    print("Failed to log:", response.text)
            except Exception as e:
                print("Error posting to backend:", e)

    # Apple detection
    for contour in contours_red:
        area = cv2.contourArea(contour)
        if area > 1000:
            cv2.drawContours(frame, [contour], -1, (0, 0, 255), 3)
            cv2.putText(frame, "apple detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            log_detection("apple", area)

    # Banana detection
    for contour in contours_yellow:
        area = cv2.contourArea(contour)
        if area > 2000:
            cv2.drawContours(frame, [contour], -1, (0, 255, 255), 3)
            cv2.putText(frame, "banana detected", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            log_detection("banana", area)

    # Cucumber detection
    for contour in contours_green:
        area = cv2.contourArea(contour)
        if area > 2000:
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)
            cv2.putText(frame, "cucumber detected", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            log_detection("cucumber", area)

    cv2.imshow("Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('0'):
        break

cap.release()
cv2.destroyAllWindows()
