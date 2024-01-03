# Importing libraries
import numpy as np
import glob
import os
from io import BytesIO
from PIL import Image
from tensorflow import keras
from fastapi import FastAPI, File, UploadFile, HTTPException

# Loading model
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models')
local_model_paths = glob.glob(f"{model_path}/*")
model_path_on_disk = sorted(local_model_paths)[-1]

model = keras.models.load_model(model_path_on_disk)

class_name = ['Early Blight', 'Late Blight', 'Healthy']

app = FastAPI()

# Reading and reshaping an image model that has been trained on image size (180, 180)
def read_img(data):
    try:
        img = Image.open(BytesIO(data))
    except Exception as e:
        raise ValueError(f"Failed to open image: {e}")
    img = img.resize((180, 180))
    img = np.array(img)
    return img

# Post request
@app.post('/analysis')
async def pred(file: UploadFile = File(...)):
    img = read_img(await file.read())

    img_reshape = np.expand_dims(img, 0)

    if img_reshape is None:
        raise HTTPException(status_code = 500, detail = 'Image could not be reshaped')

    try:
        pred = model.predict(img_reshape)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {e}")

    pred_class = class_name[np.argmax(pred)]
    confidence = float(np.max(pred))
    return {
        'prediction': pred_class,
        'confidence': confidence
    }
