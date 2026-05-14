# Quick Reference - Deployment Commands

Fast lookup for deployment commands across all platforms.

## 🚀 Quick Deploy Commands

### Render (Recommended for Beginners)
```bash
# Setup
git push origin main
# That's it! Render auto-deploys

# Watch deployment
# Go to: https://dashboard.render.com/

# View logs
# Render Dashboard → Service → Logs
```

### Vercel
```bash
# Install CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod

# View logs
vercel logs
```

### Heroku
```bash
# Install CLI
# Windows: Download from https://devcenter.heroku.com/articles/heroku-cli
# macOS: brew install heroku

# Login
heroku login

# Create app
heroku create my-valtrion-app

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku main

# Initialize DB
heroku run python seed.py

# View logs
heroku logs --tail
```

### Cloudflare
```bash
# Install Wrangler
npm install -g @cloudflare/wrangler

# Login
wrangler login

# Deploy Workers
wrangler deploy

# View logs
wrangler tail

# Deploy Pages (GitHub integration)
# GitHub → Cloudflare Pages → Connect repo
```

### Docker (Local/VPS)
```bash
# Build image
docker build -t valtrion .

# Run locally
docker run -p 5000:5000 valtrion

# Docker Compose
docker-compose up -d

# View logs
docker logs -f valtrion

# Stop
docker stop valtrion
```

---

## 🔐 Environment Variables Setup

### Set Environment Variables - All Platforms

**Get these values first:**
```bash
# Generate SECRET_KEY
openssl rand -hex 32

# Gmail App Password: https://myaccount.google.com/apppasswords

# Razorpay keys: https://dashboard.razorpay.com/app/api-keys
```

### Render
```bash
# Go to: Render Dashboard → Service Settings → Environment
# Add:
FLASK_ENV=production
SECRET_KEY=your-generated-key
DATABASE_URL=auto-set
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-password
RAZORPAY_KEY_ID=your-key
RAZORPAY_KEY_SECRET=your-secret
```

### Vercel
```bash
# Via CLI
vercel env add FLASK_ENV production
vercel env add SECRET_KEY "your-key"
vercel env add MAIL_USERNAME "your-email@gmail.com"
vercel env add MAIL_PASSWORD "your-app-password"
vercel env add RAZORPAY_KEY_ID "your-key"
vercel env add RAZORPAY_KEY_SECRET "your-secret"

# Or via Dashboard: Settings → Environment Variables
```

### Heroku
```bash
# Via CLI
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY="your-key"
heroku config:set MAIL_USERNAME="your-email@gmail.com"
heroku config:set MAIL_PASSWORD="your-app-password"
heroku config:set RAZORPAY_KEY_ID="your-key"
heroku config:set RAZORPAY_KEY_SECRET="your-secret"

# Verify
heroku config
```

### Cloudflare
```bash
# Via Dashboard: Pages/Workers → Settings → Environment Variables
# Add all variables via UI

# Or with secret values
wrangler secret put SECRET_KEY
wrangler secret put MAIL_PASSWORD
```

### Docker
```bash
# Create .env file
echo "FLASK_ENV=production" > .env
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env
echo "MAIL_USERNAME=your-email@gmail.com" >> .env
# ... add all other variables

# Or use docker-compose.yml
# environment:
#   FLASK_ENV: production
#   SECRET_KEY: your-key
```

---

## 📊 Database Setup

### Render
```bash
# PostgreSQL auto-created
# Just add DATABASE_URL to environment
# Done!
```

### Heroku
```bash
# Create PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Initialize database
heroku run python seed.py

# Check DB
heroku pg:info
```

### Vercel (External Database Required)
```bash
# Use PostgreSQL from another service
# Or use external service: Supabase, PlanetScale, etc.

# Set DATABASE_URL
vercel env add DATABASE_URL "postgresql://..."
```

### Cloudflare (External Database Required)
```bash
# Use external PostgreSQL service
# Vercel Postgres, Supabase, AWS RDS, etc.

# Set DATABASE_URL in environment
```

### Docker
```bash
# Using docker-compose (includes PostgreSQL)
docker-compose up -d

# Database initialized automatically
# Access at: postgresql://valtrion_user:valtrion_password@postgres:5432/valtrion
```

---

## 🔍 Verify Deployment

### Health Check (All Platforms)
```bash
# Test if service is running
curl https://your-domain.com/api/hello
# or
curl http://localhost:5000/

# Expected response:
# { "status": "ok", "version": "1.0.0" }
```

### Admin Login (All Platforms)
1. Go to: `https://your-domain.com`
2. Click "Login"
3. Email: `valtrionbookings@gmail.com`
4. Password: `valtrion@123`
5. ✅ If successful, deployment works

### Database Check
```bash
# Local/Docker
python -c "from app import db; print('DB OK')"

# Heroku
heroku run python -c "from app import db; print('DB OK')"

# Render
# Check in dashboard logs
```

---

## 🐛 Common Commands for Debugging

### View Logs

**Render**
```bash
# Dashboard → Logs tab
# Or scroll in dashboard
```

**Vercel**
```bash
vercel logs
vercel logs --tail
```

**Heroku**
```bash
heroku logs
heroku logs --tail
heroku logs -n 100  # Last 100 lines
```

**Cloudflare**
```bash
wrangler tail
```

**Docker**
```bash
docker logs valtrion
docker logs -f valtrion  # Follow logs
docker logs --tail 100 valtrion
```

