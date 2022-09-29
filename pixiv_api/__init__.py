import flask
import pixivpy3
import os
import requests
import sqlite3
import time
import json


def json_conv(json_str: str):
    json_cvd = ""
    for i in json_str:
        if i == "'":
            json_cvd += "\\'"
        else:
            json_cvd += i
    return json_cvd


class Pixiv:

    def get_image(self, img_id: int):
        json_str = self.get_image_json(img_id)
        json_list = json.loads(json_str)
        headers = {'Referer': 'https://www.pixiv.net'}
        try:
            url = json_list['illust']['meta_single_page']['original_image_url']
        except KeyError as e:
            return "出错了：该ID对应的可能不是单张图片。"
        req = requests.get(url=url, headers=headers, verify=False)
        response = flask.make_response(req.content)
        response.headers["Content-Type"] = "image/jpg"
        return response

    def get_images(self, img_id:int, img_num:int):
        json_str = self.get_image_json(img_id)
        json_list = json.loads(json_str)
        headers = {'Referer': 'https://www.pixiv.net'}
        try:
            page_count = json_list['illust']['page_count']
            if img_num>page_count:
                return "错误：图片超范围"
            url = json_list['illust']['meta_pages'][img_num-1]['image_urls']['original']
        except KeyError as e:
            return "出错了：该ID对应的可能不是多张图片。"
        req = requests.get(url=url, headers=headers, verify=False)
        response = flask.make_response(req.content)
        response.headers["Content-Type"] = "image/jpg"
        return response

    def get_image_json(self, img_id: int):
        sql = f"SELECT * FROM artworks WHERE id = {img_id}"
        cursor = self.cache.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        if row is not None:
            time_now = time.time()
            time_cache = int(row[2])
            if time_now - time_cache <= 86400:
                cursor.close()
                return row[1]
        else:
            json_dic = self.api.illust_detail(img_id)
            stori = json.dumps(json_dic)
            json_str = json_conv(stori)
            print(json_str)
            print("New data cached: id = %s" % img_id)
            sql = f'INSERT INTO artworks (id, json, "time") VALUES ({img_id}, \'{json_str}\', {time.time()})'
            cursor.execute(sql)
            self.cache.commit()
            cursor.close()
            return stori
        json_str = self.api.illust_detail(img_id)
        stori = json_str
        json_str = json_conv(json_str)
        print("Cache %s updated!" % img_id)
        sql = f"UPDATE artworks SET json = '{json_str}', time = {time.time()} WHERE id = {img_id}"
        cursor.execute(sql)
        self.cache.commit()
        cursor.close()
        return stori

    def __init__(self):
        self.refreshToken = os.getenv("pixiv_refresh_token")
        self.api = pixivpy3.AppPixivAPI()
        self.api.auth(refresh_token=self.refreshToken)
        self.cache = sqlite3.connect("cache.db")
        sql = "CREATE TABLE IF NOT EXISTS artworks(" \
              "id INTEGER PRIMARY KEY," \
              "json TEXT," \
              "time BIGINT);"
        cursor = self.cache.cursor()
        cursor.execute(sql)
        self.cache.commit()
        cursor.close()
