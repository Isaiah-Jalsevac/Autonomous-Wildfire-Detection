import cv2
import numpy as np
from datetime import datetime

# TC001 settings
CAMERA_INDEX = 0
FRAME_WIDTH = 256
FRAME_HEIGHT = 192

# Detection settings - adjust these based on testing
HOTSPOT_THRESHOLD = 200  # pixel intensity value (0-255)
MIN_HOTSPOT_AREA = 10    # minimum pixel area to count as hotspot

def initialize_camera():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    return cap

def detect_hotspots(frame):
    # Convert to grayscale for thresholding
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Threshold - pixels above value are potential hotspots
    _, thresh = cv2.threshold(gray, HOTSPOT_THRESHOLD, 255, cv2.THRESH_BINARY)
    
    # Find contours of hotspot regions
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    hotspots = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= MIN_HOTSPOT_AREA:
            x, y, w, h = cv2.boundingRect(contour)
            hotspots.append({
                'x': x,
                'y': y,
                'width': w,
                'height': h,
                'area': area,
                'timestamp': datetime.now().isoformat()
            })
    
    return hotspots, thresh

def draw_hotspots(frame, hotspots):
    output = frame.copy()
    for spot in hotspots:
        # Draw rectangle around each hotspot
        cv2.rectangle(output,
                      (spot['x'], spot['y']),
                      (spot['x'] + spot['width'], spot['y'] + spot['height']),
                      (0, 0, 255), 2)
        # Label it
        cv2.putText(output, 'HOTSPOT',
                    (spot['x'], spot['y'] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
    return output

def log_hotspot(hotspot):
    with open('hotspot_log.txt', 'a') as f:
        f.write(f"{hotspot['timestamp']} - Position: ({hotspot['x']}, {hotspot['y']}) Area: {hotspot['area']:.1f}px\n")

def main():
    print("Initializing camera...")
    cap = initialize_camera()
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("Camera initialized. Starting detection...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            hotspots, thresh = detect_hotspots(frame)
            
            if hotspots:
                print(f"{datetime.now().isoformat()} - {len(hotspots)} hotspot(s) detected")
                for spot in hotspots:
                    log_hotspot(spot)
            
    except KeyboardInterrupt:
        print("\nStopping detection")
    finally:
        cap.release()
        print("Camera released")

if __name__ == '__main__':
    main()
