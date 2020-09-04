import cv2
import os

# video_path = os.path.join("", "", 'DJI_0547_out.mp4')
#
# print(video_path)
#
# camera = cv2.VideoCapture(video_path)
#
# fps = camera.get(cv2.CAP_PROP_FPS)
#
# print(round(fps))
folder_name = 'C:/Users/61609/PycharmProjects/sensetime_project\static/tag_video/DJI_0547_out'

for pic in range(len(os.listdir(folder_name))):
    print(pic)