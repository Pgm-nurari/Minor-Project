# FinSight

FinSight is a web application built with Flask to provide management dashboards for admins, event managers, and finance teams. This project utilizes MySQL for data storage and Bootstrap for front-end styling, creating a seamless user experience across different roles.

## Project Structure

```plaintext
FinSight/
├── app/
│   ├── modules/              # Reusable Python modules (e.g., validations)
│   ├── static/               # Static assets: CSS, images, JavaScript
│   │   ├── css/
│   │   ├── images/
│   │   └── js/
│   ├── templates/            # HTML templates for each section and component
│   │   ├── admin/            # Templates specific to admin views
│   │   ├── components/       # Shared components for reuse
│   │   ├── event_manager/    # Templates specific to event management
│   │   ├── finance_manager/  # Templates specific to finance management
│   │   ├── home/             # Templates for the homepage
│   │   └── base.html         # Base template structure for all pages
│   ├── __init__.py           # Initializes the Flask app and registers blueprints
│   ├── admin.py              # Admin dashboard logic and views
│   ├── event_manager.py      # Event management logic and views
│   ├── finance_manager.py    # Finance management logic and views
│   ├── home.py               # Homepage logic and views
│   └── routes.py             # General route definitions
├── .flaskenv                 # Environment variables for Flask setup
├── app.py                    # Main entry point to start the Flask app
├── LICENSE                   # Project license
├── README.md                 # Documentation for project setup and usage
└── requirements.txt          # List of Python dependencies
