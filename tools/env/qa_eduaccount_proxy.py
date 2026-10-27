#!/usr/bin/env python3
"""
tools/qa_eduaccount_proxy.py - QA Authentication & Chunked-Encoding Proxy for EducationAccountService.
Intercepts requests on port 5016, handles both Content-Length and Transfer-Encoding: chunked,
injects MOEHQ internal authorization headers, and forwards to EducationAccountService on port 5006.
Part of the UI Automation test harness (does not modify copy/).
"""
import http.server
import socketserver
import urllib.request
import urllib.error
import sys

TARGET_HOST = "http://127.0.0.1:5006"
PORT = 5016


def read_chunked(rfile):
    """Read full HTTP payload when Transfer-Encoding: chunked is used."""
    chunks = []
    while True:
        line = rfile.readline().strip()
        if not line:
            break
        # Ignore chunk extensions if present
        chunk_size = int(line.split(b';')[0], 16)
        if chunk_size == 0:
            # Consume trailing headers / CRLF
            while True:
                trailer = rfile.readline().strip()
                if not trailer:
                    break
            break
        chunk_data = rfile.read(chunk_size)
        chunks.append(chunk_data)
        rfile.readline()  # consume trailing CRLF
    return b"".join(chunks)


class EduAccountProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_request(self):
        url = f"{TARGET_HOST}{self.path}"

        transfer_encoding = self.headers.get('Transfer-Encoding', '').lower()
        if 'chunked' in transfer_encoding:
            body = read_chunked(self.rfile)
        else:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None

        req_headers = {}
        for key, val in self.headers.items():
            if key.lower() not in ('host', 'content-length', 'transfer-encoding'):
                req_headers[key] = val

        # Ensure internal service-to-service auth headers (always include MOEHQ for internal queries)
        roles = req_headers.get('X-User-Roles', '')
        if not roles:
            req_headers['X-User-Roles'] = 'MOEHQ'
        elif 'MOEHQ' not in [r.strip() for r in roles.split(',')]:
            req_headers['X-User-Roles'] = f"{roles},MOEHQ"

        if 'X-User-Id' not in req_headers:
            req_headers['X-User-Id'] = 'system'

        proxy_req = urllib.request.Request(
            url,
            data=body,
            headers=req_headers,
            method=self.command
        )

        try:
            with urllib.request.urlopen(proxy_req, timeout=30) as resp:
                resp_body = resp.read()
                self.send_response(resp.status)
                for k, v in resp.getheaders():
                    if k.lower() not in ('transfer-encoding', 'content-length', 'connection'):
                        self.send_header(k, v)
                self.send_header('Content-Length', str(len(resp_body)))
                self.end_headers()
                self.wfile.write(resp_body)
        except urllib.error.HTTPError as e:
            err_body = e.read()
            self.send_response(e.code)
            for k, v in e.headers.items():
                if k.lower() not in ('transfer-encoding', 'content-length', 'connection'):
                    self.send_header(k, v)
            self.send_header('Content-Length', str(len(err_body)))
            self.end_headers()
            self.wfile.write(err_body)
        except Exception as ex:
            self.send_response(502)
            msg = f'{{"isSuccess":false,"statusCode":502,"message":"Proxy error: {str(ex)}"}}'.encode('utf-8')
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)

    do_GET = do_request
    do_POST = do_request
    do_PUT = do_request
    do_DELETE = do_request
    do_PATCH = do_request
    do_OPTIONS = do_request

    def log_message(self, format, *args):
        sys.stderr.write(f"[EduAccountProxy] {self.address_string()} - {format % args}\n")


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == '__main__':
    with ReusableTCPServer(('127.0.0.1', PORT), EduAccountProxyHandler) as httpd:
        sys.stderr.write(f"[EduAccountProxy] Listening on 127.0.0.1:{PORT} -> {TARGET_HOST}\n")
        httpd.serve_forever()
