# Changelog

All notable changes and improvements to the FinSight project.

## [1.1.0] - 2025-12-30

### 🔒 Security Update - Environment Variables

#### Added
- ✨ **Environment Variable Configuration** - Database credentials now stored in `.env` file
- ✨ **`.env.example`** - Template file for easy setup
- 📚 **`docs/SECURITY.md`** - Comprehensive security best practices guide

#### Changed
- 🔒 **Config System** - Updated `app/config.py` to load credentials from environment variables using `python-dotenv`
- 🔒 **Setup Scripts** - Updated `scripts/setup_database.py` to use environment variables
- 📚 **Documentation** - Updated `README.md` and `docs/INSTALLATION.md` with .env setup instructions

#### Security Improvements
- 🔐 Database credentials no longer hardcoded in source code
- 🔐 `.env` file already in `.gitignore` to prevent accidental commits
- 🔐 Each environment can use different credentials (dev/test/prod)
- 🔐 Secrets can be rotated without code changes

---

## [1.0.0] - 2025-12-30

### 🎉 Major Release - Complete Project Overhaul

### Added

#### Core Features
- ✨ **Automatic Database Setup** - Application now creates database and tables automatically on first run
- ✨ **Advanced Table Features** - Search, filter, sort, and export CSV functionality on all data tables
- ✨ **Modern UI/UX** - Complete redesign with purple gradient theme and smooth animations
- ✨ **Startup Script** - New `run.py` with dependency checking and helpful startup messages
- ✨ **Windows Batch File** - `start.bat` for one-click startup on Windows

#### Security Enhancements
- 🔒 Password hashing for all user accounts (Werkzeug scrypt algorithm)
- 🔒 Fixed password exposure in URL parameters
- 🔒 Secure default password generation for admin-created users
- 🔒 Removed plain-text password storage

#### Documentation
- 📚 Comprehensive `docs/README.md` with full project documentation
- 📚 Detailed `docs/INSTALLATION.md` with step-by-step setup guide
- 📚 `docs/PROJECT_SUMMARY.md` with complete project overview
- 📚 Updated main `README.md` with quick-start guide
- 📚 Inline code comments and documentation

#### Database
- 🗄️ Fixed table name mismatches (transaction_table vs Transactions_table)
- 🗄️ Added missing `transactionitem` table
- 🗄️ Added missing `Budget` table
- 🗄️ Added `Sub_Event_ID` column to transactions
- 🗄️ Added `modified_date` columns where missing
- 🗄️ Fixed invalid CHECK constraints
- 🗄️ Set proper default values (Amount = 0.00)
- 🗄️ Automatic database initialization in `app/__init__.py`

#### Project Organization
- 📁 Created `scripts/` folder for utility scripts
- 📁 Created `database/` folder for SQL files
- 📁 Created `docs/` folder for documentation
- 📁 Moved `setup_database.py` to scripts
- 📁 Moved `setup_database_sqlalchemy.py` to scripts
- 📁 Moved `populate_db.py` to scripts
- 📁 Moved `insert_dummy_data.sql` to scripts
- 📁 Moved `tables.sql` to database folder

### Changed

