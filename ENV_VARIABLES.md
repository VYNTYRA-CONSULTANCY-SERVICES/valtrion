# Environment Variables Configuration Guide

This guide explains all environment variables used by Valtrion across different deployment platforms.

## Common Variables (All Platforms)

### Flask Configuration
```bash
# Application environment
FLASK_ENV=production|development|testing
# production - Production mode, no debug
# development - Development mode, debug enabled
# testing - Testing mode, in-memory database

# Secret key for session management (REQUIRED)
# Generate with: openssl rand -hex 32
SECRET_KEY=your-secure-secret-key-here
```

### Database Configuration
```bash
# Database URL (auto-configured on some platforms)
# SQLite (local/development):
DATABASE_URL=sqlite:///valtrion.db

# PostgreSQL (production):
DATABASE_URL=postgresql://user:password@host:port/dbname

# MySQL (alternative):
DATABASE_URL=mysql+pymysql://user:password@host:port/dbname

# For Vercel (use /tmp for read-only filesystem):
DATABASE_URL=sqlite:////tmp/valtrion.db
```

## Email Configuration

### Gmail Setup
```bash
# Email address to send from
MAIL_USERNAME=your-email@gmail.com

# Gmail App Password (not your regular password!)
# Steps:
# 1. Enable 2-Step Verification on Gmail
# 2. Go to myaccount.google.com/apppasswords
# 3. Generate app password for Mail
# 4. Use 16-character password
MAIL_PASSWORD=jfqi-bfcm-ywgw-ckgg
```

### Alternative Email Providers
```bash
# SendGrid
MAIL_PROVIDER=sendgrid
SENDGRID_API_KEY=SG.xxxxxxxxxxxxx

# Mailgun
MAIL_PROVIDER=mailgun
MAILGUN_API_KEY=key-xxxxxxxxxxxxx
```

## Payment Gateway

### Razorpay
```bash
# Get from Razorpay Dashboard: https://dashboard.razorpay.com/app/api-keys
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx

# For test mode, use test keys
# For production, use live keys (requires business account)
```

### Alternative Payment Gateways
```bash
# Stripe
STRIPE_API_KEY=sk_live_xxxxxxxxxxxxxxxx
STRIPE_PUBLIC_KEY=pk_live_xxxxxxxxxxxxxxxx

# PayPal
PAYPAL_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxx
PAYPAL_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxx
```

## SMS & Communication

### Twilio (Optional)
```bash
# Get from Twilio Console: https://console.twilio.com/
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE=+1234567890  # Your Twilio phone number

# For SMS notifications
ENABLE_SMS_NOTIFICATIONS=true
```

## Platform-Specific Variables

### Vercel
```bash
# Set in Vercel Dashboard
VERCEL=1
VERCEL_URL=https://valtrion.vercel.app
```

### Heroku
```bash
# Auto-configured
HEROKU_APP_NAME=valtrion
```

### Render
```bash
# Auto-configured
RENDER=true
RENDER_GIT_BRANCH=main
```

### Cloudflare
```bash
# Set in Cloudflare Dashboard
CLOUDFLARE_ACCOUNT_ID=your-account-id
CLOUDFLARE_ZONE_ID=your-zone-id
BACKEND_URL=https://api.valtrion.com
```

### Docker
```bash
# For docker-compose.yml
POSTGRES_USER=valtrion_user
POSTGRES_PASSWORD=secure-password
POSTGRES_DB=valtrion
```

## Logging & Monitoring

```bash
# Log level
LOG_LEVEL=INFO|DEBUG|WARNING|ERROR

# Sentry (error tracking)
SENTRY_DSN=https://xxxxx@sentry.io/1234567

# New Relic (monitoring)
NEW_RELIC_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# CloudWatch (AWS)
AWS_ACCESS_KEY_ID=xxxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxxx
```

## Feature Flags & Configuration

```bash
# Feature toggles
ENABLE_PAYMENTS=true
ENABLE_CHAT=true
ENABLE_REVIEWS=true
ENABLE_SMS_NOTIFICATIONS=false

# API Configuration
API_RATE_LIMIT=100  # Requests per minute
SESSION_TIMEOUT=3600  # Seconds

# CORS Configuration
CORS_ORIGINS=https://app.valtrion.com,https://dashboard.valtrion.com

# WebSocket Configuration
SOCKETIO_CORS_ORIGINS=*
SOCKETIO_ASYNC_MODE=threading
```

