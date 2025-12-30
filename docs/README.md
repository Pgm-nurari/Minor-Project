# FinSight - Financial Event Management System

## 🎯 Project Overview

FinSight is a comprehensive web-based Financial Event Management System built with Flask, designed to help organizations manage events, budgets, and financial transactions efficiently.

## ✨ Features

### For Administrators
- ✅ User management (create, edit, delete, authorize users)
- ✅ Complete event oversight and management
- ✅ System-wide financial reporting
- ✅ Role and department management

### For Event Managers
- ✅ Create and manage events and sub-events
- ✅ Track event budgets
- ✅ Record and manage transactions
- ✅ View transaction history with advanced search/filter
- ✅ Generate financial reports

### For Finance Managers
- ✅ Monitor all events and budgets
- ✅ Financial visualization and analytics
- ✅ Export financial data
- ✅ Cross-event budget tracking

### General Features
- 🔐 Secure authentication with password hashing
- 📊 Advanced table features (search, sort, filter, export CSV)
- 📈 Interactive data visualizations
- 🎨 Modern, responsive UI with gradient themes
- 📱 Mobile-friendly design

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FinSight
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure database**
   Edit `app/config.py` and update the MySQL password:
   ```python
   db_password = quote_plus('your_mysql_password')
   ```

4. **Run the application**
   ```bash
   python run.py
   ```
   
   The application will automatically:
   - Check and install dependencies
   - Create the database if it doesn't exist
   - Create all required tables on first run
   - Start the Flask development server

5. **Access the application**
   Open your browser and navigate to: `http://127.0.0.1:5000`

### First-Time Setup

If you're running with an empty database, populate it with sample data:
```bash
python scripts/populate_db.py
```

## 👤 Default Login Credentials

| Role             | Email                     | Password      |
|------------------|---------------------------|---------------|
| Admin            | admin@finsight.com        | Password@123  |
| Event Manager    | john.doe@finsight.com     | Password@123  |
| Finance Manager  | jane.smith@finsight.com   | Password@123  |

**⚠️ Important:** Change these passwords after first login in production!

## 📁 Project Structure

```
FinSight/
├── app/                          # Main application package
│   ├── __init__.py              # App factory and initialization
│   ├── config.py                # Configuration settings
│   ├── admin.py                 # Admin blueprint
│   ├── event_manager.py         # Event Manager blueprint
│   ├── finance_manager.py       # Finance Manager blueprint
│   ├── home.py                  # Authentication routes
│   ├── routes.py                # Blueprint registration
│   ├── modules/                 # Core modules
│   │   ├── models.py           # Database models
│   │   ├── db_queries.py       # Database query functions
│   │   ├── validations.py      # Input validation
│   │   └── transaction_utils.py # Transaction utilities
│   ├── static/                  # Static files (CSS, JS, images)
│   │   ├── css/                # Stylesheets
│   │   ├── js/                 # JavaScript files
│   │   └── images/             # Images
│   └── templates/               # Jinja2 templates
│       ├── base.html           # Base template
│       ├── admin/              # Admin templates
│       ├── event_manager/      # Event Manager templates
│       ├── finance_manager/    # Finance Manager templates
│       ├── home/               # Authentication templates
│       └── components/         # Reusable components
├── scripts/                     # Utility scripts
│   ├── setup_database.py       # Database setup from SQL
│   ├── setup_database_sqlalchemy.py  # Setup using SQLAlchemy
│   └── populate_db.py          # Sample data population
├── docs/                        # Documentation
├── tables.sql                   # Database schema
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
└── app.py                       # Legacy entry point
```

## 🗄️ Database Schema

The application uses 16 tables:
- **User Management:** User, Role, Department
- **Event Management:** Event, Event_Type, Sub_Event, Budget
- **Transactions:** transaction_table, transactionitem
- **Financial Categories:** Transaction_Nature, Payment_Mode, Transaction_Category, Account_Category
- **Reports:** Financial_Statement, Profit_and_Loss, Balance_Sheet

## 🔧 Configuration

### Database Configuration
Edit `app/config.py`:
```python
db_password = quote_plus('your_password')
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{db_password}@localhost/finsight_db'
```

### Environment Variables
Create a `.flaskenv` file:
```
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
```

## 📊 Advanced Features

### Table Component
All data tables include:
- **Global Search:** Search across all columns
- **Column Filters:** Filter by specific column values
- **Sortable Columns:** Click headers to sort ascending/descending
- **Export to CSV:** Download filtered data
- **Responsive Design:** Works on all devices

### Security
- Password hashing using Werkzeug
- SQL injection prevention via SQLAlchemy ORM
- CSRF protection (configure in production)
- Session management

## 🛠️ Development

### Running in Development Mode
```bash
python run.py
```

### Database Management

**Reset Database:**
```bash
python scripts/setup_database.py
```

**Populate Sample Data:**
```bash
python scripts/populate_db.py
```

**Using SQLAlchemy Models:**
```bash
python scripts/setup_database_sqlalchemy.py
```

## 📝 API Endpoints

### Authentication
- `GET /` - Home page
- `POST /login` - User login
- `POST /signup` - User registration
- `GET /logout` - User logout

### Admin Routes (`/admin/<user_id>/`)
- `/` - Admin dashboard
- `/users` - User management
- `/events` - Event management
- `/new_user` - Create user
- `/edit_user/<user_id>` - Edit user
- `/authorize/<user_id>` - Authorize user

### Event Manager Routes (`/evemng/<user_id>/`)
- `/` - Event Manager dashboard
- `/event_details/<event_id>` - Event details
- `/create_transaction/<event_id>` - Create transaction
- `/all_transactions/<event_id>` - View all transactions

### Finance Manager Routes (`/finmng/<user_id>/`)
- `/` - Finance Manager dashboard
- `/event_details/<event_id>` - Event financial details
- `/visualizations/<event_id>` - Financial visualizations

## 🚨 Troubleshooting

### Database Connection Issues
- Verify MySQL is running
- Check credentials in `app/config.py`
- Ensure database `finsight_db` exists
- Check MySQL user permissions

### Import Errors
```bash
pip install -r requirements.txt
```

### Port Already in Use
Change port in `run.py`:
```python
app.run(debug=True, port=5001)
```

## 📦 Dependencies

Key packages:
- Flask 3.0.3
- Flask-SQLAlchemy 3.1.1
- PyMySQL 1.1.1
- Werkzeug 3.0.4
- mysql-connector-python 9.1.0
- plotly 5.24.1

See `requirements.txt` for complete list.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Support

For issues, questions, or contributions:
- Create an issue in the repository
- Contact the development team

## 🔄 Version History

### v1.0.0 (Current)
- Initial release
- Complete CRUD operations for events and transactions
- User management and authentication
- Financial reporting and visualizations
- Advanced table features
- Automatic database setup

---

**Built with ❤️ using Flask and modern web technologies**
