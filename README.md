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

   ```git clone https://github.com/your-username/real-time-file-monitoring.git```

Install dependencies:
```pip install -r requirements.txt```

Set up your environment variables by creating a .env file:

```EMAIL=your-email@gmail.com```
```PWD=your-email-password```

Replace your-email@gmail.com and your-email-password with your actual email and password.

### Run the application:

    ```python interface.py```

    ```python server.py```

    ```Visit http://localhost:5000/ in your browser.```


### Configuration

- **Select Directory** : Use the web interface to choose the directory you want to monitor.
- **Alert Method** : Choose between "Email" and "Notification on PC" for receiving alerts.
- **Your Email** : If you choose "Email," enter your email address.
- **Critical File (optional)** : Optionally specify a critical file for immediate alerts.

## Screenshots:


## License

This project is licensed under the [MIT License](LICENSE).