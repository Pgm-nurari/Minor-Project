# Authentication Quick Reference

## How the Authentication System Works

### User Login Flow
1. User visits `/login`
2. Enters email and password
3. System validates credentials against database
4. If valid, creates session with user info
5. Redirects to appropriate dashboard based on role

### Session Data Stored
```python
session['user_id']     # User ID from database
session['username']    # User's full name
session['email']       # User's email
session['role']        # User's role (Admin, Event Manager, Finance Manager)
```

### Logout Flow
1. User visits `/logout`
2. Session is cleared
3. User is redirected to login page

## Protected Routes

### Admin Routes (`/admin/*`)
- **Required:** Admin role
- **Enforced by:** `@admin_bp.before_request` in admin.py
- **Redirect:** Login page if not authenticated, home page if wrong role

### Event Manager Routes (`/evemng/<user_id>/*`)
- **Required:** Event Manager or Admin role
- **Enforced by:** `@event_manager_bp.before_request` in event_manager.py
- **Redirect:** Login page if not authenticated, home page if wrong role

### Finance Manager Routes (`/finmng/<user_id>/*`)
- **Required:** Finance Manager or Admin role
- **Enforced by:** `@finance_manager_bp.before_request` in finance_manager.py
- **Redirect:** Login page if not authenticated, home page if wrong role

## Using Authentication Decorators

### Method 1: Blueprint-wide Protection (Current Implementation)
```python
@admin_bp.before_request
def check_admin_access():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('home.login'))
    
    if session.get('role') != 'Admin':
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('home.index'))
```

### Method 2: Individual Route Protection
```python
from app.auth import login_required, role_required

@app.route('/some-route')
@login_required
def some_route():
    # User must be logged in
    pass

@app.route('/admin-only')
@role_required('Admin')
def admin_only():
    # User must have Admin role
    pass

@app.route('/multiple-roles')
@role_required('Admin', 'Event Manager')
def multiple_roles():
    # User must have Admin OR Event Manager role
    pass
```

### Getting Current User
```python
from app.auth import get_current_user

@app.route('/profile')
@login_required
def profile():
    current_user = get_current_user()
    return render_template('profile.html', user=current_user)
```

## Testing Authentication

### Test 1: Unauthenticated Access
```bash
# Should redirect to login
curl -I http://localhost:5000/admin/
# Expected: 302 redirect to /login
```

### Test 2: Valid Login
```bash
# Login with valid credentials
curl -X POST http://localhost:5000/login \
  -d "email=admin@finsight.com" \
  -d "password=Password@123" \
  -c cookies.txt

# Access admin page with session cookie
curl -b cookies.txt http://localhost:5000/admin/
# Expected: 200 OK with admin dashboard
```

### Test 3: Wrong Role Access
```bash
# Login as Event Manager
curl -X POST http://localhost:5000/login \
  -d "email=eventmanager@example.com" \
  -d "password=ValidPassword123!" \
  -c cookies.txt

# Try to access admin page
curl -b cookies.txt http://localhost:5000/admin/
# Expected: 302 redirect with permission denied message
```

### Test 4: Logout
```bash
# Logout
curl -b cookies.txt http://localhost:5000/logout
# Expected: 302 redirect to /login

# Try to access protected page
curl -b cookies.txt http://localhost:5000/admin/
# Expected: 302 redirect to /login (session cleared)
```

## Common Issues & Solutions

### Issue: "Please log in to access this page"
**Cause:** No active session
**Solution:** User needs to login at `/login`

### Issue: "You do not have permission to access this page"
**Cause:** User is logged in but lacks required role
**Solution:** Contact admin to update role, or login with correct account

### Issue: Session expires too quickly
**Cause:** `PERMANENT_SESSION_LIFETIME` too short
**Solution:** Update in config.py or .env file

### Issue: Users can't stay logged in
**Cause:** `session.permanent` not set
**Solution:** Already implemented in login route (line 57 of home.py)

## Security Best Practices

1. **Always check authentication before sensitive operations**
2. **Use HTTPS in production** to protect session cookies
3. **Set strong SECRET_KEY** in production (use `secrets.token_hex(32)`)
4. **Implement CSRF protection** for form submissions
5. **Add rate limiting** on login endpoint
6. **Log all authentication events** for audit trail
7. **Implement session timeout** warnings for users
8. **Clear sessions on password change**

## Environment Variables

Add to `.env`:
```bash
SECRET_KEY=<use secrets.token_hex(32) to generate>
PERMANENT_SESSION_LIFETIME=3600  # 1 hour
```

## Future Enhancements

- [ ] Add "Remember Me" functionality
- [ ] Implement password reset tokens with expiry
- [ ] Add multi-factor authentication (MFA)
- [ ] Implement account lockout after failed attempts
- [ ] Add session activity logging
- [ ] Implement CSRF tokens on all forms
- [ ] Add API token authentication for API endpoints
