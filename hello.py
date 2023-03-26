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
from model_to_tex import get_latex, model_output

app = Flask(__name__)

# allow our Javascript app hosted on a different port (and thus origin) to access this Flask app
# cors = CORS(app)
# app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/", methods=["GET", "POST"])
@cross_origin()
def index():
    print("HERE")
    if request.method == "POST":
        f = request.files['img']
        # f.save(f.filename)

        img = Image.open(f)

        t = T.ToTensor()(img)

        time.sleep(2)

        latex = get_latex(model_output)
        # latex = 'abc'

        #Tried
        #print(request_data.decode("utf-8"))
        # img = Image.frombytes("RGBA", (100, 100), request_data)
        # print(img)

        # grab the image file from the url, convert to some python object i.e. PIL Image..   # img = Image().open("filename.png")
        # run_inference :: Image -> (Boxes, Labels)

        # Feed output from neural network into get_latex
        # get_latex(model_output)

        return {"code": latex}
    


# HOW TO RUN
# run this app using: python3 -m flask --app hello run
