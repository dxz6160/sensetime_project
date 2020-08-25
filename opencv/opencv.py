import os
import cv2

def opencv_1():
    folder_name = r'vedio/DJI_0547_out'
    image_extension = '.jpg'
    output_video_name = 'labeled_WT5'
    output_video_extension = '.mp4'
    frame_per_second = 30
    #####################################################################
    #####################################################################

    images = []

    # 按照顺序把你每个帧的名字排到image这个list里，我这里出来的结果是[frame-0001.png, frame-0002.png, ...] 注意不要忘记extension，_length
    for pic in range(len(os.listdir(folder_name))):

        images.append(str(pic+1) + image_extension)

    print(images)

    frame = cv2.imread(os.path.join(folder_name, images[1]))
    height, width, layers = frame.shape
    size = (width, height)

    out = cv2.VideoWriter(output_video_name + output_video_extension, 0, frame_per_second, size)

    for image in images:
        out.write(cv2.imread(os.path.join(folder_name, image)))

    cv2.destroyAllWindows()
    out.release()

def opencv_2(filename):
    # 要提取视频的文件名，隐藏后缀
    sourceFileName = filename.split('.')[0]
    # 在这里把后缀接上
    video_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/video", filename)
    print(video_path)
    times = 0
    # 提取视频的频率，每25帧提取一个
    frameFrequency = 1
    # 输出图片到当前目录vedio文件夹下
    outPutDirName = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/out_picture/", sourceFileName) + '/'
    print(outPutDirName)
    # if not os.path.exists(outPutDirName):
    #     # 如果文件目录不存在则创建目录
    #     os.makedirs(outPutDirName)
    # camera = cv2.VideoCapture(video_path)
    # final = ''
    # while True:
    #     times += 1
    #     res, image = camera.read()
    #     if not res:
    #         print('not res , not image')
    #         break
    #     if times % frameFrequency == 0:
    #         # local = final[times - 1][1]
    #         # for tag in local:
    #         #     x1 = int(tag[0].split(',')[0].split('.')[0])
    #         #     y1 = int(tag[0].split(',')[1].split('.')[0])
    #         #     x2 = int(tag[0].split(',')[2].split('.')[0])
    #         #     y2 = int(tag[0].split(',')[3].split('.')[0])
    #         #     type = tag[1]
    #         #     confident = tag[2]
    #         #     cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 4)
    #         #     font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    #         #     text = 'type:{} confident:{}'.format(type, confident)
    #         #     cv2.putText(image, text, (x1, y1 + 100), font, 2, (0, 0, 255), 2)
    #         cv2.imwrite(outPutDirName + str(times) + '.jpg', image)
    #         print(outPutDirName + str(times) + '.jpg')
    # print('图片提取结束')
    # camera.release()

if __name__ == '__main__':
    opencv_2('DJI_0547_out.MP4')