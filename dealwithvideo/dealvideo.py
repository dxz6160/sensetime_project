import glob
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
    print('图片提取结束')
    camera.release()


def content(content):
    content = content.replace('\n', '').replace(' ', '').replace(",device='cuda:0'", '')
    content = content.replace("'boxes'", '')
    content = content.replace("'labels'", '')
    content = content.replace("'scores'", '')
    content = content.replace(":tensor", '')

    content1 = content.split('}')
    # print(content1)

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


def get_video(filename):
    file_name = filename.split('.')[0]
    folder_name = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/tag_picture/", file_name)
    image_extension = '.jpg'
    frame_per_second = 30
    images = []
    for pic in range(len(os.listdir(folder_name))):
        images.append(str(pic + 1) + image_extension)

    frame = cv2.imread(os.path.join(folder_name, images[1]))
    height, width, layers = frame.shape
    size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'MPEG')
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/tag_video/", 'tag_' + file_name) + '.mp4'
    out = cv2.VideoWriter(filepath, 0x7634706d, frame_per_second, size)

    for image in images:
        out.write(cv2.imread(os.path.join(folder_name, image)))

    out.release()
if __name__ == '__main__':
    # get_video('DJI_0547_out.MP4')
    get_video('DJI_0547_out.MP4')