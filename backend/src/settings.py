import os
from decouple import config


class FlaskAppConfiguration:
    DEBUG = config('DEBUG', default=False, cast=bool)
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = config('SECRET_KEY')
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    UPLOADED_IMAGES_DEST = os.path.join("static", "images")


VIDEO_SOURCE = config('OPENCV_VIDEO_SOURCE', default=0, cast=int)

DATASET_PATH = os.path.join("static", "images", "dataset")
UNKNOWN_IMAGES_PATH = os.path.join("static", "images", "unknown")

HAAR_CASCADE_PATH = os.path.join("files", "detectors", "haarcascade_frontalface_alt2.xml")
PROTOTXT_PATH = os.path.join("files", "detectors", "deploy.prototxt.txt")
CAFFEMODEL_PATH = os.path.join("files", "detectors", "res10_300x300_ssd_iter_140000.caffemodel")


DLIB_MODEL = "hog"  # hog -> faster but less accurate, cnn -> more accurate but slower
DLIB_TOLERANCE = 0.6  # 0.6 -> default, 0.72 -> strict
ENCODINGS_FILE = os.path.join("files", "encodings.pickle")
