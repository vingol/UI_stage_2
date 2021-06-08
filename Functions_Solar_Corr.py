import os
import cv2
import pickle
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from skimage import measure
from collections import Counter


class Cloud_image(object):

    def __init__(self, time, image, dst):

        self.time = time
        self.image = image
        self.dst = dst

    def get_target_area(self):

        return self.image[0:int(3000), int(11000):int(15000)]

    def get_target_area_dst(self):

        img = self.get_target_area()

        _, target_dst = cv2.threshold(
            np.array(img / img.max() * 255, dtype='uint8'), 0, 255, cv2.THRESH_OTSU)

        return target_dst

    def plot_image(self, ax, dst=False, marker=True, pixel_pos=0):

        if dst:
            ax.imshow(self.get_target_area(), cmap='gray')
        else:
            ax.imshow(self.get_target_area_dst(), cmap='gray')

        if marker:
            for pixel in pixel_pos:
                ax.scatter(pixel[0], pixel[1])
        else:
            pass

    def get_cloud_area(self, ):
        # 得到云团区域
        barrier = 500

        # 各方向均膨胀3格，膨胀后为dilate_
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

        dilate_ = cv2.dilate(self.get_target_area_dst(), kernel, iterations=3)

        opening = cv2.morphologyEx(self.get_target_area_dst(), cv2.MORPH_OPEN, kernel)

        dilate_ = opening

        # 膨胀后的云图的分块结果bwlabel
        bwlabel = measure.label(dilate_)

        # 膨胀后的2分块云图的统计结果
        element_count = Counter(bwlabel.flatten())

        # 寻找面积大于5000像素的区域 sign
        sign = np.where(np.array(list((element_count.values()))) > 50000)[0]

        cloud_area = bwlabel == sign[0]

        sign_cloud = []

        for i in sign:
            cloud_area = cloud_area | (bwlabel == i)

            if dilate_[bwlabel == i][0] == 255:
                sign_cloud.append(i)

        cloud_area = cloud_area & (dilate_ == 255)

        return cloud_area

def load_image(dir_image, sample_time):

    image_times = []

    for file in os.listdir(dir_image):
        image_times.append(name_to_time(file.split('.')[0]))

    image_times.sort()

    ar_image_times = np.array(image_times)

    image_times = ar_image_times[ar_image_times < sample_time][-3:]

    image_names = list(map(time_to_name_pkl, image_times))

    with open(dir_image + '/' + image_names[-2], "rb") as f:
        img = pickle.load(f)

        retval, dst = cv2.threshold(
            np.array(img / img.max() * 255, dtype='uint8'), 0, 255, cv2.THRESH_OTSU)

        im0 = Cloud_image(image_times[-2], img, dst)

    with open(dir_image + '/' + image_names[-1], "rb") as f:
        img = pickle.load(f)

        retval, dst = cv2.threshold(
            np.array(img / img.max() * 255, dtype='uint8'), 0, 255, cv2.THRESH_OTSU)

        im1 = Cloud_image(image_times[-1], img, dst)

    return im0, im1

def name_to_time(name):

    date_time_ = name.split('.')[0]
    date_ = date_time_.split(' ')[0]
    time_ = date_time_.split(' ')[1]

    year = int(date_.split('-')[0])
    month = int(date_.split('-')[1])
    day = int(date_.split('-')[2])
    hour = int(time_.split('_')[0])
    minute = int(time_.split('_')[1])
    second = int(time_.split('_')[2])

    return datetime.datetime(year, month, day, hour, minute, second)

def time_to_name_pkl(sample_time):
    sample_time = sample_time

    date, time = str(sample_time).split(' ')[0], str(sample_time).split(' ')[1]

    return '-'.join(date.split('-')) + ' ' +'_'.join(time.split(':')) + '.pkl'

def is_in_cloud(im1, target):
    taregt_mean_gray_value = im1.dst[target[0] - 60:target[0] + 60, target[1] - 60:target[1] + 60].mean() / 255

    if taregt_mean_gray_value < 0.2:
        return False
    else:
        return True

def search_points(im1, target):
    in_cloud = is_in_cloud(im1, target)

    points = {}

    for theta in np.arange(0, (np.pi) * 2, (np.pi) / 12):

        for i in range(800):

            temper = ((target[0] + np.sin(theta) * i).astype(int), (target[1] + np.cos(theta) * i).astype(int))

            # 选定坐标周围区域
            x = temper[0]
            y = temper[1]

            x1 = max(x - 60, 2)
            x2 = x + 60
            y1 = max(y - 60, 2)
            y2 = y + 60

            search_area = im1.dst[x1:x2, y1:y2]

            #         if (dilate_[temper]) & (search_area.mean()/255 > 0):

            if in_cloud:

                if search_area.mean() / 255 < 0.2:
                    points[theta] = temper

                    break
            else:
                if search_area.mean() / 255 > 0.2:
                    points[theta] = temper

                    break

    return points

