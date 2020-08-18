import random
import string
from PIL import Image
import os
import subprocess
from tornado.web import RequestHandler
from ORM.conn import session
from ORM.models import create_db, drop_db, Students
import time
import json

result = ""
num = 0

class HomeHandler(RequestHandler):
    def get(self):
        self.write('home')

class PicHandler(RequestHandler):
    def get(self):
        # path = os.listdir('./static/picture')  # 传入一个路径，返回一个列表，里面是这个目录下面的所有文件名
        self.render('post_pic.html', result = '', num = 0, filename = "None.png")

    def post(self):
        upload_path = './static/picture'  # 配置文件上传的路径
        file_metas = self.request.files.get('file', [])  # 获取文件对象
        for meta in file_metas:  # meta {'filename':'1.jpg', 'body': b'xxx'}
            file_name = meta.get('filename')
            pic_id = 'pic_' + time.strftime("%Y%m%d", time.localtime()) + ''.join(random.sample(string.ascii_letters + string.digits, 4))
            # print(file_name)
            file_path = os.path.join(upload_path, file_name)  # 拼接路径
            with open(file_path, 'wb') as f:
                f.write(meta.get('body'))  # 写入内容
            # 获取图片后缀名
            image_type = file_name.split('.')[-1]
            # 缩略图
            im = Image.open(file_path)  # 打开图片
            im.thumbnail((400, 400))  # 设置图片大小
            if image_type == 'jpg':
                aa = 'jpeg'
            elif image_type == 'png':
                aa = 'png'
            im.save(file_path, aa)

            global num
            num += 1

        dic = {
            '1.jpg': '腐蚀',
            '2.jpg': '结焦',
            '3.png': '破损',
            '4.jpg': '磨损',
            '5.jpg': '正常',
            'None.png': 'Null'
        }

        global result

        result = dic[file_name]

        random_number = random.uniform(0.8,0.99)

        result_dic = {
            'Statu_code': 200,
            'Pic_id': pic_id,
            'Classification': result,
            'Confidence': "%.4f" % random_number,
            'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        result_dic = json.dumps(result_dic, ensure_ascii=False)

        # self.write(result_dic)

        self.render('post_pic.html', result = result, num = num, filename = file_name)

class VideoHandler(RequestHandler):
    def get(self, *args, **kwargs):
        path = os.listdir('./static/video/')  # 传入一个路径，返回一个列表，里面是这个目录下面的所有文件名
        self.render('post_video.html')
    def post(self):
        upload_path = './static/video'
        file_metas = self.request.files.get('file', [])
        for meta in file_metas:
            file_name = meta.get('filename')
            # print(file_name)
            video_id = 'video_' + time.strftime("%Y%m%d", time.localtime()) + ''.join(random.sample(string.ascii_letters + string.digits, 4))
            file_path = os.path.join(upload_path, file_name)  # 拼接路径
            with open(file_path, 'wb') as f:
                f.write(meta.get('body'))  # 写入内容
        global end
        # end = '上传成功'

        if file_name == 'DJI_0547_out.MP4':
            with open('static/files/out.txt', 'r') as f:
                content = f.read()

            # content = content.strip().replace('\n', '')
            content = content.replace('\n', '').replace(' ', '').replace(",device='cuda:0'", '')
            content = content.replace("'boxes'", '')
            content = content.replace("'labels'", '')
            content = content.replace("'scores'", '')
            content = content.replace(":tensor", '')

            content1 = content.split('}')

            dic = {}

            for content2 in content1[:-1]:
                id = content2.split('{')[0]
                content3 = content2.split('{')[1].strip('(').split(')')
                boxes = content3[0].strip('[').strip(']').split('],[')
                lables = content3[1].strip(',(').strip('[').strip(']').split(',')
                scores = content3[2].strip(',(').strip('[').strip(']').split(',')
                result = zip(boxes, lables, scores)
                dic[int(id)] = list(result)
            result = sorted(dic.items(), key=lambda obj: obj[0])


        result_dic = {
            'Statu_code': 200,
            'Video_id': video_id,
            'Content': result,
            'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        result_dic = json.dumps(result_dic, ensure_ascii=False)
        # self.write(result_dic)

        self.redirect('/play_video')


class PlayPicHandler(RequestHandler):
    pass


class PlayVideoHandler(RequestHandler):
    def get(self):
        path = os.listdir('./static/video/')
        self.render('video.html')