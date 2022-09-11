import pixivpy3
import os


class Pixiv:
    def get_image_json(self, img_id: int):
        return self.api.illust_detail(img_id)

    def __init__(self):
        self.refreshToken = os.getenv("pixiv_refresh_token")
        self.api = pixivpy3.AppPixivAPI()
        self.api.auth(refresh_token=self.refreshToken)
