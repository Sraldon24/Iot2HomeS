import json, os, logging

log = logging.getLogger(__name__)

DEFAULTS = {
    "ADAFRUIT_IO_USERNAME": "",
    "ADAFRUIT_IO_KEY": "",
    "MQTT_BROKER": "io.adafruit.com",
    "MQTT_PORT": 8883,
    "DHT_PIN": 4,
    "MOTOR_PIN": 21,
    "security_check_interval": 5,
    "env_interval": 30,
    "camera_enabled": True
}

def load_config(path="config.json"):
    cfg = dict(DEFAULTS)
    if os.path.exists(path):
        try:
            with open(path) as f:
                cfg.update(json.load(f))
                log.info(f"✅ Loaded config from {path}")
        except Exception as e:
            log.warning(f"⚠️ Failed reading {path}: {e}")
    else:
        log.warning(f"⚠️ Using default configuration")
    return cfg
