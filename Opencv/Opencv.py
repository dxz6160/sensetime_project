import os
import cv2
import numpy as np

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
