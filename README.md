# politimer

**Politimer** is a lightweight countdown display designed for outdoor speaking events.
It manages speaker time limits with a loopable schedule and minimal visual clutter, ideal for public forums, debates, and protests.

---

## 🚀 Features

- ✅ Simple, fullscreen timer display for speaker queue
- ✅ JSON-based schedule with speaker names and durations
- ✅ Navigation via keyboard (next/previous speaker)
- ✅ Pause/resume functionality
- ✅ Countdown with visual alert when time expires
- ✅ Kiosk-mode friendly (no terminal or mouse interaction required)

---

## 📦 Setup

### 1. Install Requirements

Install Requirements

```bash
pip install -r requirements.txt
```

You may need tkinter installed system-wide (usually comes preinstalled with Python). On Raspberry Pi OS:

```bash
sudo apt install python3-tk
```


### 2. Prepare a Schedule

Your JSON file should follow this format:

```JSON
[
  {"speaker": "Alice", "time": "00:05:00"},
  {"speaker": "Bob", "time": "00:07:00"},
  {"speaker": "Charlie", "time": "00:04:30"}
]
```

### 3. Run It

```bash
python -m politimer data/schedule.json
```

## 🖥 GUI Controls

| Key     | Action                 |
|--------:|------------------------|
| `right arrow`     | Next speaker           |
| `left arrow`     | Previous speaker       |
| `space` | Pause/resume countdown |
| `Esc`   | Exit program           |


## 🔧 Run at Boot (Linux / Raspberry Pi)

This is windowmanager specific, but here is one approach

```bash
~/.config/lxsession/LXDE-pi/autostart
```

Add this line:

```bash
@/usr/bin/python3 /home/pi/politimer -m politimer /home/pi/politimer/data/schedule.json
```

### Option 2: Systemd Service

Create /etc/systemd/system/politimer.service:

```ini
[Unit]
Description=Politimer Speaker Timer
After=network.target

[Service]
ExecStart=/usr/bin/python3 -m politimer /home/pi/politimer/data/schedule.json
WorkingDirectory=/home/pi/politimer
Restart=always
User=pi
Environment=DISPLAY=:0

[Install]
WantedBy=default.target
```

Enable and start:

```bash
sudo systemctl enable politimer
sudo systemctl start politimer
```

### 📜 License

AGPL
