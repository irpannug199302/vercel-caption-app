from http.server import BaseHTTPRequestHandler
import json
import random
import string
import os
DB_FILE = "/tmp/urls.json"
def get_urls():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}
def save_urls(urls):
    try:
        with open(DB_FILE, "w") as f:
            json.dump(urls, f)
    except Exception:
        pass
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
            urls = get_urls()
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            urls[code] = long_url
            save_urls(urls)
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
