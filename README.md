# 🏠 DomiSafeApp2 — IoT Home Security System

A Raspberry Pi–based smart security system that detects motion, captures images, and uploads sensor data to **Adafruit IO** using **MQTT**.  
The project integrates multiple sensors (PIR, DHT11), actuators (buzzer, LED, motor), and a camera for event-triggered automation.

---

## 📦 Features

| Module | Description |
|--------|--------------|
| 🔔 **Security System** | Detects motion via PIR sensor, activates LED + buzzer + motor, and captures camera image |
| 🌡 **Environmental Monitor** | Reads DHT11 temperature and humidity data |
| ☁️ **MQTT Communication** | Publishes all readings and status updates to Adafruit IO over TLS |
| 📷 **Camera Handler** | Captures Base64 images using `picamera2` |
| ⚙️ **Config Loader** | Reads configuration dynamically from `config.json` |
| 🧠 **Threaded Architecture** | Runs environment and security loops concurrently for real-time operation |

---

## 🧰 Hardware Components

| Component | Pin (BCM) | Board Pin | Notes |
|------------|-----------|-----------|-------|
| PIR Motion Sensor | 6 | 31 | Detects motion |
| LED Indicator | 16 | 36 | Flashes when motion detected |
| Buzzer | 26 | 37 | Beeps on motion event |
| DHT11 Sensor | 4 | 7 | Measures temperature & humidity |
| DC Motor | 21 | 40 | Spins briefly when motion detected |
| Camera Module | CSI Port | — | Captures photo when motion detected |

---
## ⚡ Installation (Raspberry Pi)

```bash
# 1️⃣ Clone repository
git clone https://github.com/Sraldon24/Iot2HomeS.git
cd Iot2HomeS

# 2️⃣ Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3️⃣ Install dependencies
pip install -r requirements.txt
# OR manually
pip install paho-mqtt adafruit-circuitpython-dht gpiozero picamera2 opencv-python board
  
# 4️⃣ Run the program
python3 main.py

```
## 🧠 Author & Credits
Developed by Amir (Sraldon24)
Computer Science Student — Champlain College Saint-Lambert
Guided by in-class IoT module standards and Raspberry Pi best practices.

---
## 🎥 YouTube Demo

Watch the full system in action (hardware + dashboard):

👉 **[▶️ Watch Demo on YouTube](https://www.youtube.com/watch?v=YOUR_VIDEO_ID_HERE)**  

> The video demonstrates:
> - Motion detection triggering LED, buzzer, and motor
> - Real-time temperature & humidity monitoring  
> - Image capture and Adafruit IO feed updates  
> - MQTT data flow from Raspberry Pi → Adafruit Cloud
