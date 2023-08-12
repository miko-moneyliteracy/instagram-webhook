import http.server
import socketserver
import json

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/miko-moneyliteracy.com/instagram-webhook':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # ここにコールバックの処理を記述します
            # dataには受信したJSONデータが含まれています
            print("Webhook callback received:", data)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Webhook callback received')
            return
    
    # do_GET メソッドをオーバーライドしてカスタムな処理を記述
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'GET request received')
        return

PORT = 8000

with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()