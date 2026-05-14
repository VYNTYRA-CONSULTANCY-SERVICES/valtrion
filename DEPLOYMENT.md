# Valtrion Car Services - Deployment Guide

## 📚 Quick Navigation

- **[Platform Comparison](PLATFORM_COMPARISON.md)** - Choose the right platform
- **[Environment Variables](ENV_VARIABLES.md)** - Configure secrets and settings
- **[Cloudflare Setup](CLOUDFLARE_SETUP.md)** - Deploy with Cloudflare Pages/Workers
- **[Render Setup](RENDER_SETUP.md)** - Deploy with Render
- **[GitHub Actions Workflows](.github/workflows)** - CI/CD automation

## Overview
Valtrion is a Flask-based car service booking application. This guide covers deployment to multiple cloud platforms: Vercel, Heroku, Render, Cloudflare, and Docker.

**Choose your platform:**
- **Vercel** - Serverless, great for APIs
- **Heroku** - Traditional PaaS, PostgreSQL included
- **Render** - Modern PaaS, affordable alternative to Heroku
- **Cloudflare** - Edge computing, global distribution
- **Docker** - Self-hosted, full control

## Prerequisites
- Python 3.11+
- pip package manager
- Git
- Vercel CLI (for Vercel deployment) or Heroku CLI (for Heroku deployment)
- Valid credentials for third-party services (Gmail, Razorpay, etc.)

## Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/NivedithaDevang/valtrion.git
cd valtrion
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

Edit `.env` with your actual values:
- `SECRET_KEY`: Generate a strong random key (e.g., `openssl rand -hex 32`)
- `MAIL_USERNAME`: Your Gmail email address
- `MAIL_PASSWORD`: Gmail App Password (16-character)
- `RAZORPAY_KEY_ID` & `RAZORPAY_KEY_SECRET`: From Razorpay dashboard
- `DATABASE_URL`: Leave default for SQLite or set PostgreSQL URL for production

### 5. Initialize Database
```bash
python seed.py
```

This will:
- Create database tables
- Seed services data
- Create default admin account

### 6. Run Locally
```bash
python run.py
```

Access the application at `http://localhost:5000`

**Default Admin Credentials:**
- Email: `valtrionbookings@gmail.com`
- Password: `valtrion@123`

## Environment Variables Setup

