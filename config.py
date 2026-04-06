# config.py

# camera
FRAME_WIDTH = 256
FRAME_HEIGHT = 192
THERMAL_DEVICE = 4

# detection
DETECTION_TYPE = 2 # 0 is mean, 1 is constant, 2 is both
DETECTION_THRESHOLD_CONST = 60
MIN_HOTSPOT_AREA = 5
DETECTION_THRESHOLD_OVER_MEAN = 35


# data
LOG_PATH = 'data/logs'
IMAGE_SAVE_COOLDOWN = 1.0



#UAV
MAVLINK_PORT = 0
MAVLINK_BAUD = 57600  # standard ArduPilot telemetry baud rate

# main
SHOW_FEED = True # if true then shows feed of thermal camera
HEARTBEAT_FREQUENCY = 10 # time in seconds between heartbeat logs

