# main.py

import cv2
from UAV.mavlink import Mavlink
from camera.read_camera import ThermalCamera
from detection.hotspot import detect_hotspot_const, detect_hotspot_mean
from data.logger import init_log, log_detection, log_heartbeat, log_image
import config
import time

def main():

    # setup camera connection
    try:
        camera = ThermalCamera()
    except RuntimeError as e:
        print(f"failed to initialize camera: {e}")
        exit(1)

    # setup mavlink connection
    mavlink = Mavlink()

    # capture latitude, longitude, and altutude from the FC

    # initializes logging and logging path
    const_path, mean_path, mean_image_dir, const_image_dir = init_log(config.LOG_PATH)

    if config.SHOW_FEED:
        cv2.namedWindow('Thermal', cv2.WINDOW_NORMAL)

    last_heartbeat = time.time() # start heartbeat timer

    running = True # loop only runs if running is True

    last_frame_save_mean = 0
    last_frame_save_const = 0 

    max_temp = 0

    # main loop
    while running:

        current_time = time.time()

        # capture positon from gps data loop
        lat, lon, alt = mavlink.position

        frame, temp_map, display = camera.get_frame() # grabs frame from camera
    
        if temp_map is None: # checks for NUC and frame read erors
            #print('NUC event happened or error occured. If persists check connection.')
            continue

        contours_const = []
        contours_mean = []
    
        if config.DETECTION_TYPE == 0: # Checks which detection method is being used
            contours_mean = detect_hotspot_mean(temp_map)
        if config.DETECTION_TYPE == 1:
            contours_const = detect_hotspot_const(temp_map)
        if config.DETECTION_TYPE == 2:
            contours_mean = detect_hotspot_mean(temp_map)
            contours_const = detect_hotspot_const(temp_map)

        if contours_mean:# if detection occured, log it
            #print(f"Hotspot over {config.DETECTION_THRESHOLD_OVER_MEAN} degrees celsius above mean detected")
            #print(f"Max temp: {temp_map.max():.1f}°C, Mean: {temp_map.mean():.1f}°C")
            max_temp = temp_map.max()
            total_area = sum(cv2.contourArea(c) for c in contours_mean)
            log_detection(mean_path, 'Detection', lat, lon, alt, max_temp, len(contours_mean), total_area)

            if current_time - last_frame_save_mean > config.IMAGE_SAVE_COOLDOWN:
                log_image(mean_image_dir, frame, display)
                last_frame_save_mean = time.time()

        if contours_const:# if detection occured, log it
            #print(f"Hotspot over {config.DETECTION_THRESHOLD_CONST} degrees celsius detected")
            #print(f"Max temp: {temp_map.max():.1f}°C, Mean: {temp_map.mean():.1f}°C")
            max_temp = temp_map.max()
            total_area = sum(cv2.contourArea(c) for c in contours_const)
            log_detection(const_path, 'Detection', lat, lon, alt, max_temp, len(contours_const), total_area)

            if current_time - last_frame_save_const > config.IMAGE_SAVE_COOLDOWN:
                log_image(const_image_dir, frame, display)
                last_frame_save_const = time.time()




        if time.time() > last_heartbeat + config.HEARTBEAT_FREQUENCY:
            #print('Heartbeat log saved')
            log_heartbeat(mean_path, 'Heartbeat', lat, lon, alt)
            log_heartbeat(const_path, 'Heartbeat', lat, lon, alt) 
            last_heartbeat = time.time()

        if config.SHOW_FEED == True:
            for c in contours_mean + contours_const:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(display, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(display, f"{max_temp:.1f}C", (x, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            cv2.imshow('Thermal', display)
            if cv2.waitKey(1) == ord('q'):
                running = False
        
    mavlink.stop()

    camera.release()
    cv2.destroyAllWindows()


# only calls main() if the file is directly run by python, not if it is imported from something
if __name__ == '__main__':
    main()

