# Render Deployment Guide

Render is a modern cloud platform for deploying applications. This guide covers deploying Valtrion to Render.

## Prerequisites

- Render account: https://render.com
- GitHub repository (recommended for auto-deploy)
- PostgreSQL database (provided by Render)

## Quick Start

### Option 1: Deploy with GitHub (Recommended)

#### Step 1: Connect GitHub
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New →** **Web Service**
3. Select **Build and deploy from a Git repository**
4. Authenticate with GitHub
5. Select the `valtrion` repository

#### Step 2: Configure Service
1. **Name**: `valtrion`
2. **Environment**: `Python 3.11`
3. **Region**: Choose nearest to your users
4. **Branch**: `main`
5. **Build Command**: 
   ```bash
   pip install -r requirements.txt && python seed.py
   ```
6. **Start Command**: 
   ```bash
   gunicorn -k eventlet -w 1 --bind 0.0.0.0:$PORT wsgi:app
   ```
7. **Plan**: Choose appropriate plan (Starter for development)

#### Step 3: Add Environment Variables
Add these in the Environment section:

```
FLASK_ENV=production
SECRET_KEY=your-secure-secret-key
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
RAZORPAY_KEY_ID=your-key-id
RAZORPAY_KEY_SECRET=your-key-secret
TWILIO_ACCOUNT_SID=(optional)
TWILIO_AUTH_TOKEN=(optional)
TWILIO_PHONE=(optional)
```

#### Step 4: Create Database
1. Go to Render Dashboard
2. Click **New →** **PostgreSQL**
3. **Name**: `valtrion-postgres`
4. **Database**: `valtrion`
5. **User**: `valtrion_user`
6. Click **Create Database**
7. Copy the connection string

#### Step 5: Connect Database
1. Go back to your web service
2. Add environment variable:
   ```
   DATABASE_URL=<paste_connection_string>
   ```
3. Click **Deploy**

#### Step 6: Check Deployment
- Visit your service URL: `https://valtrion.onrender.com`
- Check logs for any errors
- Verify admin login works

### Option 2: Deploy from render.yaml

If you have `render.yaml` configured:

```bash
# Clone repository
git clone https://github.com/NivedithaDevang/valtrion.git
cd valtrion

# Push to trigger deployment
git push
```

## Environment Setup

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `production` |
| `SECRET_KEY` | Flask secret key | Generate with `openssl rand -hex 32` |
| `DATABASE_URL` | PostgreSQL connection | `postgresql://user:pass@host/db` |
| `MAIL_USERNAME` | Gmail address | `your-email@gmail.com` |
| `MAIL_PASSWORD` | Gmail app password | 16-char password |
| `RAZORPAY_KEY_ID` | Razorpay key | From dashboard |
| `RAZORPAY_KEY_SECRET` | Razorpay secret | From dashboard |

### Optional Environment Variables

```
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_PHONE=+1234567890
LOG_LEVEL=INFO
```

## Database Management

### Connect to Database

```bash
# Install PostgreSQL client
apt-get install postgresql-client

# Connect to Render PostgreSQL
psql postgresql://user:password@host/valtrion
```

### Database Backups

1. Go to Database settings on Render
2. Enable **Backups**
3. Backups stored for 7 days (Pro plan: 30 days)

### Restore Database

```bash
# Export current database
pg_dump postgresql://user:pass@host/db > backup.sql

# Restore
psql postgresql://user:pass@host/db < backup.sql
```

## Deployment Updates

### Automatic Deployment
- Push to `main` branch triggers automatic deployment
- Takes ~5-10 minutes
- Check logs during deployment

### Manual Redeployment
1. Go to service settings
2. Click **Manual Deploy**
3. Select branch and click **Deploy**

### Rollback
Render keeps deployment history:
1. Go to **Deployments** tab
2. Select previous deployment
3. Click **Rollback**

## Custom Domain Setup

### Connect Custom Domain

1. Go to service settings
2. Click **Custom Domain**
3. Enter your domain (e.g., `api.valtrion.com`)
4. Add DNS records shown in Render dashboard
5. Wait for SSL certificate (usually instant)

### DNS Records (if using Render nameservers)

Update your registrar to use Render nameservers shown in dashboard.

### DNS Records (if keeping existing registrar)

Add CNAME record:
```
Type: CNAME
Name: api
Value: valtrion.onrender.com
```

## Health Checks

Render automatically monitors your service:

1. **HTTP Health Check**: Queries `/` every 30 seconds
2. **Restart on Failure**: Auto-restarts if health check fails
3. **Custom Health Endpoint**: Optional

