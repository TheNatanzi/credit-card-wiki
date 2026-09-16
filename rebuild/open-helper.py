# -*- coding: utf-8 -*-
"""Tiny localhost helper for the wiki: GET /open?u=<url> opens the URL in Chrome (new window).
Also serves the wiki at http://127.0.0.1:8787/ . Start: rebuild/open-helper.cmd"""
import http.server, urllib.parse, subprocess, os, socketserver
PORT=8787; WIKI=r"C:\Claude\credit-card-wiki"
CHROME=[p for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")) if os.path.exists(p)]
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**k): super().__init__(*a,directory=WIKI,**k)
    def log_message(self,*a): pass
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin","*"); self.send_header("Cache-Control","no-store"); super().end_headers()
    def do_GET(self):
        q=urllib.parse.urlparse(self.path)
        if q.path=="/open":
            u=urllib.parse.parse_qs(q.query).get("u",[""])[0]
            ok=u.startswith(("http://","https://"))
            if ok:
                if CHROME: subprocess.Popen([CHROME[0],"--new-window",u])
                else: os.startfile(u)
            self.send_response(200 if ok else 400); self.send_header("Content-Type","text/plain"); self.end_headers()
            self.wfile.write(b"opened" if ok else b"bad url"); return
        if q.path=="/ping":
            self.send_response(200); self.send_header("Content-Type","text/plain"); self.end_headers(); self.wfile.write(b"ok"); return
        super().do_GET()
socketserver.TCPServer.allow_reuse_address=True
with socketserver.ThreadingTCPServer(("127.0.0.1",PORT),H) as s: s.serve_forever()
