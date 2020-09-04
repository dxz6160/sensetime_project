import os
import time
import json
import warnings
import random
import string
import numpy as np
import cv2
from PIL import Image
from tornado.gen import coroutine
from tornado.web import RequestHandler
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

warnings.filterwarnings('ignore')

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
        if file_name.split('.')[1] != ('jpg' or 'png'):
            self.send_error(415, '格式错误')
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
            cmd = 'cd /home/ts/shanghai_test/defect_classification/Obj_Classify  && python predict.py /home/ts/shanghai_test/sensetime_project/static/picture/' + file_name
            val = os.popen(cmd).read()
            result = val.split('类')[1].strip('\n')
            confidence = ''
            return result, file_name, pic_id, confidence
        elif method == 'method2':
            cmd = 'cd /home/ts/shanghai_test/defect_classification/libtorch-cpp/build && ./classifier ../abc.pt ../label.txt /home/ts/shanghai_test/sensetime_project/static/picture/' + file_name
            val = os.popen(cmd).read()
            result = val.split(':')[1].split('\n')[0]
            confidence = val.split(':')[2].strip('\n')
            return result, file_name, pic_id, confidence


class VideoHandler(RequestHandler):
    executor = ThreadPoolExecutor(10)
    
    def get(self):
        global method

        try:
            method = self.request.arguments.get('method', [])[0]
            method = method.decode('UTF-8')
        except:
            pass
        self.render('post_video.html')

    @coroutine
    def post(self):
        upload_path = './static/video'
        res = yield self.post_video(upload_path)

        video_id  = res[0]
        result = res[1]
        videoname = res[2].split('.')[0]
        filename = 'tag_'+ videoname + '.mp4'


        result_dic = {
            'Statu_code': 200,
            'Video_id': video_id,
            'Content': result,
            'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        result_dic = json.dumps(result_dic, ensure_ascii=False)
        #self.write(result_dic)
        self.render('video.html', filename = filename)

    @run_on_executor
    def post_video(self, upload_path):
        meta = self.request.files.get('file', [])[0]  # 获取文件对象
        file_name = meta.get('filename')
        video_id = 'pic_' + time.strftime("%Y%m%d", time.localtime()) + ''.join(random.sample(string.ascii_letters + string.digits, 4))
        file_path = os.path.join(upload_path, file_name)  # 拼接路径
        with open(file_path, 'wb') as f:
            f.write(meta.get('body'))
        dealwith(file_name)
        if method == 'method1':
            cmd = 'cd /home/ts/shanghai_test/video_object_detection/FasterRCNN && python predict.py /home/ts/shanghai_test/sensetime_project/static/out_picture/' + file_name.split('.')[0] + '/'
            val = os.popen(cmd).read()
            result = content(val)
        elif method == 'method2':
            cmd = 'cd /home/ts/shanghai_test/video_object_detection/libtorch_fasterrcnn/build && ./example-app ../rcnn_gpu.pt /home/ts/shanghai_test/sensetime_project/static/out_picture/' + file_name.split('.')[0] + '/'
            val = os.popen(cmd).read()
            result = content2(val)
        tag_picture(file_name, result)
        get_video(file_name)
        return video_id, result, file_name


def dealwith(filename):
    sourceFileName = filename.split('.')[0]
    video_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/video", filename)
    times = 0
    frameFrequency = 1
    outPutDirName = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/out_picture/", sourceFileName) + '/'
    if not os.path.exists(outPutDirName):
        os.makedirs(outPutDirName)
    camera = cv2.VideoCapture(video_path)
    while True:
        times += 1
        res, image = camera.read()
        if not res:
            print('not res , not image')
            break
        if times % frameFrequency == 0:
            cv2.imwrite(outPutDirName + str(times) + '.png', image)
    camera.release()

def content(content):
    content = content.replace('\n', '').replace(' ', '').replace(",device='cuda:0'", '')
    content = content.replace("'boxes'", '')
    content = content.replace("'labels'", '')
    content = content.replace("'scores'", '')
    content = content.replace(":tensor", '')

    content1 = content.split('}')

    dic = {}

    for content2 in content1[:-1]:
        id = content2.split('{')[0]
        id = id.split('/')[-1]
        id = id.split('.')[0]
        content3 = content2.split('{')[1].strip('(').split(')')
        boxes = content3[0].strip('[').strip(']').split('],[')
        lables = content3[1].strip(',(').strip('[').strip(']').split(',')
        scores = content3[2].strip(',(').strip('[').strip(']').split(',')
        result = zip(boxes, lables, scores)
        dic[int(id)] = list(result)

    final = sorted(dic.items(), key=lambda obj: obj[0])
    return final

def content2(content):
    dic = {}

    content = content.replace('\nlabels is ', '|')
    content = content.replace('\nscore is', '')
    content = content.replace('\nbox is: ', ' ')
    content = content.replace('---', ',')
    content = content.split('#')
    for content1 in content[:-1]:
        # print(content1)
        content1 = content1.split('|')
        pic_id = content1[0].split('/')[-1].split('.')[0]
        list = []
        for content2 in content1[1:]:
            content2 = content2.split(' ')
            box = content2[2]
            score = content2[1]
            lable = content2[0]
            result = (box, lable, score)
            list.append(result)
        dic[int(pic_id)] = list

    final = sorted(dic.items(), key=lambda obj: obj[0])
    return final

def tag_picture(filename, result):
    sourceFileName = filename.split('.')[0]
    video_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/video", filename)
    times = 0
    frameFrequency = 1
    outPutDirName = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/tag_picture/", sourceFileName) + '/'
    if not os.path.exists(outPutDirName):
        os.makedirs(outPutDirName)
    camera = cv2.VideoCapture(video_path)
    while True:
        times += 1
        res, image = camera.read()
        if not res:
            print('not res , not image')
            break
        if times % frameFrequency == 0:
            local = result[times - 1][1]
            for tag in local:
                x1 = int(tag[0].split(',')[0].split('.')[0])
                y1 = int(tag[0].split(',')[1].split('.')[0])
                x2 = int(tag[0].split(',')[2].split('.')[0])
                y2 = int(tag[0].split(',')[3].split('.')[0])
                type = tag[1]
                confident = tag[2]
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 4)
                font = cv2.FONT_HERSHEY_COMPLEX_SMALL
                text = 'type:{} confident:{}'.format(type, confident)
                cv2.putText(image, text, (x1, y1 + 100), font, 2, (0, 0, 255), 2)
            cv2.imwrite(outPutDirName + 'image' + str(times) + '.jpg', image)
    #print('图片提取结束')
    camera.release()

def get_video(filename):
    filename = filename.split('.')[0]
    cmd = "ffmpeg -f image2 -i /home/ts/shanghai_test/sensetime_project/static/tag_picture/{}/image%d.jpg -r 30 /home/ts/shanghai_test/sensetime_project/static/tag_video/tag_{}.mp4".format(filename, filename)
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
	get_video('DJI_0547_out.MP4')
