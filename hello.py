from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from model_to_tex import get_latex
import time
import sys
import numpy as np
import torchvision.transforms as T
from PIL import Image
import base64
from model_to_tex import get_latex
from models.common import DetectMultiBackend
from utils.general import scale_boxes, non_max_suppression
from utils.augmentations import letterbox
import torch

app = Flask(__name__)

# allow our Javascript app hosted on a different port (and thus origin) to access this Flask app
# cors = CORS(app)
# app.config["CORS_HEADERS"] = "Content-Type"

conf_thres = .25
iou_thres = .45
classes = None
agnostic_nms = False
max_det = 1000

img_size = 640
stride = 32
auto = True

def predict(im):
    im.convert("RGB")
    im = np.asarray(im)
    im = letterbox(im, img_size, stride=stride, auto=auto)[0]  # padded resize
    im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
    im = np.ascontiguousarray(im)
    im = torch.from_numpy(im)
    im = im.float()
    im /= 255
    im = im[None]

    model = DetectMultiBackend("weights.pt", data="graph.yaml")
    pred = model(im)
    pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

    labels = []
    boxes = []

    for i, det in enumerate(pred):
        if len(det):
            for b in det:
                boxes.append(b[:4].tolist())
                labels.append(b[5].tolist())

    return {"boxes": boxes, "labels": labels}

@app.route("/", methods=["GET", "POST"])
@cross_origin()
def index():
    print("HERE")
    if request.method == "POST":
        f = request.files['img']

        im = Image.open(f)
        model_output = predict(im)
        latex = get_latex(model_output)

        #Tried
        #print(request_data.decode("utf-8"))
        # img = Image.frombytes("RGBA", (100, 100), request_data)
        # print(img)

        return {"code": latex}

def __main__():
    with Image.open("/home/larry/Pictures/graph/IMG_0047.png") as f:
        o = predict(f)
        print(get_latex(o))

# HOW TO RUN
# run this app using: python3 -m flask --app hello run

if __name__ == "__main__":
    __main__()