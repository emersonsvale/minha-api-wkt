# API de Localização - Teste

Script para testar uma API que converte coordenadas WKT para Latitude/Longitude.

## Requisitos

```
pip install requests
```

## Como usar

Execute o script informando o caminho do arquivo Excel:

```
python test_api.py --file caminho/para/seu/arquivo.xlsx
```

Parâmetros opcionais:
- `--file`: Caminho para o arquivo Excel (padrão: ./sample.xlsx)
- `--url`: URL da API (padrão: https://minha-api-wkt.vercel.app/api/upload)

Exemplo:
```
python test_api.py --file ./dados/coordenadas.xlsx --url https://minha-api-personalizada.com/api/upload
```

## Formato do Arquivo

O arquivo Excel deve conter as coordenadas WKT no formato esperado pela API.
