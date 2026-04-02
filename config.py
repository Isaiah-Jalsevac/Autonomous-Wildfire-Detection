# config.py

# camera
FRAME_WIDTH = 256
FRAME_HEIGHT = 192
THERMAL_DEVICE = 4

# detection
DETECTION_TYPE = 0 # 0 is relitive to constant, 1 is relitive to mean
DETECTION_THRESHOLD_CONST = 60
MIN_HOTSPOT_AREA = 5
DETECTION_THRESHOLD_OVER_MEAN = 50


# data
LOG_PATH = 'data/logs/flight_log.csv'
IMAGE_SAVE_DIR = 'data/images/'
IMAGE_SAVE_COOLDOWN = 1.0



#UAV
MAVLINK_PORT = 0
MAVLINK_BAUD = 57600  # standard ArduPilot telemetry baud rate

# main
HEARTBEAT_FREQUENCY = 10 # time in seconds between heartbeat logs
