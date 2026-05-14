/**
 * Cloudflare Pages Function - Health Check Endpoint
 * Path: /api/hello
 * Purpose: Service health check and basic API validation
 */

export async function onRequest(context) {
  try {
    // Get environment variables
    const env = context.env;
    
    // Check if we have required environment setup
    const backendUrl = env.BACKEND_URL || 'http://localhost:5000';
    
    const response = {
      status: 'ok',
      timestamp: new Date().toISOString(),
      version: '1.0.0',
      service: 'Valtrion API Gateway',
      environment: env.ENVIRONMENT || 'production',
      backend: backendUrl,
      features: {
        cors: true,
        caching: true,
        authentication: true,
        realtime: true
      }
    };

    return new Response(JSON.stringify(response), {
      status: 200,
      headers: {
        'content-type': 'application/json',
        'cache-control': 'public, max-age=60',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      }
    });
  } catch (error) {
    return new Response(JSON.stringify({
      status: 'error',
      message: error.message || 'Internal server error'
    }), {
      status: 500,
      headers: { 'content-type': 'application/json' }
    });
  }
}
