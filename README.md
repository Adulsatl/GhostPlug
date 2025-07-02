
# 👻 GhostPlug – USB Intrusion Logger for Linux

**GhostPlug** is a real-time USB intrusion monitoring tool for Linux.  
It silently watches for USB insertions and instantly sends alerts to **Telegram** with full device information, while logging activity locally.

Runs automatically in the background — no manual activation needed after setup.

---

## 🔐 Features

- 🧠 Runs silently in background (systemd)
- 📬 Telegram alerts on USB insertion
- 📝 Logs events locally to `/var/log/usb_intrusion.log`
- 🔧 One-time install, no user activation required
- 🖥️ Ideal for labs, shared PCs, servers, or offices

---

## 🧰 Requirements

- Linux with `systemd` (Ubuntu, Debian, Fedora, etc.)
- Python 3.6+
- `udevadm`, `lsusb`, `curl`
- Internet access (for Telegram API)

---

## 📋 Step-by-Step Setup

### 1️⃣ Install Required Packages

```bash
sudo apt update
sudo apt install -y python3 python3-pip usbutils udev curl
pip3 install requests
```

---

### 🤖 Step 2: Create Your Telegram Bot

1. Open Telegram → search **[@BotFather](https://t.me/BotFather)**
2. Type `/newbot` → follow the prompts
3. Copy the **bot token** (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
4. Send any message to your new bot
5. In your browser, go to:

```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
```

6. Look for:

```json
"chat": {
  "id": 000000000,
  ...
}
```

This number is your `CHAT_ID`.

---

### 📝 Step 3: Configure the Script

1. Rename the file (if needed):

```bash
mv usb_telegram_logger.py ghostplug.py
```

2. Open `ghostplug.py` and replace:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
```

3. Save and close the file.

---

### 🚀 Step 4: Move Script to System Path

```bash
sudo cp ghostplug.py /usr/local/bin/ghostplug
sudo chmod +x /usr/local/bin/ghostplug
```

---

### ⚙️ Step 5: Create systemd Service (Auto-Run at Boot)

```bash
sudo nano /etc/systemd/system/ghostplug.service
```

Paste this:

```ini
[Unit]
Description=GhostPlug - USB Intrusion Logger
After=network.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/ghostplug
Restart=always
User=root
StandardOutput=append:/var/log/ghostplug.log
StandardError=append:/var/log/ghostplug.err

[Install]
WantedBy=multi-user.target
```

Save and exit.

---

### 🔁 Step 6: Enable & Start the Service (No Manual Activation Needed)

```bash
sudo systemctl daemon-reload
sudo systemctl enable ghostplug
sudo systemctl start ghostplug
```

✅ **GhostPlug will now run automatically at every startup.**

---

## 🧪 Test

Insert a USB device — you should receive a Telegram alert like this:

```
🛑 USB Inserted
📅 Date: 2025-07-02 10:45:20
💾 Device: SanDisk Cruzer Blade
🔌 Port: /dev/sdb
🔐 Serial: 4C530001230520104281
```

---

## 📁 Logs

| File                             | Description                     |
|----------------------------------|---------------------------------|
| `/var/log/usb_intrusion.log`     | USB device insertion history    |
| `/var/log/ghostplug.log`         | Background stdout logs (systemd)|
| `/var/log/ghostplug.err`         | Background error logs           |

---

## 🧠 Useful Commands

| Action               | Command                                 |
|----------------------|-----------------------------------------|
| Check service status | `sudo systemctl status ghostplug`       |
| Stop GhostPlug       | `sudo systemctl stop ghostplug`         |
| Restart GhostPlug    | `sudo systemctl restart ghostplug`      |
| Disable on boot      | `sudo systemctl disable ghostplug`      |
| View live log        | `tail -f /var/log/ghostplug.log`        |

---

## ✅ Tested On

- Ubuntu 20.04 / 22.04
- Debian 11+
- Fedora 36+
- Kali Linux
- Arch Linux (with `systemd`)

---

## 📜 License

MIT License — Free to use, modify, and redistribute.

---

## 👤 Author

**Adul S**  
📍 Trivandrum, India  
🔗 [LinkedIn](https://linkedin.com/in/aduls2002)  
📧 aduls.career@gmail.com

---

## 🙌 Support & Contributions

Have ideas or improvements? Pull requests and issues are welcome.

Let’s build the **cleanest, stealthiest Linux USB logger** ever.