#### UI/UX Improvements
- 🎨 Login page - Modern gradient background, improved forms, animations
- 🎨 Event cards - Gradient accent bars, better shadows, hover effects
- 🎨 Tables - Gradient headers, modern buttons, improved row styling
- 🎨 User auth cards - Gradient accent stripe, modern card design
- 🎨 Signup page - Gradient background, modern inputs
- 🎨 Header - Gradient background, glassmorphism buttons
- 🎨 Footer - Gradient background, improved link styling
- 🎨 Buttons - Consistent gradient styling with hover lift effects
- 🎨 Forgot/Reset password pages - Complete modernization
- 🎨 Color scheme - Changed from green to purple gradient (#667eea to #764ba2)

#### Component Enhancements
- ⚡ Table component - Added search, filter, sort, export functionality
- ⚡ Table component - Added column-specific filters with dropdowns
- ⚡ Table component - Added filter count badge
- ⚡ Table component - Added "Clear Filters" button
- ⚡ Table component - Sortable column headers with visual indicators
- ⚡ Table component - CSV export with timestamp

#### Database Scripts
- 🔧 `populate_db.py` - Enhanced with table existence checks
- 🔧 `populate_db.py` - Better error handling and graceful failures
- 🔧 `populate_db.py` - Auto-creates tables if missing
- 🔧 `setup_database.py` - Updated to use new database folder path
- 🔧 All scripts - Improved progress indicators and user feedback

### Removed

#### Cleanup
- 🗑️ Deleted `check_admin.py` - Temporary testing file
- 🗑️ Deleted `app/test_data.py` - Unused test data module
- 🗑️ Removed imports of `test_data` from admin.py and finance_manager.py
- 🗑️ Cleaned up unnecessary Python files

### Fixed

#### Critical Bugs
- 🐛 Fixed password storage (was plain text, now properly hashed)
- 🐛 Fixed password exposure in URL query parameters
- 🐛 Fixed admin users created with empty passwords
- 🐛 Fixed database connection with special characters in password (URL encoding)
- 🐛 Fixed admin login redirect (was going to homepage instead of admin dashboard)

#### Database Issues
- 🐛 Fixed `sub_event` table creation (invalid CHECK constraint)
- 🐛 Fixed table name consistency across SQL and models
- 🐛 Fixed missing columns in transaction_table
- 🐛 Fixed Amount field requirement in transactions

#### Import Errors
- 🐛 Fixed ModuleNotFoundError for test_data module
- 🐛 Removed circular import issues

### Database Schema Changes

#### Tables Modified
- `transaction_table` - Added Sub_Event_ID, modified_date, made Amount default to 0.00
- `Budget` - Changed Total_Budget to Amount, removed calculated columns, added Notes
- `Sub_Event` - Removed invalid budget CHECK constraint

#### Tables Added
- `transactionitem` - Transaction line items with descriptions and amounts
- `Budget` - Event and sub-event budget tracking (was missing)

### Testing

#### Verified Functionality
- ✅ User authentication (login/logout) with hashed passwords
- ✅ Role-based access control (Admin, Event Manager, Finance Manager)
- ✅ Event CRUD operations
- ✅ Transaction creation and viewing
- ✅ Budget management
- ✅ Table search, filter, sort, export features
- ✅ Data visualizations
- ✅ User management (admin functions)
- ✅ Database auto-creation on first run
- ✅ Responsive design on multiple devices

### Performance

#### Optimizations
- ⚡ Client-side table filtering for instant results
- ⚡ Efficient SQLAlchemy queries with proper joins
- ⚡ Lazy loading for relationships
- ⚡ Indexed foreign keys

### Documentation Updates

#### New Files
- `docs/README.md` - Complete project documentation
- `docs/INSTALLATION.md` - Detailed installation guide
- `docs/PROJECT_SUMMARY.md` - Project completion summary
- `README.md` - Updated quick-start guide
- `CHANGELOG.md` - This file

#### Updated Files
- All Python files - Added docstrings and comments
- `requirements.txt` - Verified and updated dependencies

---

## [0.1.0] - Initial Development

### Initial Features
- Basic Flask application structure
- Database models with SQLAlchemy
- User authentication
- Event management
- Transaction tracking
- Basic UI with Bootstrap

---

## Version Naming Convention

- **Major.Minor.Patch** (Semantic Versioning)
- Major: Breaking changes or complete rewrites
- Minor: New features, non-breaking changes
- Patch: Bug fixes and minor improvements

---

## Future Enhancements (Roadmap)

### Planned Features
- [ ] Email notifications
- [ ] PDF report generation
- [ ] Multi-currency support
- [ ] Advanced analytics dashboard
- [ ] Mobile app (Flutter/React Native)
- [ ] REST API for third-party integrations
- [ ] Role permissions customization
- [ ] Audit logging
- [ ] Backup and restore functionality

### Planned Improvements
- [ ] Unit tests and integration tests
- [ ] CI/CD pipeline
- [ ] Docker containerization
- [ ] Load testing and optimization
- [ ] Accessibility improvements (WCAG compliance)
- [ ] Internationalization (i18n)

---

**Last Updated:** December 30, 2025
