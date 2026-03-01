import cv2
import numpy as np
import config

# Takes THERMAL_DEVICE, grabs frame, and outputs visual frame and a temp map in celsius
class ThermalCamera:
    def __init__(self):
        self.cap = cv2.VideoCapture(config.THERMAL_DEVICE)
        self.cap.set(cv2.CAP_PROP_CONVERT_RGB, 0) # Raw data, not processed RGB

        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open thermal camera on device {config.THERMAL_DEVICE}")
                               
        print(f"Thermal camera opened on /dev/video{config.THERMAL_DEVICE}")

    def get_frame(self):
        ret, frame = self.cap.read()

        if not ret or frame is None:
            return None, None # Used for periodic NUC dropout. Also handels read errors.
        
        # Split frame into visual and thermal halves
        visual = frame[:config.FRAME_HEIGHT, :]
        raw_thermal = frame[config.FRAME_HEIGHT:, :]

        # Decode raw 16-bit temperature data
        raw_16 = raw_thermal[:, :, 1].astype(np.uint16) * 256 + raw_thermal[:, :, 0].astype(np.uint16)
        celsius_temp_map = (raw_16 / 64.0) - 273.15 # Outputs a temperatue map with shape[FRAME_HEIGHT, FRAME_WIDTH]
                                                    # This points to the temperature in celsius
        
        return visual, celsius_temp_map

    # Cleanly relase camera
    def release(self):
        self.cap.release()
