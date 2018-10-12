import os
import sys
import tornado.web
import json
import logging
#import requests
import zipfile
import cv2
import numpy as np



WORK_DIR = os.path.dirname(os.path.abspath(__file__))


# 创建log文件
def creat_log_file():
    targetDirect = WORK_DIR + "/log"
    log_file_name = targetDirect + "/xiaozhi.log"

    # 创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    # 创建一个handler，写入日志文件
    file_handler = logging.FileHandler(log_file_name, mode='a+')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # 创建handler, 在控制台打印日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.formatter = formatter

    # 添加handler到logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


total_logger = creat_log_file()


# 解压客户端发送过来的zip二进制文件 
def un_zip(zip_data, imgs_path):

    zimgs_file_name = os.path.join(WORk_DIR, "zimgs.zip")
    f = open(zimgs_file_name, "wb")
    f.write(zip_data)
    f.close()

    zip_f = zipfile.ZipFile(zimgs_file_name, 'r')
    if os.path.isdir(imgs_path):
        pass
    else:
        os.mkdir(imgs_path)

    for names in zip_f.namelist():
        zip_f.extract(names, imgs_path)
    zip_f.close()

    os.remove(zimgs_file_name)


class Face_Detecting(tornado.web.RequestHandler):

    def post(self):

        total_logger.info(".........face_detecting request starts............")

        try:
            img_buf = np.frombuffer(self.request.body, dtype=np.uint8)
            img = cv2.imdecode(img_buf, 1)

        except Exception as ex:
            self.finsh({"request body error!!!"})

        # to do
        # result format: {"M":True, "L":False, "R":False}
        result = get_result()

        self.finish(result)



class Emotion_Face_Recognition(tornado.web.RequestHandler):

    def get(self):

        total_logger.info( ".........emotion_recognition request starts.........")

        # to do
        img = get_img()
        
        # to do
        # result format: [{"name":id1, "expression":{}},...]
        result = get_results() 

        # add img_data
        _, img_encode = cv2.imencode('.jpg', img)
        img_data = img_encode.tobytes()
        result.append({"img":img_data})

        self.finish(result)




class Training(tornado.web.RequestHandler):

    def post(self):

        total_logger.info(".........training request starts.........")

        try:
            zip_b_data = self.request.body
            imgs_path = os.path.join(WORK_DIR, "imgs")
            un_zip(zip_b_data, imgs_path)

        except Exception as ex:
            self.finish("unzip imgs error!!!")
        
        # to do
        # result format: {"sucess": True}
        result = training()
        self.finish(result)


class Get_Version(tornado.web.RequestHandler):

    def get(self):

        version = "1.0.0"

        self.finish(version)




if __name__ == "__main__":

    application = tornado.web.Application([
        (r'/xiaozhi/face_detecting', Face_Detecting),
        (r'/xiaozhi/emotion_face_recognition', Emotion_Face_Recognition),
        (r'/xiaozhi/training', Training),
        (r'/xiaozhi/get_version', Get_Version)
    ])

    application.listen(8888)

    tornado.ioloop.IOLoop.current().start()






