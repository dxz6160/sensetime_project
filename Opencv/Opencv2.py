'''
@author: trise
@studioe: JCAI
@software: pycharm
@time: 2020/8/16 23:10
'''
import cv2
import os


with open('out.txt', 'r') as f:
    content = f.read()

content = content.replace('\n','').replace(' ','').replace(",device='cuda:0'", '')
content = content.replace("'boxes'",'')
content = content.replace("'labels'",'')
content = content.replace("'scores'",'')
content = content.replace(":tensor",'')

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

final = sorted(dic.items(), key=lambda obj: obj[0])


#要提取视频的文件名，隐藏后缀
sourceFileName='DJI_0547_out'
#在这里把后缀接上
video_path = os.path.join("", "", sourceFileName+'.mp4')
times=0
#提取视频的频率，每25帧提取一个
frameFrequency=1
#输出图片到当前目录vedio文件夹下
outPutDirName='vedio/'+sourceFileName+'/'
if not os.path.exists(outPutDirName):
    #如果文件目录不存在则创建目录
    os.makedirs(outPutDirName)
camera = cv2.VideoCapture(video_path)
while True:
    times+=1
    res, image = camera.read()
    if not res:
        print('not res , not image')
        break
    if times%frameFrequency==0:
        local = final[times-1][1]
        for tag in local:
            x1 = int(tag[0].split(',')[0].split('.')[0])
            y1 = int(tag[0].split(',')[1].split('.')[0])
            x2 = int(tag[0].split(',')[2].split('.')[0])
            y2 = int(tag[0].split(',')[3].split('.')[0])
            type = tag[1]
            confident = tag[2]
            cv2.rectangle(image, (x1,y1), (x2,y2), (0, 255, 0), 4)
            font = cv2.FONT_HERSHEY_COMPLEX_SMALL
            text = 'type:{} confident:{}'.format(type, confident)
            cv2.putText(image, text, (x1,y1+100), font, 2, (0, 0, 255), 2)
        cv2.imwrite(outPutDirName + str(times)+'.jpg', image)
        print(outPutDirName + str(times)+'.jpg')
print('图片提取结束')
camera.release()