import os
import shutil
from random import randint
from datetime import datetime

from typing import Optional
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from torch.utils.data import DataLoader
from predict import ImgListDataset, TrafficLaneInference
import pytorch_lightning as pl

import base64


model = TrafficLaneInference.load_from_checkpoint(checkpoint_path="lane_detection_e5b5lr001.ckpt")
model.batch_size = 1
trainer = pl.Trainer(gpus=1, progress_bar_refresh_rate=0)

app = FastAPI()

# 출처 명시 
origins = [ 
    "http://localhost.tiangolo.com", 
    "https://localhost.tiangolo.com", 
    "http://localhost", 
    "http://localhost:5000",
    "http://3.134.125.59",
    "http://3.134.125.59:5000",
    "*"
] 

# 미들웨어 추가 
app.add_middleware( 
    CORSMiddleware, 
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"], 
)

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

class ImgItem(BaseModel):
    name: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    upload_dir = 'upload'
    response_dir = 'response'
    now2filename = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    now2filename = now2filename + f'-{randint(10000, 100000)}-' + image.filename
    upload_img_path = os.path.join('.', upload_dir, now2filename)

    with open(upload_img_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    inf_img_list = [upload_img_path]
    inf_dataset = ImgListDataset(img_data_path_list=inf_img_list)
    inf_dataloader = DataLoader(inf_dataset, batch_size = model.batch_size, num_workers=1)
    trainer.test(model, inf_dataloader)

    send_img = upload_img_path.replace(upload_dir, response_dir)
    #return FileResponse(send_img)

    with open(send_img, "rb") as image_file:
        encoded_image_string = base64.b64encode(image_file.read())

    payload = {
        "mime" : "image/png",
        "image": encoded_image_string,
        "some_other_data": None
    }

    return payload
