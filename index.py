from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import pandas as pd
from shapely import wkt

app = FastAPI(title="API de Conversão WKT → Lat/Lon")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

class PointOut(BaseModel):
    number: int
    latitude: float
    longitude: float

@app.get("/")
async def root():
    return {"message": "API de Conversão WKT para Lat/Long. Use o endpoint POST /api/upload para enviar arquivos Excel."}

@app.post("/api/upload")
async def upload_planilha(file: UploadFile = File(...)):
    # valida extensão
    if not file.filename.lower().endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Envie um arquivo .xls ou .xlsx")
    
    try:
        # lê planilha Excel
        df = pd.read_excel(file.file)
        
        # validar colunas
        if "number" not in df.columns or "location" not in df.columns:
            raise HTTPException(status_code=400, detail="Cols 'number' e 'location' obrigatórias")

        resultado = []
        for idx, row in df.iterrows():
            try:
                # tratar valores NaN ou None
                if pd.isna(row["location"]) or pd.isna(row["number"]):
                    continue
                    
                # converter WKT para coordenadas
                geom = wkt.loads(str(row["location"]))
                resultado.append({
                    "number": int(row["number"]),
                    "latitude": geom.y,
                    "longitude": geom.x
                })
            except Exception as e:
                # ignorar linhas com erro para não interromper todo o processo
                continue
        
        # verificar se temos resultados
        if not resultado:
            raise HTTPException(status_code=422, detail="Nenhum ponto WKT válido encontrado no arquivo")
            
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar arquivo: {str(e)}")

# Para ambiente serverless
handler = app 