def cloud_move(im1, im2, x, y):
    im1 = im1.astype('double')
    im2 = im2.astype('double')

    f = lambda x: max(x, 0)

    # 选定坐标周围区域
    x1 = max(x - 60, 2)
    x2 = x + 60
    y1 = max(y - 60, 2)
    y2 = y + 60

    region_1 = im1[x1:x2, y1:y2]

    diff = []
    x_v = []
    y_v = []

    for i in range(-80, 80):
        for j in range(-80, 80):
            region_2 = im2[f(x1 - 1 + i):f(x2 - 1 + i), f(y1 - 1 + j):f(y2 - 1 + j)]

            diff.append(np.abs(region_1 - region_2).sum())

            x_v.append(i)
            y_v.append(j)

    index = np.array(diff).argmin()

    return x_v[index], y_v[index]

import math
# 逆时针旋转
def Nrotate(angle, valuex, valuey, pointx, pointy):

    angle = (angle/180)*math.pi
    valuex = np.array(valuex)
    valuey = np.array(valuey)
    nRotatex = (valuex-pointx)*math.cos(angle) - \
        (valuey-pointy)*math.sin(angle) + pointx
    nRotatey = (valuex-pointx)*math.sin(angle + \
        (valuey-pointy)*math.cos(angle) + pointy
    return (nRotatex, nRotatey)
# 顺时针旋转
def Srotate(angle, valuex, valuey, pointx, pointy):
    angle = (angle/180)*math.pi
    valuex = np.array(valuex)
    valuey = np.array(valuey)
    sRotatex = (valuex-pointx)*math.cos(angle) + \
        (valuey-pointy)*math.sin(angle) + pointx
    sRotatey = (valuey-pointy)*math.cos(angle) - \
        (valuex-pointx)*math.sin(angle) + pointy
    return (sRotatex, sRotatey)
# 将四个点做映射
def rotatecordiate(angle, rectboxs, pointx, pointy):
    output = []
    for rectbox in rectboxs:
        if angle > 0:
            output.append(
                Srotate(angle, rectbox[0], rectbox[1], pointx, pointy))
        else:
            output.append(
                Nrotate(-angle, rectbox[0], rectbox[1], pointx, pointy))
    return output

def imagecrop(image,box):
    xs = [x[1] for x in box]
    ys = [x[0] for x in box]
    print(xs)
    print(min(xs),max(xs),min(ys),max(ys))
    cropimage = image[min(xs):max(xs),min(ys):max(ys)]
    print(cropimage.shape)
    cv2.imwrite('cropimage.png',cropimage)
    return cropimage

def cloud_move_rotated(im1, im2, box_):
    im1 = im1.astype('double')
    im2 = im2.astype('double')

    f = lambda x: max(x, 0)

    # 选定坐标周围区域
    xs = list(zip(*np.int0(box_)))[0]
    ys = list(zip(*np.int0(box_)))[1]

    # 此处已将坐标转位索引坐标的格式

    x1 = min(ys)
    x2 = max(ys)
    y1 = min(xs)
    y2 = max(xs)

    region_1 = im1[x1:x2, y1:y2]

    diff = []
    x_v = []
    y_v = []

    for i in range(-80, 80):
        for j in range(-80, 80):
            region_2 = im2[f(x1 - 1 + i):f(x2 - 1 + i), f(y1 - 1 + j):f(y2 - 1 + j)]

            diff.append(np.abs(region_1 - region_2).sum())

            x_v.append(i)
            y_v.append(j)

    index = np.array(diff).argmin()

    return x_v[index], y_v[index]

def search_cloud_by_v(im1, target, v_search_cloud, in_cloud=False):
    mod_v = np.linalg.norm(v_search_cloud)

    for i in range(800):

        temper = ((target[0] - v_search_cloud[0] * i / mod_v).astype(int),
                  (target[1] - v_search_cloud[1] * i / mod_v).astype(int))

        # 选定坐标周围区域
        x = temper[0]
        y = temper[1]

        x1 = max(x - 60, 2)
        x2 = x + 60
        y1 = max(y - 60, 2)
        y2 = y + 60

        search_area = im1.dst[x1:x2, y1:y2]

        #         if (dilate_[temper]) & (search_area.mean()/255 > 0):
        if in_cloud:

            if search_area.mean() / 255 < 0.1:
                cloud_to_station = temper

                break
        else:
            if search_area.mean() / 255 > 0.1:
                cloud_to_station = temper

                break

    return cloud_to_station