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

if __name__ == '__main__':
    contents = '''
    /home/jcai/DJI_0547_out/212.png
{'boxes': tensor([[2841.7759,  480.6227, 3205.1343, 1460.2932],
        [3002.2854,  701.3279, 3128.7825,  820.3132],
        [ 257.9881,  695.8599,  348.8932,  808.6546],
        [ 172.5657,  525.1677,  381.4815, 1122.7023],
        [ 266.9252,  715.6194,  336.0609,  787.1235],
        [ 290.7675,  697.2819,  351.7250,  786.7068]], device='cuda:0'), 'labels': tensor([1, 3, 3, 1, 3, 3], device='cuda:0'), 'scores': tensor([0.9997, 0.9912, 0.9722, 0.9304, 0.7629, 0.0874], device='cuda:0')}
/home/jcai/DJI_0547_out/133.png
{'boxes': tensor([[1172.9905,  744.4508, 1272.4536,  867.2560],
        [1097.3082,  560.1055, 1291.3790, 1149.1207],
        [1186.3761,  772.0015, 1254.4043,  842.5856]], device='cuda:0'), 'labels': tensor([3, 1, 3], device='cuda:0'), 'scores': tensor([0.9662, 0.8802, 0.7422], device='cuda:0')}
/home/jcai/DJI_0547_out/257.png
{'boxes': tensor([[2331.4844,  467.7040, 2676.5923, 1536.8551],
        [2477.9226,  714.6446, 2611.1060,  842.0335]], device='cuda:0'), 'labels': tensor([1, 3], device='cuda:0'), 'scores': tensor([0.9998, 0.9929], device='cuda:0')}
/home/jcai/DJI_0547_out/172.png
{'boxes': tensor([[3383.4192,  423.8369, 3799.1995, 1709.8464],
        [3541.8215,  705.4402, 3678.6030,  838.2643],
        [ 733.8892,  708.6610,  835.3246,  835.0735],
        [ 662.9111,  532.2111,  857.0561, 1107.9175],
        [ 764.4730,  724.0927,  825.7848,  823.8889],
        [ 741.2740,  725.2961,  804.0698,  822.0750]], device='cuda:0'), 'labels': tensor([1, 3, 3, 1, 3, 3], device='cuda:0'), 'scores': tensor([0.9989, 0.9932, 0.9793, 0.6615, 0.6208, 0.4056], device='cuda:0')}
/home/jcai/DJI_0547_out/192.png
{'boxes': tensor([[3108.0264,  475.7342, 3471.0913, 1541.7426],
        [3253.6780,  700.2975, 3396.1768,  835.8168],
        [ 497.1724,  698.7026,  587.8160,  826.3599],
        [ 413.9886,  513.3654,  621.0415, 1089.8868],
        [ 507.5409,  722.8750,  578.9794,  799.0517]], device='cuda:0'), 'labels': tensor([1, 3, 3, 1, 3], device='cuda:0'), 'scores': tensor([0.9994, 0.9932, 0.9505, 0.9504, 0.7617], device='cuda:0')}
/home/jcai/DJI_0547_out/184.png
{'boxes': tensor([[3215.7058,  479.5688, 3580.5825, 1520.0446],
        [3373.8152,  698.5565, 3501.4797,  815.6759],
        [ 591.3787,  708.8191,  687.7502,  828.4807],
        [ 507.4908,  510.8294,  713.8162, 1116.9734],
        [ 598.9042,  729.5573,  675.5704,  802.9324],
        [ 602.9485,  752.7626,  690.4319,  818.3636]], device='cuda:0'), 'labels': tensor([1, 3, 3, 1, 3, 3], device='cuda:0'), 'scores': tensor([0.9994, 0.9857, 0.9610, 0.7734, 0.6098, 0.0715], device='cuda:0')}
'''
    result = content(contents)
    print(result)
    # content(contents)