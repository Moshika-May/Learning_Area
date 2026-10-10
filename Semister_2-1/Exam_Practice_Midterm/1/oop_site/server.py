"""Local OOP tutor. Run: python3 server.py  then open http://127.0.0.1:8000"""
import json, subprocess, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HERE = Path(__file__).parent

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body = (HERE / "index.html").read_bytes()
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers(); self.wfile.write(body)

    def do_POST(self):
        # custom header = other websites can't call this (CORS preflight fails)
        if self.headers.get("X-Run") != "1":
            self.send_response(403); self.end_headers(); return
        code = json.loads(self.rfile.read(int(self.headers["Content-Length"])))["code"]
        try:
            p = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, timeout=5)
            out = p.stdout + p.stderr
        except subprocess.TimeoutExpired:
            out = "⏱ รันนานเกิน 5 วินาที (วนลูปไม่จบหรือเปล่า?)"
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(json.dumps({"out": out}).encode())

    def log_message(self, *a): pass

print("เปิด http://127.0.0.1:8000")
HTTPServer(("127.0.0.1", 8000), H).serve_forever()
