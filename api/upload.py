from http.server import BaseHTTPRequestHandler
import json
import cgi
import io
import pandas as pd
from shapely import wkt

def parse_multipart(handler):
    """Parse multipart/form-data request to extract the file."""
    content_type = handler.headers.get('Content-Type', '')
    
    if not content_type.startswith('multipart/form-data'):
        return None, "Tipo de conteúdo inválido. Use multipart/form-data."
    
    # Parse o conteúdo multipart
    form = cgi.FieldStorage(
        fp=handler.rfile,
        headers=handler.headers,
        environ={
            'REQUEST_METHOD': 'POST',
            'CONTENT_TYPE': content_type,
        }
    )
    
    # Obtenha o arquivo
    if 'file' not in form:
        return None, "Campo 'file' não encontrado"
    
    fileitem = form['file']
    if not fileitem.file:
        return None, "Arquivo vazio"
    
    return fileitem, None

def process_excel(fileitem):
    """Processa o arquivo Excel e extrai coordenadas de pontos WKT."""
    try:
        # Verifica a extensão
        filename = fileitem.filename.lower()
        if not filename.endswith(('.xls', '.xlsx')):
            return None, "O arquivo deve ser .xls ou .xlsx"

        # Lê o conteúdo do arquivo em memória
        file_data = fileitem.file.read()
        df = pd.read_excel(io.BytesIO(file_data))
        
        # Verifica as colunas necessárias
        if 'number' not in df.columns or 'location' not in df.columns:
            return None, "As colunas 'number' e 'location' são obrigatórias"
        
        # Processa os pontos
        results = []
        for _, row in df.iterrows():
            try:
                if pd.isna(row['number']) or pd.isna(row['location']):
                    continue
                    
                # Parse WKT para coordenadas
                geom = wkt.loads(str(row['location']))
                results.append({
                    'number': int(row['number']),
                    'latitude': geom.y,
                    'longitude': geom.x
                })
            except Exception:
                # Ignora linhas com erro
                continue
                
        if not results:
            return None, "Nenhum ponto WKT válido encontrado no arquivo"
            
        return results, None
    except Exception as e:
        return None, f"Erro ao processar arquivo: {str(e)}"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse a solicitação multipart
            fileitem, error = parse_multipart(self)
            if error:
                self.send_error(400, error)
                return
                
            # Processa o Excel
            results, error = process_excel(fileitem)
            if error:
                self.send_error(400, error)
                return
                
            # Retorna os resultados
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(results).encode())
        except Exception as e:
            self.send_error(500, str(e))
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'message': 'API de WKT para Lat/Long. Faça um POST com um arquivo Excel contendo "number" e "location".'
        }).encode()) 