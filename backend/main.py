import torch
from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from starlette.responses import RedirectResponse
import io
import cv2
import numpy as np
from . import models
from . import utils

CONFIG = {
    'input_size' : 1024,
    'device' : 'mps' if torch.has_mps else 'cuda' if torch.cuda.is_available() else 'cpu',
    'pth_path' : './backend/assets/east.pth',
}

app = FastAPI()
model = utils.load_model(CONFIG['device'], CONFIG['pth_path'])

# rediect home url -> /docs
@app.get("/")
async def home() -> RedirectResponse:
    return RedirectResponse('/docs')

@app.post("/ocr-detection")
async def inference_files(files: List[UploadFile]):
    if not files:
        return {"message": "No upload file sent"}
    else:
        # Get image file
        contents = files[0].file.read()
        nparr = np.fromstring(contents, np.uint8) # type: ignore        
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Inference
        ret_img = utils.inference(model, img, CONFIG['input_size'], CONFIG['device'])

        # Return File
        binary_cv = cv2.imencode('.png', ret_img)[1].tobytes()
        image_stream = io.BytesIO(binary_cv)
        return StreamingResponse(content=image_stream, media_type="image/png")