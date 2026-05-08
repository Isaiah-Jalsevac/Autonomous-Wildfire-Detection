# mavlink.py

import threading
import time
from pymavlink import mavutil
import config

class Mavlink:
    def __init__(self):
        self._lat = 0.0
        self._lon = 0.0
        self._alt = 0.0
        self._fix = False
        self._lock = threading.Lock()
        self._running = False
        
        try:
            self._conn = mavutil.mavlink_connection(
                config.MAVLINK_PORT,
                baud=config.MAVLINK_BAUD,
                source_system=config.MAVLINK_SYSTEM_ID,
                source_component=config.MAVLINK_COMPONENT_ID
            )
        
            print("Waiting for FC heartbeat...")
            self._conn.wait_heartbeat(timeout=10)
            print(f"Heartbeat recieved system id ({self._conn.target_system}, component {self._conn.target_component})")

            self._request_gps_stream()
            self._running = True
            self._thread = threading.Thread(target=self._listen_loop, daemon=True)
            self._thread.start()

        except Exception as e:
            print(f"Warning: could not connect to FC {e}")
            print("Position will defualt to 0, 0, 0")


    def _request_gps_stream(self):
        self._conn.mav.set_message_interval_send(
            self._conn.target_system,
            self._conn.target_component,
            mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT,
            1_000_000 // config.MAVLINK_GPS_RATE_HZ,
            0
        )

    def _listen_loop(self):
        while self._running:
            try:
                msg = self._conn.recv_match(
                    type='GLOBAL_POSITION_INT',
                    blocking=True,
                    timeout=1.0
                )
                if msg:
                    with self._lock:
                        self._lat = msg.lat / 1e7
                        self._lon = msg.lon / 1e7
                        self._alt = msg.relative_alt / 1000.0
                        self._fix = True

            except Exception as e:
                print(f"FC listening error {e}")
                time.sleep(0.5)

    @property
    def position(self):
        with self._lock:
            return self._lat, self._lon, self._alt

    @property
    def has_fix(self):
        with self._lock:
            return self._fix

    def send_detection_alert(self, lat, lon, alt, size):
        text = f"FIRE lat:{lat:.4f} lon:{lon:.4f} sz:{size:.0f}"
        self._conn.mav.statustext_send(
            mavutil.mavlink.MAV_SEVERITY_WARNING,
            text.encode()[:50]
        )

    def loiter_at(self, lat, lon, alt):
        raise NotImplementedError("Heartbeat sender required before sending commands")

    def resume_mission(self):
        raise NotImplementedError("Heartbeat sender required before sending commands")

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
        if self._conn:
            self._conn.close()
 




        
        
