from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'message': 'API de WKT para Lat/Long. Use POST /api/upload para enviar um arquivo Excel com colunas "number" e "location".',
            'endpoints': {
                '/api/upload': 'POST com arquivo Excel'
            }
        }).encode())
        return 