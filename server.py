import json
import os
import time
from flask import Flask, render_template, Response, request, redirect, url_for
from flask_socketio import SocketIO
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from dotenv import load_dotenv
from sender.send_email import send_email_to
import ctypes
from plyer import notification

app = Flask(__name__)
socketio = SocketIO(app)

last_position = 0
selected_file = None
critical_file = None  
user_email = None
alert_method = None

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global last_position
        if event.is_directory:
            return
        content = get_file_content()

        try:
            data_dict = json.loads(content[last_position:])
            data = f"{data_dict['event_type'].replace('_', ' ').capitalize()}: {data_dict['path']}"
            data = data + '\n'
            socketio.emit('file_update', data)

            # Check if the modified file is the critical file
            if critical_file and data_dict.get("path", "").split("\\")[-1] == critical_file:
                socketio.emit('critical_file_update', {'data': f'{critical_file} has changed!', 'criticality': 'critical'})
                #socketio.emit('critical_file_update', data)  # Emit a special event for critical file changes
                # Send an email to the user
                # user_email = request.form.get('email')  # Retrieve the user's email from the form
                
                if alert_method == 'notification':
                    # show notifiation to user
                    try:
                        ctypes.windll.user32.MessageBoxW(0, f'The critical file {critical_file} has been modified. Take immediate action!', 'Critical File Alert', 1)
                    except Exception as e:
                        # Cross-platform notification using plyer
                        notification_title = 'Critical File Alert'
                        notification_message = f'The critical file {critical_file} has been modified. Take immediate action!'
                        notification.notify(
                            title=notification_title,
                            message=notification_message,
                            app_icon=None,  # e.g., 'path/to/icon.png'
                            timeout=22  # Notification will disappear after 22 seconds
                        )
                        print(f"Error displaying notification on windows : {e}")
                else :
                    #send email to user
                    load_dotenv()
                    send_email_to(user_email, critical_file)

        except json.JSONDecodeError:
            socketio.emit('file_update', content[last_position:])
            print(content[last_position:])
        
        last_position = len(content)

def get_file_content():
    global selected_file
    if selected_file is None or not os.path.exists(selected_file):
        return ""
    with open(selected_file, 'r') as file:
        return file.read()

def format_event_data(data_dict):
    return f"{data_dict['event_type'].replace('_', ' ').capitalize()}: {data_dict['path']}\n"

@app.route('/')
def index():
    return render_template('index.html', selected_file=selected_file, critical_file=critical_file)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/upload', methods=['POST'])
def upload_file():
    global selected_file, critical_file, user_email, alert_method
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"

    selected_file = os.path.join(app.root_path, file.filename)
    file.save(selected_file)

    # Retrieve the user's email from the form
    alert_method = request.form.get('alert_method')
    if alert_method == 'email':
        user_email = request.form.get('email')

    # Added: Allow user to input the critical file name
    critical_file = request.form.get('critical_file', None)

    return redirect(url_for('index'))

def generate_file():
    while True:
        yield get_file_content()[last_position:].encode('utf-8')
        time.sleep(1)

if __name__ == '__main__':
    observer = Observer()
    observer.schedule(MyHandler(), path=os.path.dirname(os.path.abspath('your_file.txt')), recursive=False)
    observer.start()

    #socketio.run(app, debug=False)
    threading.Thread(target=socketio.run, args=(app,), kwargs={'debug': False}).start()
