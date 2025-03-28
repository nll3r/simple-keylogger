# Simple Keylogger

This is an educational project that demonstrates how to create a simple keylogger in Python. **This project is for educational and learning purposes only. Do not use this code for malicious or illegal activities.**

## Project Structure

- `dependencies.bat`: Script to install the required dependencies (works only on Windows).
- `keylogger.py`: The script that must be executed on the victim's machine to capture keystrokes.
- `server.py`: The Flask server that receives and displays the captured keystroke logs.
- `readme.md`: This file, containing information about the project.

## How It Works

1. The `keylogger.py` file captures the keystrokes on the victim's machine and sends the data to the server.
2. The `server.py` file runs on the attacker's (hacker's) machine and displays the keystroke logs and the active window in real-time.

## Warnings

- **Ethical Use**: This project is for learning purposes only. Using this code to invade others' privacy or for any illegal activity is strictly prohibited.
- **Responsibility**: The author is not responsible for any misuse of this code.

## Requirements

- Python 3.7 or higher.
- Windows operating system for the `dependencies.bat` script.

## Installation

### For the Hacker (Server)

1. Make sure Python is installed.
2. Install the required dependencies:
   ```bash
   pip install flask