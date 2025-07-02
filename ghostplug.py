#!/usr/bin/env python3

import os
import time
import socket
import subprocess
import requests
from datetime import datetime

# === CONFIGURATION ===
BOT_TOKEN = "7716319908:AAEwjGNez1ogJmrfrDskEYnKHDGGvrFAxlM"
CHAT_ID = "7925159901"
LOG_FILE = "/var/log/usb_intrusion.log"

# === FUNCTIONS ===

def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        requests.post(url, data=payload)
    except Exception as e:
        log_event(f"Failed to send Telegram message: {e}")

def log_event(entry):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp}] {entry}\n")

def get_usb_info(dev_name):
    try:
        info = subprocess.check_output(['udevadm', 'info', '--query=all', f'--name={dev_name}'], text=True)
        model = vendor = serial = "Unknown"
        for line in info.splitlines():
            if "ID_MODEL=" in line:
                model = line.split("=", 1)[1]
            elif "ID_VENDOR=" in line:
                vendor = line.split("=", 1)[1]
            elif "ID_SERIAL_SHORT=" in line:
                serial = line.split("=", 1)[1]

        if model == "Unknown" or serial in ["", "Unknown"]:
            lsusb_output = subprocess.check_output(['lsusb'], text=True)
            model_lines = [l for l in lsusb_output.splitlines() if dev_name[-1] in l]
            if model_lines:
                model = " ".join(model_lines[0].split()[6:])

        return model or "Unknown", vendor or "Unknown", serial or "Unavailable"
    except Exception as e:
        return "Unknown", "Unknown", "Unavailable"

def monitor_usb():
    seen = set()
    hostname = socket.gethostname()

    while True:
        try:
            output = subprocess.check_output(["lsblk", "-o", "NAME,TYPE"], text=True)
            devices = set()
            for line in output.splitlines():
                if "disk" in line:
                    devices.add("/dev/" + line.split()[0])

            new_devices = devices - seen
            for dev in new_devices:
                model, vendor, serial = get_usb_info(dev)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if model == "Unknown":
                    message = f"🛑 <b>Unknown USB Inserted</b>\n\n"                               f"💻 <b>Host:</b> {hostname}\n"                               f"📅 <b>Time:</b> {timestamp}"
                    log_event(f"Unknown USB Inserted - Host: {hostname}, Time: {timestamp}")
                else:
                    message = f"🛑 <b>USB Inserted</b>\n\n"                               f"💻 <b>Host:</b> {hostname}\n"                               f"📅 <b>Time:</b> {timestamp}\n"                               f"💾 <b>Device:</b> {vendor} {model}\n"                               f"🔌 <b>Port:</b> {dev}\n"                               f"🔐 <b>Serial:</b> {serial}"
                    log_event(f"USB Inserted - Host: {hostname}, Device: {vendor} {model}, Port: {dev}, Serial: {serial}")
                send_telegram_alert(message)

            seen = devices
            time.sleep(2)
        except Exception as e:
            log_event(f"Monitoring error: {e}")
            time.sleep(5)

# === START ===
if __name__ == "__main__":
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()
    monitor_usb()
