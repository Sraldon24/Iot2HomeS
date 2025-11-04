import logging, threading, time
from datetime import datetime
from modules.camera_handler import CameraHandler

try:
    from gpiozero import LED, Buzzer, MotionSensor, OutputDevice
    HW_OK = True
except Exception:
    HW_OK = False

log = logging.getLogger(__name__)

class SecuritySystem:
    def __init__(self):
        self.led = LED(16) if HW_OK else None
        self.buzzer = Buzzer(26) if HW_OK else None
        self.motion = MotionSensor(6) if HW_OK else None
        self.motor = OutputDevice(21) if HW_OK else None
        self.cam = CameraHandler()

    def _spin_motor(self):
        if not self.motor: return
        self.motor.on()
        time.sleep(2)
        self.motor.off()

    def check(self):
        motion = self.motion.motion_detected if self.motion else False
        led_status = buzzer_status = 0
        image = None

        if motion:
            log.info("Motion detected.")
            if self.led: self.led.on(); led_status = 1
            if self.buzzer: self.buzzer.on(); buzzer_status = 1
            threading.Thread(target=self._spin_motor, daemon=True).start()
            time.sleep(0.8)
            if self.buzzer: self.buzzer.off(); buzzer_status = 0
            image = self.cam.capture_b64()
        else:
            if self.led: self.led.off()
            if self.buzzer: self.buzzer.off()

        return {
            "timestamp": datetime.now().isoformat(),
            "motion": motion,
            "led_status": led_status,
            "buzzer_status": buzzer_status,
            "image_b64": image
        }
