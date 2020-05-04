import os
import cv2
import numpy as np
from PIL import Image


# -------------- image labels ------------------------

# returns faces and id_list
def get_images_and_labels(path):
    # get the path of all the files in the folder
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empty Face list
    faces = []
    # create empty ID list
    id_list = []

    # now looping through all the image paths and loading the IDs and the images
    for image_path in image_paths:
        # loading the image and converting it to gray scale
        pil_image = Image.open(image_path).convert('L')
        # Now we are converting the PIL image into numpy array
        image_np = np.array(pil_image, 'uint8')
        # getting the ID from the image
        _id = int(os.path.split(image_path)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(image_np)
        id_list.append(_id)
    return faces, id_list


# ----------- train images function ---------------
def train():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    # haar_cascade_path = "files" + os.sep + "haarcascade_frontalface_default.xml"
    # detector = cv2.CascadeClassifier(haar_cascade_path)
    faces, _id = get_images_and_labels("training_images")
    recognizer.train(faces, np.array(_id))
    recognizer.save("files" + os.sep + "trainer.yml")
    print("Images Trained Successfully")
