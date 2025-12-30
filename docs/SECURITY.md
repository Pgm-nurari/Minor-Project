# Security Best Practices for FinSight

## Environment Variables

### What is .env?
The `.env` file stores sensitive configuration like database passwords and secret keys. This file should **NEVER** be committed to version control.

### Setup Instructions

1. **Copy the example file:**
   ```bash
   copy .env.example .env
   ```

2. **Edit `.env` with your credentials:**
   ```
   DB_USERNAME=root
   DB_PASSWORD=your_actual_mysql_password
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=finsight_db
   SECRET_KEY=generate_a_long_random_string_here
   ```

3. **Verify .env is in .gitignore:**
   - The `.gitignore` file should contain `.env` (already configured)
   - This prevents accidentally committing secrets to Git

### Generating a Secure SECRET_KEY

Use Python to generate a random secret key:

```python
import secrets
print(secrets.token_hex(32))
```

Or use this one-liner:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## What Changed?

### Before (Insecure ❌)
```python
# app/config.py
db_password = quote_plus('mysql123!@#MYSQL')  # Hardcoded password
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{db_password}@localhost/finsight_db'
```

### After (Secure ✅)
```python
# app/config.py
from dotenv import load_dotenv
load_dotenv()

DB_USERNAME = os.environ.get('DB_USERNAME', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
# ... credentials loaded from .env file
```

## Security Benefits

1. **No Hardcoded Secrets** - Passwords aren't in source code
2. **Environment-Specific** - Different credentials for dev/test/prod
3. **Git-Safe** - `.env` is ignored, `.env.example` is committed as template
4. **Easy Rotation** - Change passwords without modifying code
5. **Team-Friendly** - Each developer uses their own `.env` file

## Production Deployment

For production environments:

1. **Use strong passwords:**
   - Minimum 16 characters
   - Mix of uppercase, lowercase, numbers, symbols
   - No dictionary words

2. **Set environment variables directly:**
   - On Linux: Export in shell or use systemd environment files
   - On Windows: Set in system environment variables
   - On Cloud: Use platform-specific secret managers (AWS Secrets Manager, Azure Key Vault, etc.)

3. **Never commit .env:**
   - Double-check before commits
   - Use `git status` to verify `.env` is not staged

4. **Rotate secrets regularly:**
   - Change database passwords periodically
   - Rotate SECRET_KEY after security incidents

## Files Overview

| File | Purpose | Committed to Git? |
|------|---------|------------------|
| `.env` | Actual secrets (your credentials) | ❌ NO - In .gitignore |
| `.env.example` | Template with placeholders | ✅ YES - Safe to commit |
| `app/config.py` | Reads from environment | ✅ YES - No secrets inside |

## Troubleshooting

### Error: "Access denied for user"
- Check `DB_USERNAME` and `DB_PASSWORD` in `.env`
- Verify MySQL user has correct permissions
- Ensure password doesn't have special characters causing issues

### Error: "No module named 'dotenv'"
- Install python-dotenv: `pip install python-dotenv`
- Already in requirements.txt

### .env not loading
- Ensure `.env` is in the project root directory (same level as `run.py`)
- Check file is named exactly `.env` (not `.env.txt`)
- Verify no spaces around `=` in `.env` file

## Quick Checklist

- [ ] Copied `.env.example` to `.env`
- [ ] Updated database password in `.env`
- [ ] Generated secure SECRET_KEY
- [ ] Verified `.env` is in `.gitignore`
- [ ] Tested application starts successfully
- [ ] Confirmed `.env` is NOT staged in Git

---

**Remember:** Keep your `.env` file secure and never share it publicly! 🔒
