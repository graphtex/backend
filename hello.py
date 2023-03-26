from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from model_to_tex import get_latex
import sys
import numpy as np
from PIL import Image
import base64

app = Flask(__name__)

# allow our Javascript app hosted on a different port (and thus origin) to access this Flask app
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/", methods=["GET", "POST"])
@cross_origin()
def index():

    if request.method == "POST":
        print("hiii", file=sys.stderr)
        request_data = request.data
        print(type(request_data))
        # data = request_data.stream.read()
        data = base64.encodebytes(request_data)
        print(data)

        #Tried
        #print(request_data.decode("utf-8"))
        # img = Image.frombytes("RGBA", (100, 100), request_data)
        # print(img)

        # grab the image file from the url, convert to some python object i.e. PIL Image..   # img = Image().open("filename.png")
        # run_inference :: Image -> (Boxes, Labels)

        # Feed output from neural network into get_latex
        # get_latex(model_output)

        return {"code": "blah"}


# HOW TO RUN
# run this app using: python3 -m flask --app hello run
