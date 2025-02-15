from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import sys
import datetime

class DetailedRequestHandler(BaseHTTPRequestHandler):
    def log_request_details(self):
        # Get current timestamp
        timestamp = datetime.datetime.now().isoformat()
        
        # Parse URL and query parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Get request body if present
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b''
        
        # Compile request details
        request_details = {
            "timestamp": timestamp,
            "basic_info": {
                "request_version": self.request_version,
                "command": self.command,
                "path": self.path,
                "client_address": self.client_address[0],
                "client_port": self.client_address[1],
                "server_address": self.server.server_address[0],
                "server_port": self.server.server_address[1]
            },
            "parsed_url": {
                "scheme": parsed_url.scheme,
                "netloc": parsed_url.netloc,
                "path": parsed_url.path,
                "params": parsed_url.params,
                "query": parsed_url.query,
                "fragment": parsed_url.fragment
            },
            "query_parameters": query_params,
            "headers": dict(self.headers),
            "body": body.decode('utf-8') if body else None
        }
        
        # Print details in a formatted way
        print("\n=== New Request ===")
        print(json.dumps(request_details, indent=2))
        return request_details

    def do_GET(self):
        details = self.log_request_details()
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(details, indent=2).encode())

    def do_POST(self):
        details = self.log_request_details()
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(details, indent=2).encode())

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, DetailedRequestHandler)
    print(f"Server running on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()
        sys.exit(0)

if __name__ == '__main__':
    run_server()