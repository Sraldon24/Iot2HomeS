import time, threading, logging, signal, sys, os
from datetime import datetime
from modules.mqtt_client import MqttClient
from modules.security_system import SecuritySystem
from modules.environment_monitor import EnvironmentMonitor
from modules.local_db import init_db, save_env, save_motion  # ✅ added for local DB

# LOGGING SETUP (new for per-run logs)
os.makedirs("logs", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = f"logs/run_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, mode='w'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("domisafeapp2")

RUNNING = True

def stop_all(signum=None, frame=None):
    global RUNNING
    log.info("🛑 Received stop signal, shutting down cleanly...")
    RUNNING = False
    time.sleep(1)
    sys.exit(0)

signal.signal(signal.SIGINT, stop_all)
signal.signal(signal.SIGTERM, stop_all)

def main():
    mqtt = MqttClient()
    sec = SecuritySystem()
    env = EnvironmentMonitor()

    init_db()  # ✅ initialize database

    time.sleep(1.5)

    def send_env():
        while RUNNING:
            try:
                data = env.read()
                mqtt.publish("temperature", data["temperature"])
                mqtt.publish("humidity", data["humidity"])
                save_env(data["temperature"], data["humidity"])  # ✅ save locally
            except Exception as e:
                log.error(f"Env loop error: {e}")
            time.sleep(30)

    def send_security():
        while RUNNING:
            try:
                s = sec.check()

                mqtt.publish("motion", int(s["motion"]))
                mqtt.publish("led_status", s["led_status"])

                # Publish buzzer ON→OFF event
                if s.get("buzzer_pulsed"):
                    mqtt.publish("buzzer_status", 1)
                    time.sleep(0.2)
                    mqtt.publish("buzzer_status", 0)
                else:
                    mqtt.publish("buzzer_status", s["buzzer_status"])

                # Publish motor ON→OFF event
                if s.get("motor_pulsed"):
                    mqtt.publish("motor_status", 1)
                    time.sleep(0.2)
                    mqtt.publish("motor_status", 0)

                if s["image_b64"]:
                    mqtt.publish("camera_last_image", s["image_b64"])

                # ✅ save motion event if detected
                if s["motion"]:
                    save_motion(1)

            except Exception as e:
                log.error(f"Security loop error: {e}")
            time.sleep(5)

    threading.Thread(target=send_env, daemon=True).start()
    send_security()

if __name__ == "__main__":
    main()
    #AUTO-UPLOAD LOGS TO GOOGLE DRIVE (after run ends) 
    try:
        os.system("python3 upload_logs.py")
    except Exception as e:
        log.error(f"Failed to upload logs: {e}")
