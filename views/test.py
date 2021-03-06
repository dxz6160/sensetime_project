# with open('static/files/out.txt', 'r') as f:
#     content = f.read()
#
# # content = content.strip().replace('\n', '')
# content = content.replace('\n','').replace(' ','').replace(",device='cuda:0'", '')
# content = content.replace("'boxes'",'')
# content = content.replace("'labels'",'')
# content = content.replace("'scores'",'')
# content = content.replace(":tensor",'')
#
# content1 = content.split('}')
#
# dic = {}
#
# for content2 in content1[:-1]:
#     id = content2.split('{')[0]
#     content3 = content2.split('{')[1].strip('(').split(')')
#     boxes = content3[0].strip('[').strip(']').split('],[')
#     lables = content3[1].strip(',(').strip('[').strip(']').split(',')
#     scores = content3[2].strip(',(').strip('[').strip(']').split(',')
#     result = zip(boxes, lables, scores)
#     dic[int(id)] = list(result)
#
# final = sorted(dic.items(), key=lambda obj: obj[0])
#
# for i in final:
#     print(i[0])
#     for j in i[1]:
#         print(j)

#     content2 = content1.split('{')[1]
#     content2 = content2.split(':')
#     boxes = content2[1]
#     lables = content2[2]
#
#     for content3 in content2:
#         print(content3)

# for content_1 in contents_1:
#     print(content_1)


# result = content.split('}')

# print(content)
# print(result)

# for i  in range(5):
#     print(i)
# import os
#
# for filename in os.listdir(r'C:\Users\61609\PycharmProjects\sensetime_project\static\out_picture\DJI_0547_out'):
#     print(filename)

import cv2
import numpy
import os
import ast
import glob

def tag_picture(filename, result):
    sourceFileName = filename.split('.')[0]
    outPutDirName = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/tag_picture/", sourceFileName) + "/"
    if not os.path.exists(outPutDirName):
        os.makedirs(outPutDirName)
    times = 1
    picture_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/out_picture/", sourceFileName) + "/"
    path_list = os.listdir(picture_path)
    path_list.sort(key=lambda x: int(x.split('.')[0]))
    for file in path_list:
        file_path = os.path.join(picture_path, file)
        local = result[times - 1][1]
        img = cv2.imread(file_path)
        for tag in local:
            try:
                x1 = int(tag[0].split(',')[0].split('.')[0])
                y1 = int(tag[0].split(',')[1].split('.')[0])
                x2 = int(tag[0].split(',')[2].split('.')[0])
                y2 = int(tag[0].split(',')[3].split('.')[0])
            except:
                x1 = x2 = y1 = y2 = 0
            type = tag[1]
            print(type)
            confident = tag[2]
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 4)
            font = cv2.FONT_HERSHEY_COMPLEX_SMALL
            text = 'type:{} confident:{}'.format(type, confident)
            cv2.putText(img, text, (x1, y1 + 100), font, 2, (0, 0, 255), 2)
        cv2.imwrite(outPutDirName + 'image' + str(times) + '.jpg', img)
        times += 1


    # pass

# for path in paths:
#         # local = result[times - 1][1]
#         # print(local)
#         img = cv2.imread(path)
#         print(img)
#         # for tag in local:
#         #     try:
#         #         x1 = int(tag[0].split(',')[0].split('.')[0])
#         #         y1 = int(tag[0].split(',')[1].split('.')[0])
#         #         x2 = int(tag[0].split(',')[2].split('.')[0])
#         #         y2 = int(tag[0].split(',')[3].split('.')[0])
#         #     except:
#         #         x1 = x2 = y1 = y2 = 0
#         #     type = tag[1]
#         #     confident = tag[2]
#         #     cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 4)
#         #     font = cv2.FONT_HERSHEY_COMPLEX_SMALL
#         #     text = 'type:{} confident:{}'.format(type, confident)
#         #     cv2.putText(img, text, (x1, y1 + 100), font, 2, (0, 0, 255), 2)
#         cv2.imwrite(outPutDirName + 'image' + str(times) + '.jpg', img)
#         # times += 1


def get_video(filename):
    project_path = os.path.join(os.path.dirname(os.path.dirname(__file__)))
    filename = filename.split('.')[0]
    cmd = "ffmpeg -i {}/static/tag_picture/{}/image%d.jpg {}/static/tag_video/tag_{}.mp4".format(project_path, filename, project_path, filename)
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    # with open('../static/out/video_20201019dOSz.txt', 'r', encoding='utf-8') as f:
    #     result = f.read()
    #     result = ast.literal_eval(result)
    # # print(type(result))
    # # print(result)
    # tag_picture('video_20201019dOSz.txt', result)
    # get_video('video_20201019dOSz.txt')
    import os

    print((os.path.dirname(os.path.dirname(__file__))))
    print(os.path.dirname(__file__))