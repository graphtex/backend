from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

# from PIL import Image

app = Flask(__name__)

# allow our Javascript app hosted on a different port (and thus origin) to access this Flask app
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/", methods=["GET", "POST"])
@cross_origin()
def index():
    if request.method == "POST":
        request_data = request.get_json()

        # process the data here
        img_url = request_data["url"]

        # grab the image file from the url, convert to some python object i.e. PIL Image..   # img = Image().open("filename.png")
        # run_inference :: Image -> (Boxes, Labels)
        # translate_tikz :: (Boxes, Labels) -> Text

        return {"code": "blah"}


# HOW TO RUN
# run this app using: python3 -m flask --app hello run
