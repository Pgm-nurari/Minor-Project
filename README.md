# FinSight 💼

> A comprehensive web-based Financial Event Management System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-green.svg)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 First Time Setup (Windows)

**Three simple steps:**

1. **Install MySQL** and start the service
2. **Configure `.env` file:**
   ```bash
   copy .env.example .env
   notepad .env
   # Set your MySQL password in DB_PASSWORD
   ```
3. **Run the application:**
   ```bash
   start.bat
   ```

📖 **Detailed first-time setup guide:** [FIRST_TIME_SETUP.md](FIRST_TIME_SETUP.md)

---

## 🚀 Quick Start (All Platforms)

```bash
# 1. Install MySQL and start the service

# 2. Configure environment
copy .env.example .env
# Edit .env and set your MySQL password

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python run.py
```

**That's it!** The application will automatically:
- ✅ Create the database if it doesn't exist
- ✅ Set up all required tables (16 tables)
- ✅ Populate sample data (8 users, 5 events, 12 transactions)
- ✅ Start the development server at http://127.0.0.1:5000

## 📚 Features

- 🔐 **Secure Authentication** - Password hashing and session management
- 👥 **Multi-Role Support** - Admin, Event Manager, Finance Manager
- 📊 **Event Management** - Create and track events, sub-events, and budgets
- 💰 **Transaction Tracking** - Record and manage financial transactions
- 📈 **Advanced Analytics** - Interactive visualizations and reports
- � **Real-time Notifications** - Smart alerts for assignments, updates, and budget thresholds
- 📝 **Activity Logging** - Complete audit trail of all system actions
- 💵 **Budget Monitoring** - Automatic alerts at 50%, 75%, 90%, and 100% of budget
- 🔍 **Smart Tables** - Search, filter, sort, and export data
- 🎨 **Modern UI** - Responsive design with gradient themes
- ✏️ **Profile Management** - Edit profile and change passwords for all users

## 👤 Default Credentials

After first run, login with:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@finsight.com | Password@123 |
| Event Manager | john.doe@finsight.com | Password@123 |
| Finance Manager | jane.smith@finsight.com | Password@123 |

**⚠️ Change these passwords in production!**

## 📖 Documentation

- 🚀 **[FIRST_TIME_SETUP.md](FIRST_TIME_SETUP.md)** - Complete first-time setup guide
- � **[NOTIFICATION_SYSTEM.md](NOTIFICATION_SYSTEM.md)** - Notification and activity logging system
- �📚 **[docs/README.md](docs/README.md)** - Full documentation
- 🔧 **[docs/INSTALLATION.md](docs/INSTALLATION.md)** - Advanced installation
- 🔒 **[docs/SECURITY.md](docs/SECURITY.md)** - Security best practices
- 📊 **[docs/PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md)** - Project overview

## 🛠️ Tech Stack

- **Backend:** Flask 3.0.3, SQLAlchemy 2.0.31
- **Database:** MySQL 8.0+
- **Frontend:** Bootstrap 5, Custom CSS/JS
- **Visualization:** Plotly 5.22.0
- **Security:** Werkzeug password hashing, Flask sessions

## 📁 Project Structure

```
FinSight/
├── app/                  # Main application
│   ├── modules/         # Core business logic
│   │   ├── models.py          # Database models
│   │   ├── activity_logger.py # Notification & logging
│   │   └── budget_monitor.py  # Budget tracking
│   ├── static/          # CSS, JS, images
│   └── templates/       # HTML templates
├── scripts/             # Utility scripts
│   ├── populate_db.py  # Sample data
│   └── setup_database.py
├── database/            # SQL schemas
├── docs/               # Documentation
├── .env                # Your config (create from .env.example)
├── run.py              # Application entry point
└── start.bat           # Windows quick-start
```

## 🔧 Additional Commands

```bash
# Populate database with fresh sample data
python scripts/populate_db.py

# Reset database from scratch
python scripts/setup_database.py

# Run on different port
python run.py --port 5001
```

## 🐛 Troubleshooting

**Can't connect to database?**
- Check MySQL is running
- Verify credentials in `.env` file
- See [FIRST_TIME_SETUP.md](FIRST_TIME_SETUP.md) for detailed help

**Import errors?**
```bash
pip install -r requirements.txt
```

**Port 5000 already in use?**
```bash
python run.py --port 5001
```

## � Notification System

FinSight includes a comprehensive notification and activity logging system:

- **Real-time Notifications** - Notification bell in header with unread count
- **Smart Alerts** - Budget thresholds, large transactions, manager assignments
- **Activity Logs** - Complete audit trail of all user actions
- **Automated Triggers** - Event creation, transaction updates, report generation

See [NOTIFICATION_SYSTEM.md](NOTIFICATION_SYSTEM.md) for complete documentation.

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

**Made with ❤️ for efficient financial event management**
