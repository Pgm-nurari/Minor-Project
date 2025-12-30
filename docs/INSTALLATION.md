# FinSight Installation and Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software
1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Verify installation: `python --version`

2. **MySQL 8.0 or higher**
   - Download from: https://dev.mysql.com/downloads/mysql/
   - Remember the root password you set during installation
   - Ensure MySQL service is running

3. **Git** (optional, for cloning)
   - Download from: https://git-scm.com/downloads

## Installation Steps

### Step 1: Get the Project

**Option A: Clone from Repository**
```bash
git clone <repository-url>
cd FinSight
```

**Option B: Download ZIP**
- Download and extract the project ZIP file
- Open terminal/command prompt in the extracted folder

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

If you encounter permission errors, try:
```bash
pip install --user -r requirements.txt
```

### Step 3: Configure Environment Variables

1. **Copy the example environment file:**
   ```bash
   # Windows
   copy .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```

2. **Edit the `.env` file and update your credentials:**
   ```bash
   # Database Configuration
   DB_USERNAME=root
   DB_PASSWORD=your_mysql_password_here
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=finsight_db
   
   # Flask Configuration
   SECRET_KEY=generate_a_random_secret_key_here
   ```

3. **Save the file**

**Important Security Notes:**
- Never commit the `.env` file to version control (it's already in `.gitignore`)
- Use a strong, random SECRET_KEY in production
- Keep your database password secure

### Step 4: Run the Application

**Windows:**
```bash
# Option 1: Use the batch file
start.bat

# Option 2: Use Python directly
python run.py
```

**Linux/Mac:**
```bash
python3 run.py
```

The application will automatically:
- ✅ Check and install any missing dependencies
- ✅ Create the database `finsight_db` if it doesn't exist
- ✅ Create all required tables on first run
- ✅ Start the Flask development server

### Step 5: Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

or
```
http://localhost:5000
```

### Step 6: Initial Login

Use one of the default credentials to log in:

**Admin Account:**
- Email: `admin@finsight.com`
- Password: `Password@123`

**Event Manager Account:**
- Email: `john.doe@finsight.com`
- Password: `Password@123`

**Finance Manager Account:**
- Email: `jane.smith@finsight.com`
- Password: `Password@123`

## First-Time Database Setup

### Option 1: Populate with Sample Data (Recommended for Testing)

If you're starting with an empty database, populate it with sample data:

```bash
python scripts/populate_db.py
```

This will create:
- 5 Departments
- 3 Roles
- 8 Users
- 5 Events
- 5 Sub-events
- 5 Budgets
- 12 Transactions with items
- All necessary lookup tables

### Option 2: Manual Database Setup

If you prefer to create the database manually:

```bash
# Using SQL file
python scripts/setup_database.py

# Using SQLAlchemy models
python scripts/setup_database_sqlalchemy.py
```

## Troubleshooting

### Issue: "Module not found" Error

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Database Connection Failed

**Possible causes and solutions:**

1. **MySQL not running**
   - Windows: Open Services and start MySQL service
   - Linux: `sudo systemctl start mysql`
   - Mac: `brew services start mysql`

2. **Wrong password**
   - Check `app/config.py` and verify the password
   - Test MySQL connection: `mysql -u root -p`

3. **User permissions**
   - Grant necessary permissions:
     ```sql
     GRANT ALL PRIVILEGES ON finsight_db.* TO 'root'@'localhost';
     FLUSH PRIVILEGES;
     ```

### Issue: Port 5000 Already in Use

**Solution 1:** Stop the process using port 5000

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

**Linux/Mac:**
```bash
lsof -ti:5000 | xargs kill -9
```

**Solution 2:** Change the port

Edit `run.py` and modify the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Import Error for mysql-connector-python

**Solution:**
```bash
pip uninstall mysql-connector-python
pip install mysql-connector-python==9.1.0
```

### Issue: Application Starts but Shows Blank Page

**Possible causes:**

1. **Static files not loading**
   - Clear browser cache (Ctrl+Shift+Delete)
   - Try incognito/private mode

2. **JavaScript errors**
   - Open browser console (F12)
   - Check for any errors
   - Ensure all CSS/JS files are present in `app/static/`

## Development Setup

### Enable Debug Mode

Debug mode is enabled by default in `run.py`. For production, set:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Database Migrations

To reset the database completely:
```bash
# This will DROP and recreate the database
python scripts/setup_database.py
```

When prompted, type `yes` to confirm.

### Environment Variables

Create a `.env` file in the project root (optional):
```
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-here
```

## Production Deployment

For production deployment:

1. **Use a production WSGI server** (e.g., Gunicorn, uWSGI)
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Update configuration**
   - Set `DEBUG = False` in `app/config.py`
   - Use strong `SECRET_KEY`
   - Configure proper database backup

3. **Use environment variables for sensitive data**
   - Don't hardcode passwords
   - Use `.env` file or system environment variables

4. **Set up SSL/HTTPS**
   - Use nginx or Apache as reverse proxy
   - Configure SSL certificates

5. **Enable firewall and security measures**
   - Limit database access
   - Configure CORS if needed
   - Enable rate limiting

## Additional Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **SQLAlchemy Documentation:** https://docs.sqlalchemy.org/
- **MySQL Documentation:** https://dev.mysql.com/doc/

## Getting Help

If you encounter issues not covered here:

1. Check the main [README.md](../README.md)
2. Review the detailed [documentation](README.md)
3. Check error logs in the console
4. Create an issue in the repository

## Quick Reference

### Common Commands

```bash
# Start application
python run.py

# Populate database with sample data
python scripts/populate_db.py

# Reset database
python scripts/setup_database.py

# Install/update dependencies
pip install -r requirements.txt --upgrade
```

### Default URLs

- **Home/Login:** http://127.0.0.1:5000
- **Admin Dashboard:** http://127.0.0.1:5000/admin/{user_id}
- **Event Manager:** http://127.0.0.1:5000/evemng/{user_id}
- **Finance Manager:** http://127.0.0.1:5000/finmng/{user_id}

---

**Happy managing! 🎉**
