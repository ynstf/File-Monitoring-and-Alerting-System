import os
import json
import time
import tkinter as tk
from tkinter import scrolledtext, filedialog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
from queue import Queue
import threading
import subprocess

# Global Variables for Log File Monitoring
LOG_FILE_NAME = "log.txt"
ALERT_CRITICALITY_THRESHOLD = "CRITICAL"

# Queue for communication between threads
log_queue = Queue()

# Watchdog Handler for File System Events
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            print(f"Directory created: {event.src_path}")
            log_queue.put({"event_type": "directory_created", "path": event.src_path})
        else:
            print(f"File created: {event.src_path}")
            log_queue.put({"event_type": "file_created", "path": event.src_path})

    def on_deleted(self, event):
        if event.is_directory:
            print(f"Directory deleted: {event.src_path}")
            log_queue.put({"event_type": "directory_deleted", "path": event.src_path})
        else:
            print(f"File deleted: {event.src_path}")
            log_queue.put({"event_type": "file_deleted", "path": event.src_path})

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith(LOG_FILE_NAME):
            print(f"Directory modified: {event.src_path}")
            log_queue.put({"event_type": "directory_modified", "path": event.src_path})
        else:
            print(f"File modified: {event.src_path}")

    def on_any_event(self, event):
        if event.event_type == 'deleted':
            if event.is_directory:
                print(f"Directory deleted: {event.src_path}")
                log_queue.put({"event_type": "directory_deleted", "path": event.src_path})
            else:
                print(f"File deleted: {event.src_path}")
                log_queue.put({"event_type": "file_deleted", "path": event.src_path})


# Tkinter User Interface
def create_user_interface():
    def select_directory():
        selected_dir = filedialog.askdirectory()
        path_var.set(selected_dir)
        start_monitoring(selected_dir)

    def start_monitoring(directory):
        # Stop existing observer if any
        global observer  # Move the global declaration here
        if 'observer' in globals():
            observer.stop()
            observer.join()

        # Start directory monitoring
        event_handler = MyHandler()
        observer = Observer()  # Remove the global declaration from here
        observer.schedule(event_handler, directory, recursive=True)
        print(f"Watching directory: {directory}")
        observer.start()


    root = tk.Tk()
    root.title("Log File Monitoring and Alerting System")

    # Set window logo
    logo_image = tk.PhotoImage(file="static/favicon.png")  # Replace with the path to your logo image
    root.iconphoto(True, logo_image)

    # Create Label and Entry for directory selection
    tk.Label(root, text="Select Directory to Monitor:").pack(pady=5)
    path_var = tk.StringVar()
    directory_entry = tk.Entry(root, textvariable=path_var, width=50)
    directory_entry.pack(pady=5)
    tk.Button(root, text="Browse", command=select_directory).pack(pady=5)

    # Add a Label for the additional message
    message_label = tk.Label(root, text="To explore more functionalities, visit: http://localhost:5000/")
    message_label.pack(pady=5)

    # Create scrolled text widget for displaying log changes
    log_display = scrolledtext.ScrolledText(root, width=80, height=20)
    log_display.pack(padx=10, pady=10)

    # Function to update log display
    def update_display():
        # Read the existing log file content and display it
        log_file_path = os.path.join(path_var.get(), LOG_FILE_NAME)
        if os.path.exists(log_file_path):
            with open(log_file_path, "r") as log_file:
                for line in log_file:
                    log_entry = json.loads(line)
                    formatted_entry = f"{log_entry['event_type'].replace('_', ' ').capitalize()}: {log_entry['path']}"
                    log_display.insert(tk.END, f"{formatted_entry}\n")
                    log_display.see(tk.END)  # Scroll to the end

        # Monitor the log queue for real-time updates and save to log file
        while True:
            log_entry = log_queue.get()
            formatted_entry = f"{log_entry['event_type'].replace('_', ' ').capitalize()}: {log_entry['path']}"
            log_display.insert(tk.END, f"{formatted_entry}\n")
            log_display.see(tk.END)  # Scroll to the end

            # Save the log entry to the log file
            with open(log_file_path, "a") as log_file:
                    log_file.write(json.dumps(log_entry) + "\n")

    # Start a thread to update the display
    threading.Thread(target=update_display, daemon=True).start()

    # Start the Flask script in a separate process
    subprocess.Popen(['python', 'server.py'])

    root.mainloop()


# Main Execution
if __name__ == "__main__":
    create_user_interface()
