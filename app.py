from flask import Flask
import pixiv_api

app = Flask(__name__)


@app.route('/json/<int:imgid>')
def get_detail(imgid):
    pixiv = pixiv_api.Pixiv()
    return pixiv.get_image_json(imgid)


@app.route('/image/<int:img_id>')
def get_detail(img_id):
    pixiv = pixiv_api.Pixiv()
    return pixiv.get_image(img_id)


@app.route('/')
def hello_world():
    return 'Hello, World!'
