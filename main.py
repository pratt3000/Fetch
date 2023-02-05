from flask import Flask, request
from utils import FetchData
from flask import send_file

import json


app = Flask("Fetch")


@app.route('/image/<int:image_index>')
def allow(image_index):
    return send_file(f"assets/images/{image_index}.png", mimetype='image/png')


@app.route("/index.html")
def index():
    file_content = open("assets/index.html", "r").read()
    return file_content


@app.route("/submit", methods=["POST"])
def submit():
    file = request.files.get("file")
    if file:
        contents = file.read().decode("utf-8")
        with open("assets/data_daily.csv", "w") as f:
            f.write(contents)
        data = FetchData("assets/data_daily.csv")
        data.train()
        output = data.predict()
        return json.dumps(output)
    return "No file"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
