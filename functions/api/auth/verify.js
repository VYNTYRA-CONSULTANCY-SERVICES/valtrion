/**
 * Cloudflare Pages Function - Authentication Middleware
 * Path: /api/auth/verify
 * Purpose: Verify JWT tokens and manage sessions
 */

export async function onRequest(context) {
  const { request, env } = context;
  
  try {
    // Get authorization header
    const authHeader = request.headers.get('Authorization');
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return new Response(JSON.stringify({
        authenticated: false,
        message: 'Missing or invalid authorization header'
      }), {
        status: 401,
        headers: { 'content-type': 'application/json' }
      });
    }
    
    const token = authHeader.substring(7);
    
    // Verify token with backend
    const backendUrl = env.BACKEND_URL || 'http://localhost:5000';
    const verifyResponse = await fetch(`${backendUrl}/api/auth/verify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!verifyResponse.ok) {
      return new Response(JSON.stringify({
        authenticated: false,
        message: 'Invalid token'
      }), {
        status: 401,
        headers: { 'content-type': 'application/json' }
      });
    }
    
    const userData = await verifyResponse.json();
    
    return new Response(JSON.stringify({
      authenticated: true,
      user: userData,
      timestamp: new Date().toISOString()
    }), {
      status: 200,
      headers: {
        'content-type': 'application/json',
        'cache-control': 'private, max-age=300'
      }
    });
  } catch (error) {
    return new Response(JSON.stringify({
      authenticated: false,
      error: error.message
    }), {
      status: 500,
      headers: { 'content-type': 'application/json' }
    });
  }
}
