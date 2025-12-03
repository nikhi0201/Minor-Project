import uvicorn
import easyocr
import numpy as np
import cv2
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
app = FastAPI(title="OCR API", description="Handwritten Text Recognition API using EasyOCR")

reader = easyocr.Reader(['en', 'hi'], gpu=False)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()

    
        np_img = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        
        results = reader.readtext(image)

        output = []
        for (bbox, text, prob) in results:
            output.append({
                "bbox": bbox,
                "text": text,
                "confidence": float(prob)
            })

        return {"results": output}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
