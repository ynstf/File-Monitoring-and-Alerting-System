# Real-time File Monitoring and Alerting System

## Overview

This project implements a real-time file monitoring and alerting system. It utilizes Flask for the web server, Socket.IO for real-time communication, and Watchdog for file system monitoring. Users can select a directory to monitor, choose between email and desktop notifications for critical file changes, and receive instant alerts when the specified critical file is modified.

## Features

- Real-time file monitoring with WebSocket communication
- User-friendly web interface to select directories and configure alerts
- Choice between email notifications and desktop notifications (on PC)
- Optional configuration of a critical file for immediate alerts
- Cross-platform desktop notifications using the `plyer` library

## Technologies Used

- Flask: A web framework for Python
- Socket.IO: Enables real-time, bidirectional, and event-based communication
- Watchdog: Monitors file system events
- Plyer: Cross-platform API to access features commonly found on various operating systems

## Installation

### Clone the repository:

   ```git clone https://github.com/ynstf/File-Monitoring-and-Alerting-System.git```

Install dependencies:
```pip install -r requirements.txt```

Set up your environment variables by creating a .env file:

```EMAIL=your-email@gmail.com```
```PWD=your-email-password```

Replace your-email@gmail.com and your-email-password with your actual email and password.

### Run the application:

    python interface.py

    Visit http://localhost:5000/ in your browser.


### Configuration

- **Select Directory** : Use the web interface to choose the directory you want to monitor.
- **Alert Method** : Choose between "Email" and "Notification on PC" for receiving alerts.
- **Your Email** : If you choose "Email," enter your email address.
- **Critical File (optional)** : Optionally specify a critical file for immediate alerts.

## Screenshots:
### interface:

![interface](https://github.com/ynstf/File-Monitoring-and-Alerting-System/assets/107154559/06c1c763-a57e-4d6c-98d1-6e6aa2b11c53)

### web:

![web](https://github.com/ynstf/File-Monitoring-and-Alerting-System/assets/107154559/620935a4-cbd4-422d-ab44-186c9511612e)

### alerts:
#### emails:
![mail](https://github.com/ynstf/File-Monitoring-and-Alerting-System/assets/107154559/900ea3f9-001f-4775-a5ce-0ffcb48f5685)
#### window:
![alert win](https://github.com/ynstf/File-Monitoring-and-Alerting-System/assets/107154559/6d70ba5f-7d5e-48b8-b517-bf6cf8c48a45)


## License

This project is licensed under the [MIT License](LICENSE).
