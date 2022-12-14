from flask import Flask
import pixiv_api

app = Flask(__name__)


@app.route('/json/<int:img_id>')
def get_detail(img_id):
    pixiv = pixiv_api.Pixiv()
    return pixiv.get_image_json(img_id)


@app.route('/image/<int:img_id>')
def get_image(img_id):
    pixiv = pixiv_api.Pixiv()
    return pixiv.get_image(img_id)


@app.route('/images/<int:img_id>/<int:img_num>')
def get_images(img_id, img_num):
    pixiv = pixiv_api.Pixiv()
    return pixiv.get_images(img_id, img_num)


@app.route('/')
def hello_world():
    return 'Hello, World!'
