import http.server
import socketserver
import json
import os
from urllib.parse import parse_qs

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == os.environ.get('MIKO_PATH') :
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # InstaglamからのWebhook通知を受け取り、必要な処理を行う
            if 'comment' in data:
                comment_text = data['comment']['text']
                user_id = data['comment']['user_id']

                # 自動返信の処理を実装（ここでは簡単な例を示す）
                if 'おはよう' in comment_text:
                    reply_text = f'@{user_id} おはようございます！'
                    self.send_instaglam_reply(reply_text)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Webhook callback received')
            return
        else:
            super().do_GET()

    def send_instaglam_reply(self, text):
        # Instaglam APIを使用してコメントに返信を送信する処理を実装
        # Instaglam APIのコードをここに記述する
        pass

PORT = 8000

with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
