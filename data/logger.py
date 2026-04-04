# logger.py

import numpy as np
import cv2
import os
import csv
import datetime

def init_log():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = os.path.join('log', timestamp)
    mean_image_dir = os.path.join(run_dir, 'mean_images')
    const_image_dir = os.path.join(run_dir, 'const_images')
    
    os.makedirs(run_dir, exist_ok=True)
    os.makedirs(mean_image_dir, exist_ok=True)
    os.makedirs(const_image_dir, exist_ok=True)
    
    const_path = os.path.join(run_dir, 'const_detections.csv')
    mean_path = os.path.join(run_dir, 'mean_detections.csv')
    
    header = ['timestamp', 'log_type', 'latitude', 'longitude', 'altitude_m', 'max_temp_c', 'hotspot_count', 'hotspot_size']
    
    for path in [const_path, mean_path]:
        with open(path, 'w', newline='') as f:
            csv.writer(f).writerow(header)
    
    return const_path, mean_path, mean_image_dir, const_image_dir

def log_detection(filepath, log_type, lat, lon, alt, max_temp, hotspot_count, hotspot_size):
    with open(filepath, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now(), log_type, lat, lon, alt, max_temp, hotspot_count, hotspot_size])

def log_heartbeat(filepath, log_type, lat, lon, alt):
    with open(filepath, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now(), log_type, lat, lon, alt, '', '', ''])

def log_image(image_dir, frame, display):
    os.makedirs(image_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    
    # Save raw temperature data for ML
    np.save(os.path.join(image_dir, f"detection_{timestamp}.npy"), frame)
    
    # Save colourmap image for display
    cv2.imwrite(os.path.join(image_dir, f"detection_{timestamp}.png"), display)
