import pixivpy3
import os
import requests
import sqlite3
import time
import json


class Pixiv:

    def get_image(self, img_id: int):
        json_str = self.get_image_json(img_id)
        json_obj = json.loads(json_str)
        headers = {'Referer': 'https://www.pixiv.net'}
        url = json_obj['illust']['meta_single_page']['original_image_url']
        req = requests.get(url=url, headers=headers, verify=False)
        return req.content

    def get_image_json(self, img_id: int):
        sql = "SELECT * FROM artworks WHERE id = %s" % img_id
        cursor = self.cache.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        if row != 0:
            time_now = time.time()
            time_cache = int(row[2])
            if time_now - time_cache <= 86400:
                return row[1]
        else:
            json_str = self.api.illust_detail(img_id)
            print("New data cached: id = %s" % img_id)
            sql = "INSERT INTO artworks (id, json, time) VALUES (%s, '%s', %s)" % (img_id, json_str, time.time())
            cursor.execute(sql)
            self.cache.commit()
            cursor.close()
            return json_str
        json_str = self.api.illust_detail(img_id)
        print("Cache %s updated!" % img_id)
        sql = "UPDATE artworks SET json = '%s', time = %s WHERE id = %s" % (json_str, time.time(), img_id)
        return json_str

    def __init__(self):
        self.refreshToken = os.getenv("pixiv_refresh_token")
        self.api = pixivpy3.AppPixivAPI()
        self.api.auth(refresh_token=self.refreshToken)
        self.cache = sqlite3.connect("cache.db")
        sql = "CREATE TABLE IF NOT EXISTS artworks(" \
              "id INTEGER PRIMARY KEY," \
              "json TEXT," \
              "time BIGINT"
        cursor = self.cache.cursor()
        cursor.execute(sql)
        self.cache.commit()
        cursor.close()
