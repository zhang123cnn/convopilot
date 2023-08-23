from http.server import HTTPServer, SimpleHTTPRequestHandler

def run_server():
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Server is running on port 3000...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()