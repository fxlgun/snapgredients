from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
from PIL import Image
import argparse
from typing import List 
import keras_ocr

app = FastAPI()

pipeline = keras_ocr.pipeline.Pipeline()

@app.post("/upload/")
async def upload_image(image: UploadFile = File(...)):
    try:
        contents = await image.read()
        with open(image.filename, "wb") as f:
            f.write(contents)
        result = ocr_scan(image.filename)
        print(result)    
        return JSONResponse(content={"message": "Image uploaded successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

def ocr_scan(image_path):
    image = keras_ocr.tools.read(image_path)
    recognized_text = ''
    predictions = pipeline.recognize([image])
    for _, text in predictions[0]:
        recognized_text += text + ' '
    return recognized_text.strip()

@app.get("/")
def welcome():
    return "Welcome to Snapgredient"
