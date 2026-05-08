# config.py

# camera
FRAME_WIDTH = 256
FRAME_HEIGHT = 192
THERMAL_DEVICE = 4

# detection
DETECTION_TYPE = 2 # 0 is mean, 1 is constant, 2 is both
DETECTION_THRESHOLD_CONST = 60
MIN_HOTSPOT_AREA = 5
DETECTION_THRESHOLD_OVER_MEAN = 10

# data
LOG_PATH = 'data/logs'
IMAGE_SAVE_COOLDOWN = 1.0

# UAV
MAVLINK_PORT = '/dev/ttyS0'
MAVLINK_BAUD = 57600
MAVLINK_SYSTEM_ID = 1
MAVLINK_COMPONENT_ID = 191
MAVLINK_GPS_RATE_HZ = 2

# main
SHOW_FEED = True # if true then shows feed of thermal camera
HEARTBEAT_FREQUENCY = 10 # time in seconds between heartbeat logs
GCS_ALERT_FREQUENCY = 120 # minimum time in seconds between detection allerts sent to ground station

