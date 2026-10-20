from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
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
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        code = query.get('code', [None])[0]
        urls = get_urls()
        if code and code in urls:
            target_url = urls[code]
            self.send_response(302)
            self.send_header('Location', target_url)
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html_response = "^<h1^>404 - Link Tidak Ditemukan^</h1^>^<p^>Link ini mungkin telah kadaluarsa atau tidak valid.^</p^>"
            self.wfile.write(html_response.encode('utf-8'))
