#!/usr/bin/env python3
import subprocess, sys

pkgs = [
    "paho-mqtt",
    "adafruit-circuitpython-dht",
    "gpiozero",
    "picamera2",
    "opencv-python",
    "board"
]

for p in pkgs:
    try:
        __import__(p.replace("-", "_"))
    except ImportError:
        print(f"📦 Installing {p} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", p])
