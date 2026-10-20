from http.server import BaseHTTPRequestHandler
import json
import random
import string
url_db = {}
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            long_url = data.get('url')
            if not long_url:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "URL tidak boleh kosong"}).encode('utf-8'))
                return
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            url_db[code] = long_url
            host = self.headers.get('Host', 'localhost')
            short_url = f"https://{host}/api/redirect?code={code}"
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"shortUrl": short_url}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