### Database Queries

```bash
# Local/Docker PostgreSQL
psql postgresql://valtrion_user:password@host/valtrion

# View users
SELECT id, email, role FROM user;

# Check bookings
SELECT id, status, payment_status FROM booking;
```

### SSH Into Service

**Heroku** (available with paid plans)
```bash
heroku ps:exec
```

**Render**
```bash
# SSH available in Pro plan via dashboard
```

**Docker**
```bash
docker exec -it valtrion bash
```

---

## 🔄 Update & Redeploy

### Update Code (All Platforms Using Git)
```bash
# Make changes
git add .
git commit -m "Update message"
git push origin main

# Vercel, Render, Heroku auto-deploy
```

### Manual Redeployment

**Vercel**
```bash
vercel --prod
```

**Heroku**
```bash
git push heroku main
# Or trigger via GitHub if integrated
```

**Render**
```bash
# Automatic on git push
# Manual: Dashboard → Deployments → Redeploy
```

**Cloudflare**
```bash
wrangler deploy
```

**Docker**
```bash
docker build -t valtrion .
docker stop valtrion
docker run -p 5000:5000 valtrion
```

---

## 🔐 Update Secrets

### Change Environment Variables

**Render**
```bash
# Dashboard → Settings → Environment → Update value
```

**Vercel**
```bash
# Via CLI
vercel env add SECRET_KEY "new-value"
vercel redeploy

# Or via Dashboard: Settings → Environment Variables
```

**Heroku**
```bash
# Via CLI
heroku config:set SECRET_KEY="new-value"
# Automatically redeploys

# Or via Dashboard: Settings → Config Vars
```

**Cloudflare**
```bash
wrangler secret put SECRET_KEY
# Follow prompts
wrangler deploy
```

**Docker**
```bash
# Update .env file
# Restart container
docker restart valtrion
```

---

## 📊 Monitoring & Performance

### Check Performance

**Render**
```bash
# Dashboard → Metrics tab
```

**Vercel**
```bash
# Dashboard → Analytics
# Shows: Requests, Response time, etc.
```

**Heroku**
```bash
# Dashboard → Metrics
# Shows: Response time, Throughput, etc.
```

**Cloudflare**
```bash
# Dashboard → Analytics
# Shows: Requests, Cache hit rate, etc.
```

### Monitor Errors

**All Platforms**
- View logs regularly
- Set up alerts/notifications
- Monitor error rates
- Check application health endpoint

---

## 🗑️ Delete/Clean Up

### Remove Deployment

**Render**
```bash
# Dashboard → Service → Settings → Delete Service
```

**Vercel**
```bash
vercel remove
```

**Heroku**
```bash
heroku destroy
```

**Cloudflare**
```bash
wrangler delete
```

**Docker**
```bash
docker stop valtrion
docker rm valtrion
docker rmi valtrion
```

---

## 📋 Pre-Deployment Checklist

Before deploying to production:

```bash
# ✅ 1. Test locally
python run.py
# Visit http://localhost:5000

# ✅ 2. Run tests
pytest

# ✅ 3. Build Docker image
docker build -t valtrion .

# ✅ 4. Check configuration
cat .env.example

# ✅ 5. Verify requirements
pip install -r requirements.txt

# ✅ 6. Initialize database
python seed.py

# ✅ 7. Check git status
git status
git log -1

# ✅ 8. Commit changes
git add .
git commit -m "Deployment ready"

# ✅ 9. Push to repository
git push origin main

# ✅ 10. Monitor deployment
# Check platform dashboard
```

---

## 🆘 Emergency Commands

### Rollback Deployment

**Vercel**
```bash
# Dashboard → Deployments → Select previous → Redeploy
```

**Heroku**
```bash
heroku releases
heroku rollback v123
```

**Render**
```bash
# Dashboard → Deployments → Select previous → Redeploy
```

### Emergency Stop

```bash
# Render: Dashboard → Suspend
# Vercel: Disable automatic deployments
# Heroku: Scale dynos to 0
# Cloudflare: Disable Workers
# Docker: docker stop
```

### Database Emergency Restore

```bash
# From backup
pg_restore -d valtrion backup.dump

# Or from export
psql -d valtrion < backup.sql
```

---

## 🌐 Domain & DNS Setup

### Point Domain to Platform

**Render/Vercel/Heroku**
```bash
# Add CNAME record:
# Type: CNAME
# Name: subdomain (or @ for root)
# Value: platform-domain.com

# Wait 24-48 hours for propagation
```

**Cloudflare**
```bash
# Use Cloudflare nameservers from platform
# Or add CNAME record
```

### Verify DNS
```bash
# Check DNS propagation
nslookup api.valtrion.com
dig api.valtrion.com

# Ping to verify
ping api.valtrion.com
```

---

## 💡 Pro Tips

1. **Always test locally first**: `python run.py`
2. **Use environment variables**: Never hardcode secrets
3. **Keep secrets secure**: Use platform secret management
4. **Monitor logs**: Check logs after each deployment
5. **Automate deployments**: Use CI/CD workflows
6. **Regular backups**: Export database monthly
7. **Document changes**: Commit with meaningful messages
8. **Use staging environment**: Test on staging before production
9. **Have rollback plan**: Know how to revert quickly
10. **Monitor performance**: Set up alerts and monitoring

---

**Last Updated**: May 14, 2026
**Status**: Production Ready ✅

Use this as quick reference for daily deployment tasks!
