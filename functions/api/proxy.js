/**
 * Cloudflare Pages Function - API Proxy
 * Path: /api/proxy
 * Purpose: Proxy requests to backend Flask application
 */

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const backendUrl = env.BACKEND_URL || 'http://localhost:5000';
  
  try {
    // Extract the target path from query parameters or request body
    const targetPath = url.searchParams.get('path') || '/';
    const method = request.method;
    
    // Build backend URL
    const proxyUrl = new URL(targetPath, backendUrl);
    
    // Copy query parameters
    url.searchParams.forEach((value, key) => {
      if (key !== 'path') {
        proxyUrl.searchParams.append(key, value);
      }
    });
    
    // Create proxy request
    const proxyRequest = new Request(proxyUrl.toString(), {
      method: method,
      headers: {
        ...Object.fromEntries(request.headers),
        'X-Forwarded-For': request.headers.get('cf-connecting-ip'),
        'X-Forwarded-Proto': 'https',
        'X-Forwarded-Host': new URL(request.url).host
      },
      body: request.body
    });
    
    // Fetch from backend
    const response = await fetch(proxyRequest);
    
    // Create response with CORS headers
    const responseBody = await response.text();
    
    return new Response(responseBody, {
      status: response.status,
      statusText: response.statusText,
      headers: {
        ...Object.fromEntries(response.headers),
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Cache-Control': 'public, max-age=0'
      }
    });
  } catch (error) {
    return new Response(JSON.stringify({
      error: 'Proxy error',
      message: error.message
    }), {
      status: 503,
      headers: {
        'content-type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });
  }
}