## Security Configuration

```bash
# Hashing
BCRYPT_ROUNDS=12  # Password hashing rounds (higher = slower/secure)

# Session
SESSION_COOKIE_SECURE=true  # HTTPS only
SESSION_COOKIE_HTTPONLY=true  # No JavaScript access
SESSION_COOKIE_SAMESITE=Lax  # CSRF protection

# CORS
CORS_ALLOW_CREDENTIALS=true
CORS_MAX_AGE=3600
```

## Platform Comparison

| Variable | Vercel | Heroku | Render | Cloudflare | Docker |
|----------|--------|--------|--------|------------|--------|
| DATABASE_URL | Manual | Auto | Manual | Manual | Manual |
| FLASK_ENV | Manual | Manual | Manual | Manual | Manual |
| SECRET_KEY | Manual | Manual | Manual | Manual | Manual |
| Mail Credentials | Manual | Manual | Manual | Manual | Manual |
| Payment Keys | Manual | Manual | Manual | Manual | Manual |

## Setting Environment Variables

### Vercel
```bash
# Via CLI
vercel env add DATABASE_URL "postgresql://..."

# Via Dashboard
# Settings → Environment Variables → Add
```

### Heroku
```bash
# Via CLI
heroku config:set DATABASE_URL="postgresql://..."

# Via Dashboard
# Settings → Config Vars → Add
```

### Render
```bash
# Via Dashboard
# Settings → Environment → Add Variable
```

### Cloudflare
```bash
# Via Dashboard
# Pages/Workers Settings → Environment Variables
```

### Docker
```bash
# Via .env file
echo "DATABASE_URL=postgresql://..." >> .env

# Via docker-compose.yml
environment:
  DATABASE_URL: postgresql://...
```

## Local Development

### Create .env file
```bash
cp .env.example .env
# Edit .env with your local values
```

### Load environment variables
```bash
# Python automatically loads from .env with python-dotenv
# Or manually:
export $(cat .env | xargs)
```

### Verify variables are loaded
```bash
python -c "import os; print(os.environ.get('SECRET_KEY'))"
```

## Security Best Practices

✅ **DO:**
- Use strong random values for SECRET_KEY
- Store secrets in platform dashboard, not in code
- Use environment-specific values (dev ≠ prod)
- Rotate secrets regularly
- Never commit .env to git
- Use .gitignore to exclude .env

❌ **DON'T:**
- Hardcode secrets in source code
- Commit .env file to repository
- Use same secrets across environments
- Share credentials via email/chat
- Use weak or predictable values
- Log sensitive information

## Variables Checklist

Before deployment, verify you have set:

- [ ] FLASK_ENV
- [ ] SECRET_KEY
- [ ] DATABASE_URL
- [ ] MAIL_USERNAME
- [ ] MAIL_PASSWORD
- [ ] RAZORPAY_KEY_ID
- [ ] RAZORPAY_KEY_SECRET
- [ ] TWILIO_ACCOUNT_SID (if using SMS)
- [ ] TWILIO_AUTH_TOKEN (if using SMS)
- [ ] TWILIO_PHONE (if using SMS)

## Troubleshooting

### "Secret Key not set" Error
- Set SECRET_KEY environment variable
- Generate new key: `openssl rand -hex 32`

### "Database connection error"
- Verify DATABASE_URL format
- Check database is running
- Verify credentials are correct
- Test connection: `psql $DATABASE_URL`

### "Email not sending"
- Verify MAIL_USERNAME and MAIL_PASSWORD
- Check Gmail App Password is correct (16 chars)
- Ensure 2FA is enabled on Gmail
- Check email logs in Gmail security

### "Payment processing fails"
- Verify Razorpay keys are correct
- Check you're using test keys in dev
- Verify business account for live keys

## Migration Between Platforms

When migrating between platforms, ensure you:

1. Copy all environment variables to new platform
2. Update DATABASE_URL if database changed
3. Test email notifications
4. Test payment processing
5. Update domain DNS records
6. Set up backups

---

**Last Updated**: May 14, 2026
**Status**: Production Ready ✅
