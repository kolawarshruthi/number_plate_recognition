# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 15:16:53 2020

@author: 91807
"""
import torch
from torch.autograd import Variable
import cv2
from data import BaseTransform, VOC_CLASSES as labelmap
from ssd import build_ssd
import imageio

def detect(frame, net, transform):
    height, width = frame.shape[:2]
    frame_t = transform(frame)[0]
    x = torch.from_numpy(frame_t).permute(2, 0, 1)
    x = Variable(x.unsqueeze(0))
    y = net(x)
    detections = y.data
    scale = torch.Tensor([width, height, width, height])
    images = []
    for i in range(detections.size(1)):
        j = 0
        while detections[0, i, j, 0] >= 0.6:
            pt = (detections[0, i, j, 1:]*scale).numpy()
            new_image = frame[int(pt[1]) : int(pt[3]), int(pt[0]) : int(pt[2]), :]
            images.append(new_image)
            cv2.rectangle(frame, (int(pt[0]), int(pt[1])), (int(pt[2]), int(pt[3])), (255, 0 , 0), 2)
            text = labelmap[i-1] + '(' + str(detections[0, i, j, 0]) + ')'
            cv2.putText(frame, text, (int(pt[0]), int(pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
            j += 1
    return images

'''
net = build_ssd('test', 300, 3)
net.load_state_dict(torch.load('ssd300_0712_5000.pth', map_location = lambda storage, loc : storage))

transform = BaseTransform(net.size, (104/256.0, 117/256.0, 123/256.0))


reader = imageio.get_reader('video.mp4')
fps = reader.get_meta_data()['fps']
writer = imageio.get_writer('output_video.mp4', fps = fps)
for i, frame in enumerate(reader):
    frame = detect(frame, net.eval(), transform)
    writer.append_data(frame)
    print(i)
writer.close() 


frame = cv2.imread('1.jpg')
frame = detect(frame, net.eval(), transform, 9)
cv2.imwrite('output_1.jpg', frame)            
'''
