# Cyber Honeypot Dashboard

## Overview

Cyber Honeypot Dashboard is a Flask-based security monitoring system that simulates a fake login portal to detect and analyze unauthorized login attempts. The application captures attacker information, stores logs in a SQLite database, and displays real-time analytics through an interactive dashboard.

## Features

* Fake Login Page for capturing login attempts
* IP Address Tracking
* Geolocation Detection
* Browser/User-Agent Logging
* Suspicious Activity Detection
* Admin Trap Panel
* Dashboard Analytics
* CSV Log Export
* SQLite Database Storage
* Real-Time Monitoring

## Technologies Used

### Backend

* Python
* Flask
* SQLite

### Frontend

* HTML
* CSS
* JavaScript

### Security Features

* Honeypot Login Trap
* IP Monitoring
* Geolocation Tracking
* Threat Detection Alerts

## Project Structure

```text
honeypot-dashboard/
│
├── app.py
├── database.py
├── honeypot.db
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   ├── fake_admin.html
│   └── dashboard.html
│
└── requirements.txt
```

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/Cyber-Honeypot-Dashboard.git
cd honeypot-dashboard
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

Application will start on:

```text
http://127.0.0.1:5000
```

## Dashboard

Access the monitoring dashboard:

```text
http://127.0.0.1:5000/dashboard
```

## Educational Purpose

This project was developed for cybersecurity learning, security monitoring, and honeypot research purposes only.

## Future Enhancements

* Real-time attack alerts
* Email notifications
* Attack visualization charts
* Threat intelligence integration
* Multi-honeypot deployment
* Machine Learning based attack detection

## Author

Deepti
MCA Student | Cybersecurity Enthusiast

```
```
