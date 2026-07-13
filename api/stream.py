from http.server import BaseHTTPRequestHandler
import yt_dlp
import json
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        self.end_headers()
        return

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query = parse_qs(parsed_path.query)
        
        video_id = query.get('videoId', [None])[0]
        
        if not video_id:
            self.send_response(400)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "videoId is required"}).encode('utf-8'))
            return

        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                
                url = info.get('url')
                if not url and 'formats' in info:
                    audio_formats = [f for f in info['formats'] if f.get('acodec') != 'none']
                    if audio_formats:
                        url = audio_formats[-1]['url']

            if not url:
                raise Exception("Could not find stream URL")

            self.send_response(302)
            self.send_header('Location', url)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return
