import time, threading, logging, signal, sys
from modules.mqtt_client import MqttClient
from modules.security_system import SecuritySystem
from modules.environment_monitor import EnvironmentMonitor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
log = logging.getLogger("domisafeapp2")

# Global running flag for graceful shutdown
RUNNING = True

def stop_all(signum=None, frame=None):
    global RUNNING
    log.info("🛑 Received stop signal, shutting down cleanly...")
    RUNNING = False
    time.sleep(1)
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, stop_all)
signal.signal(signal.SIGTERM, stop_all)

def main():
    mqtt = MqttClient()
    sec = SecuritySystem()
    env = EnvironmentMonitor()

    # Wait briefly for MQTT readiness
    time.sleep(1.5)

    def send_env():
        while RUNNING:
            try:
                data = env.read()
                mqtt.publish("temperature", data["temperature"])
                mqtt.publish("humidity", data["humidity"])
            except Exception as e:
                log.error(f"Env loop error: {e}")
            time.sleep(30)

    def send_security():
        while RUNNING:
            try:
                s = sec.check()
                mqtt.publish("motion", int(s["motion"]))
                mqtt.publish("led_status", s["led_status"])
                mqtt.publish("buzzer_status", s["buzzer_status"])
                if s["image_b64"]:
                    mqtt.publish("camera_last_image", s["image_b64"])
            except Exception as e:
                log.error(f"Security loop error: {e}")
            time.sleep(5)

    threading.Thread(target=send_env, daemon=True).start()
    send_security()

if __name__ == "__main__":
    main()
