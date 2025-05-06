# API de Conversão WKT para Lat/Long

API simples para converter coordenadas no formato WKT (Well-Known Text) para latitude e longitude.

## Endpoints

- `GET /api` - Documentação da API
- `POST /api/upload` - Envio de arquivo Excel para conversão

## Uso

Faça um POST para `/api/upload` com um arquivo Excel contendo:
- Coluna `number` com o identificador do ponto
- Coluna `location` com o ponto no formato WKT, exemplo: `POINT Z (28.26384809883179 45.40868410295115 0)`

### Exemplo de resposta:

```json
[
  {
    "number": 1,
    "latitude": 45.40868410295115,
    "longitude": 28.26384809883179
  },
  {
    "number": 2,
    "latitude": 45.41390142171629,
    "longitude": 28.25258833227215
  }
]
```

## Testando localmente

```bash
python -m uvicorn index:app --reload
``` 