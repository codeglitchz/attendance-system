import os
from decouple import config


class FlaskAppConfiguration:
    DEBUG = config('DEBUG', default=False, cast=bool)
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = config('SECRET_KEY')
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')


VIDEO_SOURCE = config('OPENCV_VIDEO_SOURCE', default=0, cast=int)

DATASET_PATH = f"static{os.sep}images{os.sep}dataset"
UNKNOWN_IMAGES_PATH = f"static{os.sep}images{os.sep}unknown"

HAAR_CASCADE_PATH = f"files{os.sep}detectors{os.sep}haarcascade_frontalface_alt2.xml"
PROTOTXT_PATH = f"files{os.sep}detectors{os.sep}deploy.prototxt.txt"
CAFFEMODEL_PATH = f"files{os.sep}detectors{os.sep}res10_300x300_ssd_iter_140000.caffemodel"


DLIB_MODEL = "hog"  # hog -> faster but less accurate, cnn -> more accurate but slower
DLIB_TOLERANCE = 0.6  # 0.6 -> default, 0.72 -> strict
ENCODINGS_FILE = f"files{os.sep}encodings.pickle"
