from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .fit_processor import process_fit_file

app = FastAPI(title="RunManager API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/upload')
async def upload_fit(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.fit'):
        raise HTTPException(status_code=400, detail='Fichier non .fit')
    contents = await file.read()
    metrics = process_fit_file(contents)
    return JSONResponse(content=metrics)

@app.get('/health')
def health():
    return {"status": "ok"}