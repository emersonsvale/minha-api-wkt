import requests
import os
import argparse
from pprint import pprint

def main():
    parser = argparse.ArgumentParser(description="Testa API de WKT para Lat/Long")
    parser.add_argument("--file", default="./sample.xlsx", help="Caminho para o arquivo Excel")
    parser.add_argument("--url", default="https://minha-api-wkt.vercel.app/api/upload", 
                        help="URL da API")
    args = parser.parse_args()

    print("Testando API de WKT para Lat/Long...")

    file_path = args.file
    if not os.path.exists(file_path):
        print(f"ERRO: Arquivo não encontrado em {file_path}")
        exit(1)

    print(f"Enviando arquivo: {file_path}")
    url = args.url

    try:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            response = requests.post(url, files=files)
        
        print(f"Status: {response.status_code}")
        print("Resposta:")
        
        if response.status_code == 200:
            data = response.json()
            pprint(data)
        else:
            print(response.text)
    except Exception as e:
        print(f"Erro ao fazer requisição: {e}")

if __name__ == "__main__":
    main() 