### Configure Health Check

In service settings:
- **Health Check Path**: `/`
- **Protocol**: `HTTP`
- **Interval**: `30 seconds`
- **Timeout**: `10 seconds`

## Performance Optimization

### Scaling

1. **Vertical Scaling**: Upgrade plan for more resources
2. **Horizontal Scaling**: Add more instances (Pro+ plans)

### Caching

```python
@app.after_request
def set_cache_headers(response):
    response.headers['Cache-Control'] = 'public, max-age=3600'
    return response
```

### Database Optimization

```python
# Enable connection pooling
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,
    'pool_recycle': 3600,
}
```

## Monitoring & Logs

### View Logs

1. Go to service dashboard
2. Click **Logs** tab
3. View real-time logs
4. Search by date/time

### Download Logs

```bash
# Via Render CLI (if available)
render logs <service-id>
```

### Configure Alerts

1. Go to account settings
2. Set up email notifications for:
   - Service down
   - Build failures
   - High resource usage

## Troubleshooting

### Service Won't Start

1. Check logs for errors
2. Verify environment variables are set
3. Ensure database connection string is correct
4. Check that `wsgi.py` exists

### Database Connection Error

```
Error: could not connect to server: Connection refused
```

**Solution**:
- Verify `DATABASE_URL` is correct
- Check database is running
- Ensure credentials are correct
- Check firewall/network rules

### Out of Memory

**Solutions**:
1. Upgrade to larger plan
2. Enable connection pooling
3. Optimize queries
4. Monitor memory usage

### SSL Certificate Error

1. Wait for certificate generation (usually instant)
2. Check domain DNS setup
3. Verify CNAME records are correct

### Build Failures

**Check**:
1. Build logs for specific error
2. Verify all dependencies in `requirements.txt`
3. Test build locally: `pip install -r requirements.txt`
4. Check Python version compatibility

## Security

### Secrets Management

✅ **DO**:
- Use environment variables for secrets
- Rotate secrets regularly
- Use strong random keys
- Enable database encryption

❌ **DON'T**:
- Commit secrets to git
- Use weak/hardcoded secrets
- Share credentials via email
- Use public databases

### HTTPS/SSL

- Automatically enabled for all services
- Free SSL certificates
- Auto-renewal (before expiration)

### DDoS Protection

Render includes DDoS protection:
- Rate limiting
- IP blocking
- Traffic filtering

## Cost Optimization

### Plans

| Plan | Price | Features |
|------|-------|----------|
| Starter | Free | Limited resources, shared infrastructure |
| Standard | $7/month | Dedicated infrastructure |
| Pro | $25/month | Advanced features, more resources |

### Cost Reduction Tips

1. Use Starter plan for development
2. Combine services (web + database)
3. Enable auto-scaling (Pro+)
4. Optimize database queries
5. Use caching effectively

## Backup & Recovery

### Automatic Backups

PostgreSQL on Render:
- Daily backups (Standard+)
- 7-day retention
- Point-in-time recovery

### Manual Backup

```bash
# Export database
pg_dump postgresql://user:pass@host/db > backup.sql

# Upload to secure storage
aws s3 cp backup.sql s3://my-bucket/valtrion/
```

## API Integration

### Webhook for Deployments

```bash
# Get webhook URL from Render dashboard
# Trigger deployment from CI/CD:
curl -X POST https://api.render.com/deploy/{service-id}?key={key}
```

## Useful Commands

```bash
# SSH into service (available with pro plan)
render ssh <service-id>

# View environment variables
render env list <service-id>

# Set environment variable
render env set <service-id> KEY=VALUE
```

## Support

- **Render Support**: https://render.com/support
- **Documentation**: https://render.com/docs
- **Status Page**: https://status.render.com
- **Community**: https://forum.render.com

## Migration from Other Platforms

### From Heroku

1. Export database
2. Create new PostgreSQL on Render
3. Import database
4. Set environment variables
5. Deploy application

### From Vercel

Render is better for long-running processes:
1. Deploy web service to Render
2. Database to Render PostgreSQL
3. Frontend can stay on Vercel

## Next Steps

1. ✅ Deploy to Render
2. ✅ Set up custom domain
3. ✅ Configure monitoring
4. ✅ Set up backups
5. ✅ Enable auto-deploy
6. ✅ Test all functionality
7. ✅ Update DNS records
8. ✅ Monitor performance

---

**Last Updated**: May 14, 2026
**Status**: Ready for Production ✅
