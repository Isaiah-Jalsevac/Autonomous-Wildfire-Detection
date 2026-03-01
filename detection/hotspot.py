import cv2
import numpy as np
import config
from camera.read_camera import ThermalCamera

# Takes celsius temperature map and returns contours of pixels over threshold
def detect_hotspot_const(temp_map):
    # creates bool map of temperatures over threshold
    bool_map = temp_map > config.DETECTION_THRESHOLD
    binary_mask = bool_map.astype(np.uint8) * 255 # Convert to a binary array so it can be read by cv2
    # Find contours over MIN_HOTSPOT_AREA
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    valid_contours = [c for c in contours if cv2.contourArea(c) > config.MIN_HOTSPOT_AREA]

