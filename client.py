
import tornado
import os
import sys
import zipfile
import requests
import cv2
import numpy as np

post_xiaozhi_url = "http://172.16.1.60:8888/xiaozhi/training"

# 发送图片数据
def send_img(img_name):

    img = cv2.imread(img_name)

    _, img_encode = cv2.imencode('.jpg', img)

    r = requests.post(post_xiaozhi_url, data=img_encode.tobytes())

    result = r.content.decode('utf-8')

    print(result)


# 发送zip包
def send_imgs_zip(imgs_path, zip_file_name):

    # 把存有图片的文件夹压缩成zip文件
    f = zipfile.ZipFile(zip_file_name, 'w')

    for root, dirs, files in os.walk(imgs_path):

        for img_name in files:

            f.write(os.path.join(root, img_name))

    f.close()

    # 发送zip文件的二进制数据
    f_b_zip = open(zip_file_name, "rb")
    r = requests.post(post_xiaozhi_url, f_b_zip)






if __name__ == "__main__":

# send img
    #img_name = "1.jpg"
    #send_img(img_name)


# send zip file
    imgs_dir = "imgs"
    zip_file = "zimgs.zip"
    send_imgs_zip(imgs_dir, zip_file)





