# main.py

import cv2
from camera.read_camera import ThermalCamera
from detection.hotspot import detect_hotspot_const, detect_hotspot_mean
from data.logger import init_log, log_detection, log_heartbeat, log_image
import config
import time

def main():

    # makes sure that if an error is incountered the program exits cleanly
    try:
        camera = ThermalCamera()
    except RuntimeError as e:
        print(f"failed to initialize camera: {e}")
        exit(1)

    init_log(config.LOG_PATH) # initializes logging and logging path

    last_heartbeat = time.time() # start heartbeat timer

    running = True # loop only runs if running is True

    last_frame_save = 0

    # main loop
    while running:

        current_time = time.time()

        frame, temp_map, display = camera.get_frame() # grabs frame from camera
    
        if temp_map is None: # checks for NUC and frame read erors
            #print('NUC event happened or error occured. If persists check connection.')
            continue
    
        if config.DETECTION_TYPE == 1: # Checks which detection method is being used
            contours = detect_hotspot_mean(temp_map)
        else:
            contours = detect_hotspot_const(temp_map)
    
        if contours:# if detection occured, log it
            #print(f"Hotspot over {config.DETECTION_THRESHOLD_CONST} degrees celsius detected")
            #print(f"Max temp: {temp_map.max():.1f}°C, Mean: {temp_map.mean():.1f}°C")
            max_temp = temp_map.max()
            total_area = sum(cv2.contourArea(c) for c in contours)
            log_detection(config.LOG_PATH, 'Detection', 0, 0, 0, max_temp, len(contours), total_area) # TODO: add drone position info

            if current_time - last_frame_save > config.IMAGE_SAVE_COOLDOWN:
                log_image(config.IMAGE_SAVE_DIR, frame, display)
                last_frame_save = time.time()

        if time.time() > last_heartbeat + config.HEARTBEAT_FREQUENCY:
            #print('Heartbeat log saved')
            log_heartbeat(config.LOG_PATH, 'Heartbeat', 0, 0, 0) # TODO: add drone position info
            last_heartbeat = time.time()

        cv2.imshow('Thermal', display)  # uncomment to display thermal feed
        if cv2.waitKey(1) == ord('q'):  # uncomment to enable q to quit
            running = False

    camera.release()
    cv2.destroyAllWindows()

# only calls main() if the file is directly run by python, not if it is imported from something
if __name__ == '__main__':
    main()

