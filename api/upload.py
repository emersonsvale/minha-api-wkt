from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse
import pandas as pd
from shapely import wkt
import io

app = FastAPI()

@app.post("/api/upload")
async def process_upload(request: Request, file: UploadFile = File(...)):
    try:
        # Ler conteúdo do arquivo
        contents = await file.read()
        
        # Verificar extensão
        if not file.filename.lower().endswith((".xls", ".xlsx")):
            return JSONResponse(
                status_code=400,
                content={"error": "O arquivo deve ser .xls ou .xlsx"}
            )
        
        # Processar o Excel
        df = pd.read_excel(io.BytesIO(contents))
        
        # Verificar colunas
        if "number" not in df.columns or "location" not in df.columns:
            return JSONResponse(
                status_code=400, 
                content={"error": "As colunas 'number' e 'location' são obrigatórias"}
            )
        
        # Processar linhas
        results = []
        for _, row in df.iterrows():
            try:
                if pd.isna(row["location"]) or pd.isna(row["number"]):
                    continue
                
                geom = wkt.loads(str(row["location"]))
                results.append({
                    "number": int(row["number"]),
                    "latitude": geom.y,
                    "longitude": geom.x
                })
            except Exception:
                # Ignorar linhas com erro
                continue
        
        # Verificar se temos resultados
        if not results:
            return JSONResponse(
                status_code=422,
                content={"error": "Nenhum ponto WKT válido encontrado no arquivo"}
            )
        
        return results
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erro ao processar arquivo: {str(e)}"}
        )

# Para o ambiente serverless da Vercel
handler = app 