from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from rembg import remove
from PIL import Image
import io
# Pre-scarica il modello AI durante l'avvio del server
import subprocess
import sys

print("⏳ Download del modello AI in corso...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pillow", "onnxruntime"])
from rembg import remove, new_session
session = new_session()
print("✅ Modello AI pronto!")
app = FastAPI(title="AUTOdata Background Remover")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AUTOdata Background Remover API is running!"}

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        input_image = Image.open(io.BytesIO(image_data))
        output_image = remove(input_image, session=session)
        
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()
        
        return Response(
            content=img_bytes,
            media_type="image/png"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
