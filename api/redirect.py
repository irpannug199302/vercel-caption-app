from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from api.shorten import url_db
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        code = query.get('code', [None])[0]
        if code and code in url_db:
            target_url = url_db[code]
            self.send_response(302)
            self.send_header('Location', target_url)
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"^(h1^)404 - Link Tidak Ditemukan^(/h1^)")
