#!/usr/bin/env python3
"""
Minimal test server to debug Railway port binding issues
"""
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

class TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        response = f"""Railway Test Server
Port: {os.environ.get('PORT', 'NOT SET')}
Railway Environment: {os.environ.get('RAILWAY_ENVIRONMENT', 'NOT SET')}
Python Version: {sys.version}
Working Directory: {os.getcwd()}
"""
        self.wfile.write(response.encode())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), TestHandler)
    print(f"Starting test server on 0.0.0.0:{port}")
    print(f"PORT environment variable: {os.environ.get('PORT', 'NOT SET')}")
    print(f"RAILWAY_ENVIRONMENT: {os.environ.get('RAILWAY_ENVIRONMENT', 'NOT SET')}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped")
        server.shutdown() 