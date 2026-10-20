from http.server import BaseHTTPRequestHandler
import json
import os
from google import genai
from PIL import Image
import io
import base64

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            image_base64 = data.get('image').split(',')[1]
            tone = data.get('tone', 'santai')
            
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "API Key belum diset di server Vercel"}).encode('utf-8'))
                return

            client = genai.Client(api_key=api_key)

            image_bytes = base64.b64decode(image_base64)
            img = Image.open(io.BytesIO(image_bytes))
            img.thumbnail((1024, 1024))

            prompt = f"""
            Analisis gambar yang diunggah dan buatkan 3 opsi caption media sosial dalam Bahasa Indonesia dengan gaya bahasa '{tone}', lengkap dengan hashtag yang relevan.
            """

            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=[img, prompt]
            )

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {"success": True, "caption": response.text}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode('utf-8'))