### Gmail Configuration
1. Enable 2-Step Verification on your Gmail account
2. Go to [Google Account Security](https://myaccount.google.com/security)
3. Navigate to **App Passwords** (appears only with 2FA enabled)
4. Select "Mail" and "Other (custom name)"
5. Copy the 16-character password to `MAIL_PASSWORD` in `.env`

### Razorpay Setup
1. Sign up at [Razorpay Dashboard](https://dashboard.razorpay.com)
2. Navigate to Settings → API Keys
3. Copy Key ID and Key Secret
4. For testing, use the test keys provided

### Twilio Setup (Optional)
1. Sign up at [Twilio Console](https://console.twilio.com)
2. Get Account SID and Auth Token
3. Get or buy a Twilio phone number

## Deployment to Vercel

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy
```bash
vercel
```

### 4. Set Environment Variables in Vercel Dashboard
1. Go to your project settings
2. Navigate to Environment Variables
3. Add all variables from `.env`:
   - `SECRET_KEY`
   - `MAIL_USERNAME`
   - `MAIL_PASSWORD`
   - `RAZORPAY_KEY_ID`
   - `RAZORPAY_KEY_SECRET`
   - `DATABASE_URL` (optional, defaults to SQLite in /tmp)
   - `FLASK_ENV=production`

### 5. Deploy Again
```bash
vercel --prod
```

## Deployment to Heroku

### 1. Install Heroku CLI
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows (download from https://devcenter.heroku.com/articles/heroku-cli)
```

### 2. Login to Heroku
```bash
heroku login
```

### 3. Create Heroku App
```bash
heroku create your-app-name
```

### 4. Set Environment Variables
```bash
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set MAIL_USERNAME="your-email@gmail.com"
heroku config:set MAIL_PASSWORD="your-app-password"
heroku config:set RAZORPAY_KEY_ID="your-key-id"
heroku config:set RAZORPAY_KEY_SECRET="your-key-secret"
heroku config:set FLASK_ENV="production"
```

### 5. Add PostgreSQL Database (Recommended)
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

This automatically sets `DATABASE_URL` environment variable.

### 6. Deploy
```bash
git push heroku main
```

### 7. Initialize Database
```bash
heroku run python seed.py
```

## Production Checklist

- [ ] `SECRET_KEY` is set and secure (never commit to git)
- [ ] `FLASK_ENV` is set to `production`
- [ ] Database is set up (SQLite or PostgreSQL)
- [ ] All API keys (Razorpay, Gmail) are configured
- [ ] CORS settings are configured correctly
- [ ] Static files are being served correctly
- [ ] Email notifications are working
- [ ] Payment processing is tested
- [ ] Error logging is configured
- [ ] HTTPS is enabled

## Database Options

### SQLite (Default)
- **Pros:** Simple, no setup required
- **Cons:** Not suitable for high-traffic, not ideal for distributed systems
- **Use case:** Development, small projects

### PostgreSQL (Recommended for Production)
- **Pros:** Scalable, reliable, industry-standard
- **Cons:** Requires setup and maintenance
- **Use case:** Production deployments

## Static Files & Templates

The application serves:
- **Templates:** From `app/templates/` directory
- **Static files:** From `app/static/` directory (CSS, JS, images)
- **Logos:** From `app/static/logos/`
- **Offers:** From `app/static/offers/`

In production, ensure these are properly served by the web server.

## Troubleshooting

### Database Connection Error
- Ensure `DATABASE_URL` is correctly formatted
- For PostgreSQL: `postgresql://user:password@host:port/dbname`
- Check database credentials and network access

### Email Not Sending
- Verify Gmail App Password (not regular password)
- Ensure 2FA is enabled on Gmail account
- Check `MAIL_USERNAME` and `MAIL_PASSWORD` are correct
- Look for gmail logs at https://myaccount.google.com/security

### SocketIO Connection Issues
- Ensure WebSocket support is enabled on your platform
- Check `SOCKETIO_CORS_ORIGINS` settings
- Verify reverse proxy (nginx) properly forwards WebSocket headers

### Static Files Not Loading
- Check that static file paths are correct
- Ensure `app/static/` folder exists and contains files
- Verify web server (gunicorn) has permission to read static folder

### "Secret Key Not Set" Error
- Ensure `SECRET_KEY` environment variable is set
- Never leave `SECRET_KEY` empty in production
- Generate secure key: `openssl rand -hex 32`

## Deployment Platforms

### Complete Guides for All Platforms

#### 1. **Render** (Recommended for beginners)
👉 **[See Full Render Deployment Guide](RENDER_SETUP.md)**

- Modern PaaS platform
- Built-in PostgreSQL ($7/month)
- Auto-deploy from GitHub
- [render.yaml](render.yaml) configuration included

```bash
# Just push to GitHub!
git push origin main
# Render auto-deploys
```

#### 2. **Cloudflare Pages & Workers**
👉 **[See Full Cloudflare Setup Guide](CLOUDFLARE_SETUP.md)**

- Edge computing network
- Global distribution
- Free tier available
- [wrangler.toml](wrangler.toml) configuration included

```bash
# Deploy Workers
wrangler deploy

# Deploy Pages
wrangler pages deploy
```

#### 3. **Vercel** (Serverless)
This document includes Vercel deployment steps above.

- Serverless functions
- Free tier available
- Great for APIs
- [vercel.json](vercel.json) configuration included

```bash
vercel --prod
```

#### 4. **Heroku** (Traditional PaaS)
This document includes Heroku deployment steps above.

- Classic PaaS experience
- PostgreSQL included
- Proven reliability
- [Procfile](Procfile) included

```bash
git push heroku main
```

#### 5. **Docker** (Self-hosted)
See Docker section below in this document.

- Full control
- Works anywhere
- [Dockerfile](Dockerfile) and [docker-compose.yml](docker-compose.yml) included

```bash
docker build -t valtrion .
docker run -p 5000:5000 valtrion
```

## Platform Comparison

👉 **[See Detailed Platform Comparison](PLATFORM_COMPARISON.md)**

Quick decision table:

| Platform | Cost | Best For | Setup Time |
|----------|------|----------|-----------|
| Render | $7/month | Full-stack apps | 5 min |
| Cloudflare | Free-$20 | APIs, CDN | 20 min |
| Vercel | Free-$50 | Serverless APIs | 5 min |
| Heroku | $7/month | Production apps | 10 min |
| Docker | $5-100 | Enterprise | 30 min |

## Environment Variables Configuration

👉 **[See Complete Environment Variables Guide](ENV_VARIABLES.md)**

All platforms require environment variables. See the guide for:
- Complete list of all variables
- Platform-specific configuration
- Security best practices
- Troubleshooting

## CI/CD with GitHub Actions

Automated testing and deployment workflows:

- **[tests.yml](.github/workflows/tests.yml)** - Run tests on every push
- **[deploy-render.yml](.github/workflows/deploy-render.yml)** - Auto-deploy to Render
- **[deploy-vercel.yml](.github/workflows/deploy-vercel.yml)** - Auto-deploy to Vercel
- **[deploy-cloudflare.yml](.github/workflows/deploy-cloudflare.yml)** - Auto-deploy to Cloudflare

### Enable GitHub Actions

1. Add repository secrets in GitHub Settings:
   ```
   VERCEL_TOKEN
   RENDER_API_KEY
   CLOUDFLARE_API_TOKEN
   ```

2. Workflows automatically run on push to main

## Monitoring & Logging

### Vercel Logs
```bash
vercel logs
```

### Heroku Logs
```bash
heroku logs --tail
```

### Render Logs
Check logs in Render dashboard

### Cloudflare Logs
```bash
wrangler tail
```

### Docker Logs
```bash
docker logs -f container-name
```

## Maintenance

### Database Backups
- For SQLite: Regular file backups
- For PostgreSQL: Use `pg_dump` or platform backup tools

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Security Updates
Regularly update Flask and dependencies:
```bash
pip list --outdated
pip install --upgrade [package-name]
```

## Troubleshooting by Platform

### Render Issues
👉 See [Render Troubleshooting](RENDER_SETUP.md#troubleshooting)

### Cloudflare Issues
👉 See [Cloudflare Troubleshooting](CLOUDFLARE_SETUP.md#troubleshooting)

### General Issues
See troubleshooting section earlier in this document

## Migration Between Platforms

If you need to move from one platform to another:

1. **Export your database**
2. **Update environment variables**
3. **Deploy to new platform**
4. **Import database**
5. **Test thoroughly**
6. **Update DNS records**
7. **Keep old platform running during transition** (if public)

See [Platform Comparison](PLATFORM_COMPARISON.md#migration-between-platforms) for specific steps.

## Support & Issues

For platform-specific help:

1. **Render Issues**
   - Check [Render Status Page](https://status.render.com)
   - Visit [Render Support](https://render.com/support)
   - Check [Render Docs](https://render.com/docs)

2. **Cloudflare Issues**
   - Check [Cloudflare Status](https://www.cloudflarestatus.com)
   - Visit [Cloudflare Support](https://support.cloudflare.com)
   - Check [Cloudflare Docs](https://developers.cloudflare.com)

3. **Vercel Issues**
   - Check [Vercel Status](https://www.vercel-status.com)
   - Visit [Vercel Support](https://vercel.com/support)
   - Check [Vercel Docs](https://vercel.com/docs)

4. **Heroku Issues**
   - Check [Heroku Status](https://www.heroku.com/status)
   - Visit [Heroku Support](https://help.heroku.com)
   - Check [Heroku Docs](https://devcenter.heroku.com)

5. **General Issues**
   - Review application logs
   - Check [GitHub Issues](https://github.com/NivedithaDevang/valtrion/issues)
   - Review this documentation

## Additional Resources

### Documentation
- [Main README](README.md)
- [Environment Variables Guide](ENV_VARIABLES.md)
- [Platform Comparison](PLATFORM_COMPARISON.md)
- [Render Setup](RENDER_SETUP.md)
- [Cloudflare Setup](CLOUDFLARE_SETUP.md)

### Official Docs
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy Docs](https://flask-sqlalchemy.palletsprojects.com/)
- [Render Docs](https://render.com/docs)
- [Cloudflare Docs](https://developers.cloudflare.com)
- [Vercel Docs](https://vercel.com/docs)
- [Heroku Docs](https://devcenter.heroku.com)
- [Docker Docs](https://docs.docker.com)

### Configuration Files
- [.env.example](.env.example) - Environment template
- [vercel.json](vercel.json) - Vercel configuration
- [Procfile](Procfile) - Heroku/traditional server configuration
- [Dockerfile](Dockerfile) - Docker container definition
- [docker-compose.yml](docker-compose.yml) - Docker Compose configuration
- [render.yaml](render.yaml) - Render configuration
- [wrangler.toml](wrangler.toml) - Cloudflare configuration

---

**Last Updated**: May 14, 2026
**Status**: Production Ready ✅

**All platforms configured and tested. Choose the one that best fits your needs!**
