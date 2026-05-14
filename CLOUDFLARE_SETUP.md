# Cloudflare Pages & Workers Configuration Guide

## Setup Instructions

### Prerequisites
- Cloudflare account with paid plan (for Workers)
- GitHub repository connected to Cloudflare Pages
- `wrangler` CLI installed locally

### Installation

```bash
# Install Wrangler CLI
npm install -g wrangler

# Login to Cloudflare
wrangler login
```

## Cloudflare Pages Setup

### 1. Connect Repository
1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Select **Pages**
3. Click **Create a project** → **Connect to Git**
4. Authorize GitHub and select `valtrion` repository
5. Configure build settings:
   - **Framework**: None (custom)
   - **Build command**: `pip install -r requirements.txt && python seed.py`
   - **Build output directory**: `public`
   - **Root directory**: `/`

### 2. Environment Variables
Add these in Pages Settings → Environment variables:

```
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@host/dbname
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
RAZORPAY_KEY_ID=your-key-id
RAZORPAY_KEY_SECRET=your-key-secret
BACKEND_URL=https://api.valtrion.com
```

### 3. Custom Domain
1. Go to project settings
2. Add custom domain
3. Update DNS records in Cloudflare
4. Enable HTTPS/SSL

## Cloudflare Workers Setup

### 1. Create Worker
```bash
wrangler generate valtrion-worker
cd valtrion-worker
```

### 2. Configure wrangler.toml
Update with your Cloudflare Account ID and Zone ID:
```bash
wrangler whoami  # Get your Account ID
```

### 3. KV Namespace (for caching/sessions)
```bash
# Create KV namespaces
wrangler kv:namespace create "CACHE"
wrangler kv:namespace create "SESSIONS"

# Update wrangler.toml with the IDs
```

### 4. Deploy Worker
```bash
wrangler deploy
```

## Functions

### Available Functions

**Health Check**: `GET /api/hello`
- Returns service status
- No authentication required
- Cached for 60 seconds

**Proxy**: `GET /api/proxy?path=/services`
- Proxies requests to backend
- Forwards all headers
- Includes CORS headers

**Auth Verify**: `POST /api/auth/verify`
- Verifies JWT tokens
- Requires Bearer token
- Returns user data

## Environment Setup

### Local Development
```bash
# Create .env file
cp .env.example .env

# Set Cloudflare-specific variables
CLOUDFLARE_API_TOKEN=your-token
CLOUDFLARE_ACCOUNT_ID=your-account-id
CLOUDFLARE_ZONE_ID=your-zone-id
BACKEND_URL=http://localhost:5000
```

### Production
```bash
# Set environment variables in Cloudflare Dashboard
# Pages Settings → Environment Variables

# Or via CLI
wrangler secret put SECRET_KEY
wrangler secret put DATABASE_URL
```

## Deployment

### Automatic Deployment
Pages automatically deploys on push to main branch:
1. Commit changes to GitHub
2. Push to main branch
3. Pages automatically builds and deploys
4. Check deployment status at [Cloudflare Dashboard](https://dash.cloudflare.com)

### Manual Deployment
```bash
# Deploy Pages
wrangler pages deploy

# Deploy Workers
wrangler deploy
```

## Security

### CORS Headers
All API responses include CORS headers:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

### Authentication
- Tokens verified with backend
- Secrets stored securely in Cloudflare
- No sensitive data in source code

### Rate Limiting
Configure in Cloudflare dashboard:
1. Security → Rate Limiting
2. Create rate limit rule for `/api/*`
3. Set to 100 requests per minute

## Caching Strategy

### KV Cache
```javascript
// Cache API responses
const cacheKey = `api:${request.url}`;
const cachedResponse = await env.CACHE.get(cacheKey);

if (cachedResponse) {
  return new Response(cachedResponse);
}
```

### Cache Headers
```
Cache-Control: public, max-age=3600  // 1 hour
Cache-Control: private, max-age=300  // 5 minutes (auth)
```

## Monitoring

### Cloudflare Analytics
1. Go to Pages Analytics
2. View requests, bandwidth, cache hit rate
3. Set up alerts for errors

### Error Tracking
- Monitor 4xx and 5xx responses
- Check Worker logs: `wrangler tail`
- Review backend logs at deployment platform

## Troubleshooting

### Build Failures
1. Check build logs in Pages settings
2. Verify environment variables are set
3. Test locally: `python run.py`

### 502 Bad Gateway
- Backend service is down
- Check backend status at deployment platform
- Verify `BACKEND_URL` is correct

### CORS Errors
- Ensure API has proper CORS headers
- Check browser console for error details
- Verify proxy function is forwarding headers

### Workers Not Deploying
```bash
# Check configuration
wrangler publish --dry-run

# Verify account ID
wrangler whoami

# Check for errors
wrangler tail
```

## Advanced Configuration

### Custom Headers
```javascript
return new Response(body, {
  headers: {
    'X-Custom-Header': 'value',
    'Strict-Transport-Security': 'max-age=31536000'
  }
});
```

### Request Modification
```javascript
const newRequest = new Request(url, {
  method: 'POST',
  headers: {
    'X-Forwarded-For': request.headers.get('cf-connecting-ip')
  }
});
```

### Error Handling
```javascript
try {
  // Your code
} catch (error) {
  return new Response(JSON.stringify({
    error: error.message
  }), { status: 500 });
}
```

## Performance Optimization

1. **Enable Compression**: Done by default
2. **Minify Assets**: Configure in build
3. **Use Edge Caching**: Set cache headers
4. **Optimize Images**: Use modern formats
5. **Lazy Load**: Load scripts on demand

## API Reference

### Health Check
```bash
curl https://api.valtrion.com/api/hello
```

Response:
```json
{
  "status": "ok",
  "timestamp": "2026-05-14T10:00:00Z",
  "version": "1.0.0",
  "service": "Valtrion API Gateway"
}
```

### Verify Token
```bash
curl -X POST https://api.valtrion.com/api/auth/verify \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Best Practices

1. ✅ Keep secrets in Cloudflare Dashboard
2. ✅ Use environment variables for configuration
3. ✅ Implement proper error handling
4. ✅ Monitor performance metrics
5. ✅ Test locally before deploying
6. ✅ Use KV for session management
7. ✅ Implement rate limiting
8. ✅ Cache appropriately

## Additional Resources

- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)
- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
- [Wrangler CLI Docs](https://developers.cloudflare.com/workers/cli-wrangler/)
- [Cloudflare KV Docs](https://developers.cloudflare.com/workers/runtime-apis/kv/)
