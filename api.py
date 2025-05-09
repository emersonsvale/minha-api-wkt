from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
from shapely import wkt
import io
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        
        # Log das colunas e primeiras linhas para debug
        logger.info(f"Colunas encontradas: {df.columns.tolist()}")
        logger.info(f"Primeiras linhas:\n{df.head()}")
        
        # Verifica se as colunas necessárias existem
        if 'number' not in df.columns or 'location' not in df.columns:
            return JSONResponse(
                status_code=400,
                content={"error": "O arquivo deve conter as colunas 'number' e 'location'"}
            )
        
        # Converte as coordenadas
        result = []
        for index, row in df.iterrows():
            try:
                # Log da linha atual
                logger.info(f"Processando linha {index}: number={row['number']}, location={row['location']}")
                
                point = wkt.loads(row['location'])
                # Mantém o número como está, sem tentar converter
                result.append({
                    "number": str(row['number']),
                    "latitude": point.y,
                    "longitude": point.x
                })
            except Exception as e:
                logger.error(f"Erro na linha {index}: {str(e)}")
                return JSONResponse(
                    status_code=400,
                    content={"error": f"Erro ao processar linha {row['number']}: {str(e)}"}
                )
        
        return result
    
    except Exception as e:
        logger.error(f"Erro geral: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Erro ao processar arquivo: {str(e)}"}
        ) 