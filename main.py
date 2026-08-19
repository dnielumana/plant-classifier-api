from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io
import torchvision.transforms as transforms
from model import model, predict

app = FastAPI()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

@app.get("/") #when sends GET, run fuction
def root():
    return {"Status": "API is running"}

@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = transform(image)
    prediction = predict(tensor)
    return {"prediction": prediction}
