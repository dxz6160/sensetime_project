import os
import time
import json
import random
import string
from config import BASE_DIRS
from PIL import Image
from tornado.gen import coroutine
from tornado.web import RequestHandler
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

method = 'method1'

class HomeHandler(RequestHandler):
    def get(self):
        self.write('home')

class PicHandler(RequestHandler):
    executor = ThreadPoolExecutor(100)

    def get(self):
        global method

        try:
            method = self.request.arguments.get('method', [])[0]
            method = method.decode('UTF-8')
        except:
            pass

        self.render('post_pic.html', filename = 'None.png', result = '')

    @coroutine
    def post(self):
        global method
        upload_path = './static/picture'

        res = yield self.Time_consuming_operation(upload_path, method)

        result = res[0]
        filename = res[1]
        pic_id = res[2]
        confidence = res[3]

        result_dic = {
            'Statu_code': 200,
            'Pic_id': pic_id,
            'Classification': result,
            'Confidence': confidence,
            'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }

        result_dic = json.dumps(result_dic, ensure_ascii=False)

        self.write(result_dic)
        self.render('post_pic.html', filename = filename, result = result)

    @run_on_executor
    def Time_consuming_operation(self, upload_path, method):
        meta = self.request.files.get('file', [])[0]
        file_name = meta.get('filename')
        pic_id = 'pic_' + time.strftime("%Y%m%d", time.localtime()) + ''.join(random.sample(string.ascii_letters + string.digits, 4))
        file_path = os.path.join(upload_path, file_name)
        with open(file_path, 'wb') as f:
            f.write(meta.get('body'))
        # return pic_id, file_name
        image_type = file_name.split('.')[-1]
        # 缩略图
        im = Image.open(file_path)  # 打开图片
        im.thumbnail((400, 400))  # 设置图片大小
        if image_type == 'jpg':
            aa = 'jpeg'
        elif image_type == 'png':
            aa = 'png'
        im.save(file_path, aa)

        if method == 'method1':
            cmd = 'cd /home/jcai/sensetime_project/Obj_Classify  && python predict.py /home/jcai/sensetime_project/static/picture/' + file_name
            val = os.popen(cmd).read()
            result = val.split('类')[1]
            confidence = ''
            return result, file_name, pic_id, confidence
        elif method == 'method2':
            cmd = 'cd /home/jcai/sensetime_project/libtorch-cpp/build && ./classifier ../abc.pt ../label.txt /home/jcai/sensetime_project/static/picture/' + file_name
            val = os.popen(cmd).read()
            result = val.split(':')[1].split('\n')[0]
            confidence = val.split(':')[2].strip('\n')
            return result, file_name, pic_id, confidence


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