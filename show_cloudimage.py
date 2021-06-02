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

if __name__ == '__main__':
    # load_data
    df = pd.read_excel(r'data_show_cloudimage/station_info_jilin.xlsx', sheet_name='光伏', index_col=0)
    df.columns = ['CAP', 'Lat', 'Lon', 'NWP_ID']

    with open('data_show_cloudimage/pixel_pos_relative.pkl', 'rb') as f:
        pixel_pos = pickle.load(f)

    dict_pixel_pos = {}

    for k in range(len(df)):
        dict_pixel_pos[df.index[k]] = pixel_pos[k]

    # 云检测
    ID_sta = 520
    sample_time = datetime.datetime(2018, 6, 19, 12, 0, 0)
    dir_image = "cloudimage_2018_06_19"

    im0,im1 = load_image(dir_image, sample_time)

    target = list(map(int, dict_pixel_pos[ID_sta]))

    target = [target[1], target[0]]

    points = search_points(im1, target)

    if points:

        # 速度计算

        v = {}

        time_interval = (im1.time - im0.time).seconds

        #     print(points)

        for label in points:
            x, y = points[label]

            v[label] = cloud_move(im0.image, im1.image, x, y)

        df_v = pd.DataFrame(v).T * 500 / time_interval

        df_v.columns = ["x", "y"]

    import matplotlib.patches as mpathes

    fig, (ax1) = plt.subplots(1, 1, figsize=(8, 6))

    ax1.imshow(im1.dst, cmap='gray')

    ax1.scatter(target[1], target[0], s=40, c='r', marker='*')

    for theta in points:

        ax1.scatter(points[theta][1], points[theta][0], c='y', s=5)

        ax1.arrow(points[theta][1], points[theta][0], df_v.loc[theta][1] * 10, df_v.loc[theta][0] * 10,
                  length_includes_head=True, color='r',
                  head_width=2, head_length=4, fc='#e87a59', ec='#e87a59')

    # ax1.set_xlabel('像素(500m)')
    # ax1.set_ylabel('像素(500m)')
    ax1.set_xticks([])
    ax1.set_yticks([])

    plt.show()


