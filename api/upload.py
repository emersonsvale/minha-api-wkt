from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
from shapely import wkt

app = FastAPI(title="API de Conversão WKT → Lat/Lon")

class PointOut(BaseModel):
    number: int
    latitude: float
    longitude: float

@app.get("/")
async def root():
    return {"message": "API de Conversão WKT para Lat/Long. Use /api/upload para enviar arquivos Excel."}

@app.post("/api/upload", response_model=List[PointOut])
async def upload_planilha(file: UploadFile = File(...)):
    # valida extensão
    if not file.filename.lower().endswith((".xls", ".xlsx")):
        raise HTTPException(400, "Envie um arquivo .xls ou .xlsx")
    # lê planilha Excel
    df = pd.read_excel(file.file)
    if "number" not in df.columns or "location" not in df.columns:
        raise HTTPException(400, "Cols 'number' e 'location' obrigatórias")

    resultado = []
    for idx, row in df.iterrows():
        try:
            geom = wkt.loads(row["location"])
            resultado.append(PointOut(
                number=int(row["number"]),
                latitude=geom.y,
                longitude=geom.x
            ))
        except Exception as e:
            raise HTTPException(422, f"Erro ao parsear WKT na linha {idx+2}: {e}")
    return resultado 