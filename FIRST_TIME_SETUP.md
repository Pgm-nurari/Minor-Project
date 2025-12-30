# 🚀 First Time Setup Guide

This guide will help you set up FinSight for the first time. Follow these steps in order.

## Prerequisites

Before you begin, make sure you have:

- ✅ **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- ✅ **MySQL Server 8.0+** - [Download MySQL](https://dev.mysql.com/downloads/)
- ✅ **Git** (optional) - [Download Git](https://git-scm.com/)

## Step 1: Get the Project

**Option A: Clone from Git**
```bash
git clone <repository-url>
cd FinSight
```

**Option B: Download ZIP**
1. Download the project ZIP file
2. Extract to a folder
3. Open command prompt/terminal in that folder

## Step 2: Install MySQL

1. **Install MySQL Server** if not already installed
2. **Start MySQL service**:
   - Windows: Services → MySQL → Start
   - Mac: `brew services start mysql`
   - Linux: `sudo systemctl start mysql`

3. **Note your MySQL credentials**:
   - Default username: `root`
   - Password: (the one you set during installation)

## Step 3: Configure Environment Variables

1. **Copy the example environment file**:
   ```bash
   copy .env.example .env
   ```
   *(On Mac/Linux use `cp .env.example .env`)*

2. **Edit the `.env` file** with your favorite text editor:
   ```bash
   notepad .env
   ```

3. **Update these values**:
   ```env
   DB_USERNAME=root
   DB_PASSWORD=your_actual_mysql_password_here
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=finsight_db
   SECRET_KEY=change_this_to_something_random
   ```

4. **Generate a secure SECRET_KEY** (optional but recommended):
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Copy the output and paste it as your SECRET_KEY in `.env`

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- SQLAlchemy (database ORM)
- PyMySQL (MySQL connector)
- And other required packages

## Step 5: Run the Application

### Option A: Using start.bat (Windows - EASIEST!)

Just double-click `start.bat` or run:
```bash
start.bat
```

The script will automatically:
- ✅ Check Python installation
- ✅ Verify .env file exists
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Start the application

### Option B: Manual Start (All Platforms)

```bash
python run.py
```

## Step 6: Access the Application

1. Open your web browser
2. Go to: **http://127.0.0.1:5000**
3. You should see the FinSight login page

## Step 7: First Login

The application automatically creates sample data on first run.

**Default Admin Account:**
- Email: `admin@finsight.com`
- Password: `Password@123`

**Other Test Accounts:**
- Event Manager: `john.doe@finsight.com` / `Password@123`
- Finance Manager: `jane.smith@finsight.com` / `Password@123`

## 🎉 You're Done!

The application will automatically:
- Create the database (`finsight_db`)
- Create all required tables (16 tables)
- Set up sample data for testing

## 📊 What Gets Created Automatically

When you run the app for the first time, it creates:

- **5 Departments** (CS, Commerce, Visual Media, etc.)
- **3 Roles** (Admin, Event Manager, Finance Manager)
- **8 Users** (including admin and test accounts)
- **5 Event Types** (Conference, Workshop, etc.)
- **5 Events** with dates and budgets
- **5 Sub-Events**
- **12 Transactions** with line items
- **Sample metadata** (payment modes, categories, etc.)

## Troubleshooting

### "Can't connect to MySQL server"
- Make sure MySQL service is running
- Check username/password in `.env`
- Try: `mysql -u root -p` to test connection

### "Access denied for user"
- Double-check `DB_PASSWORD` in `.env`
- No spaces around the `=` sign
- Password should not be in quotes

### "ModuleNotFoundError: No module named 'flask'"
- Run: `pip install -r requirements.txt`
- Make sure you're in the project directory

### "Port 5000 already in use"
- Another app is using port 5000
- Stop the other app, or
- Edit `run.py` and change port to 5001

### Database already exists warning
- This is normal! The app detected existing database
- It will use the existing database
- To start fresh, run: `python scripts/setup_database.py`

## Next Steps

1. **Explore the application** with the test accounts
2. **Change default passwords** in production
3. **Read the documentation** in `docs` folder
4. **Customize** for your needs

## Quick Commands Reference

```bash
# Start application
python run.py

# Windows quick start
start.bat

# Reset database
python scripts/setup_database.py

# Populate fresh data
python scripts/populate_db.py

# Run with custom port
python run.py --port 5001
```

## Need Help?

- 📖 Read `docs/README.md` for detailed documentation
- 🔧 Check `docs/INSTALLATION.md` for advanced setup
- 🔒 See `docs/SECURITY.md` for security best practices

---

**Welcome to FinSight! Happy Event Managing! 🎉**
