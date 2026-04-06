Autonomous Wildfire Detection with Thermal Camera

A systemd service file to initialize on boot: 

[Unit]
Description=Wildfire Detection
After=multi-user.target

[Service]
Type=simple
User=isaiah
WorkingDirectory=/home/isaiah/Autonomous-Wildfire-Detection
ExecStart=/home/isaiah/tc001-env/bin/python main.py
Environment=PYTHONUNBUFFERED=1
Environment=QT_QPA_PLATFORM=offscreen
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target


Command to run: 
cd ~/Projects/2026-science-fair/Wildfire_Detection
source ~/tc001-env/bin/activate
python main.py

