import os
import time
import json
import random
import string
from tornado.gen import coroutine
from tornado.web import RequestHandler
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

class HomeHandler(RequestHandler):
    def get(self):
        self.write('home')

class PicHandler(RequestHandler):
    executor = ThreadPoolExecutor(100)

    @coroutine
    def post(self):
        upload_path = './static/picture'

        res = yield self.Time_consuming_operation(upload_path)

        pic_id = res[0]
        result = res[1]

        result_dic = {
            'Statu_code': 200,
            'Pic_id': pic_id,
            'Classification': result,
            'Confidence': "",
            'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }

        result_dic = json.dumps(result_dic, ensure_ascii=False)

        self.write(result_dic)

    @run_on_executor
    def Time_consuming_operation(self, upload_path):
        meta = self.request.files.get('file', [])[0]
        file_name = meta.get('filename')
        pic_id = 'pic_' + time.strftime("%Y%m%d", time.localtime()) + ''.join(
            random.sample(string.ascii_letters + string.digits, 4))
        file_path = os.path.join(upload_path, file_name)
        with open(file_path, 'wb') as f:
            f.write(meta.get('body'))
        return pic_id, file_name

class VideoHandler(RequestHandler):
    executor = ThreadPoolExecutor(10)

    @coroutine
    def post(self):
        upload_path = './static/video'
        video = yield self.post_video(upload_path)

        video_id  = video[0]
        result = video[1]


        result_dic = {
            'Statu_code': 200,
            'Video_id': video_id,
            'Content': result,
            'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        result_dic = json.dumps(result_dic, ensure_ascii=False)
        self.write(result_dic)

    @run_on_executor
    def post_video(self, upload_path):
        meta = self.request.files.get('file', [])[0]  # 获取文件对象
        file_name = meta.get('filename')
        video_id = 'pic_' + time.strftime("%Y%m%d", time.localtime()) + ''.join(random.sample(string.ascii_letters + string.digits, 4))
        file_path = os.path.join(upload_path, file_name)  # 拼接路径
        with open(file_path, 'wb') as f:
            f.write(meta.get('body'))  # 写入内容
        return video_id, file_name