from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
from shapely import wkt
import io

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API de conversão WKT para Lat/Long"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Lê o arquivo Excel
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Verifica se as colunas necessárias existem
        if 'number' not in df.columns or 'location' not in df.columns:
            return JSONResponse(
                status_code=400,
                content={"error": "O arquivo deve conter as colunas 'number' e 'location'"}
            )
        
        # Converte as coordenadas
        result = []
        for _, row in df.iterrows():
            try:
                point = wkt.loads(row['location'])
                # Tenta converter para int, se não conseguir usa o valor original
                try:
                    number = int(row['number'])
                except (ValueError, TypeError):
                    number = str(row['number'])
                
                result.append({
                    "number": number,
                    "latitude": point.y,
                    "longitude": point.x
                })
            except Exception as e:
                return JSONResponse(
                    status_code=400,
                    content={"error": f"Erro ao processar linha {row['number']}: {str(e)}"}
                )
        
        return result
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erro ao processar arquivo: {str(e)}"}
        ) 