 GhostPlug
markdown
Copy
Edit
# 👻 GhostPlug

**GhostPlug** is a lightweight, real-time USB intrusion logger for Linux systems.  
It monitors USB insertions and immediately sends alerts via **Telegram**, helping you secure systems from unauthorized USB usage.

---

## 🔐 Features

- 🕵️ Real-time detection of USB insertions  
- 📬 Telegram alerts with device name, port, and serial  
- 📁 Logs saved to `/var/log/usb_intrusion.log`  
- 🔄 Optional background service (auto-start on boot)  
- 🧠 Lightweight, Python-based, and easy to customize  

---

## 📦 Requirements

- Python 3.6+
- `udevadm` (from udev)
- `lsusb` (from `usbutils`)
- Telegram bot token & chat ID
- `systemd` (for background service)

Install dependencies:

```bash
sudo apt update
sudo apt install python3-pip usbutils udev
pip3 install requests
⚙️ Telegram Setup
Open @BotFather on Telegram

Send /newbot and follow prompts

Copy your Bot Token

To get your chat ID:

Send any message to your new bot

Visit:
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates

Look for "chat": {"id": 123456789} — that's your CHAT_ID

🛠️ Setup
📁 1. Copy the script
Rename the script to ghostplug.py and move it:

bash
Copy
Edit
sudo cp ghostplug.py /usr/local/bin/ghostplug
sudo chmod +x /usr/local/bin/ghostplug
Edit it and set your:

python
Copy
Edit
BOT_TOKEN = "your-telegram-bot-token"
CHAT_ID = "your-chat-id"
🖐️ Manual Activation (Run When Needed)
To run manually anytime:

bash
Copy
Edit
sudo python3 /usr/local/bin/ghostplug
Press Ctrl+C to stop.

🔁 Background Service (Start on Boot)
📄 Create systemd service
bash
Copy
Edit
sudo nano /etc/systemd/system/ghostplug.service
Paste:

ini
Copy
Edit
[Unit]
Description=GhostPlug - USB Intrusion Logger with Telegram Alerts
After=network.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/ghostplug
Restart=always
User=root
StandardOutput=append:/var/log/ghostplug.log
StandardError=append:/var/log/ghostplug.err

[Install]
WantedBy=multi-user.target
✅ Enable and Start
bash
Copy
Edit
sudo systemctl daemon-reload
sudo systemctl enable ghostplug
sudo systemctl start ghostplug
🧪 Verify It's Running
bash
Copy
Edit
sudo systemctl status ghostplug
You should see:
Active: active (running)

📬 Telegram Alert Format
When a USB is inserted, you receive:

yaml
Copy
Edit
🛑 USB Inserted
📅 Date: 2025-07-02 10:45:20
💾 Device: SanDisk Cruzer Blade
🔌 Port: /dev/sdb
🔐 Serial: 4C530001230520104281
