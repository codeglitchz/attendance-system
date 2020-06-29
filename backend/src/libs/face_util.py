import os
import time
import pickle
import datetime
from typing import Union

import csv
import cv2
from imutils import paths
import unicodedata
import numpy as np
import pandas as pd
from PIL import Image
import face_recognition


class FaceUtils:
    app_title = "Attendance System"
    dataset_path = f"static{os.sep}images{os.sep}dataset"
    unknown_images_path = f"static{os.sep}images{os.sep}unknown"

    haar_cascade_path = f"files{os.sep}haarcascade_frontalface_default.xml"
    prototxt_path = f"files{os.sep}dnn{os.sep}deploy.prototxt.txt"
    caffemodel_path = f"files{os.sep}dnn{os.sep}res10_300x300_ssd_iter_140000.caffemodel"

    encodings_file = f"files{os.sep}encodings.pickle"
    dlib_model = "hog"  # or "cnn"
    tolerance = 0.6

    def __init__(self, input_video: Union[int, str]):
        self.input_video = input_video

    def check(self):
        # store input video stream capture in cap variable
        cap = cv2.VideoCapture(self.input_video)
        while cap.isOpened():
            # capture frame-by-frame
            ret, frame = cap.read()
            if ret:  # video is detected
                # display the resulting frame
                cv2.imshow(f"Checking Camera - {self.app_title}", frame)

                k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
                if k == 27:
                    break
            else:  # video not detected
                break
        # when everything is done
        cap.release()
        cv2.destroyAllWindows()

    # helper method ->  to check whether student_id is a number
    @classmethod
    def is_number(cls, _id):
        try:
            float(_id)
            return True
        except ValueError:
            pass
        try:
            unicodedata.numeric(_id)
            return True
        except (TypeError, ValueError):
            pass
        return False

    # Capture Image function definition
    def detect_n_capture(self):
        student_id = input("Enter ID(numbers only): ")
        name = input("Enter Name(alphabets only): ")

        # if "student_id is a number" and "name consists of alphabetic chars only" then
        if self.is_number(student_id) and name.isalpha():
            # store input video stream in cap variable
            cap = cv2.VideoCapture(self.input_video)
            # load our serialized model from disk
            net = cv2.dnn.readNetFromCaffe(prototxt=self.prototxt_path, caffeModel=self.caffemodel_path)
            increment_num = 0
            # loop over the frames from the video stream
            while True:
                # capture frame-by-frame
                ret, img = cap.read()
                if ret:  # video is detected
                    # convert frame to grayscale
                    # gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    # grab the image frame dimensions and convert it to a blob
                    (h, w) = img.shape[:2]
                    blob = cv2.dnn.blobFromImage(
                        cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0)
                    )

                    # pass the blob through the network and obtain the detections and
                    # predictions
                    net.setInput(blob)
                    detections = net.forward()

                    # # detect faces using haar cascade detector
                    # faces = detector.detectMultiScale(gray_frame, 1.3, 5)

                    # loop over the detections
                    for i in range(0, detections.shape[2]):
                        # extract the confidence (i.e., probability) associated with the
                        # prediction
                        confidence = detections[0, 0, i, 2]

                        # filter out weak detections by ensuring the `confidence` is
                        # greater than the minimum confidence
                        if confidence < 0.5:
                            continue

                        # compute the (x, y)-coordinates of the bounding box for the
                        # object
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")

                        # draw the bounding box of the face along with the associated
                        y = startY - 10 if startY - 10 > 10 else startY + 10
                        cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)
                        # # probability
                        # text = "{:.2f}%".format(confidence * 100)
                        # cv2.putText(
                        #     img, text, (startX, y),
                        #     cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2
                        # )

                        # incrementing number
                        increment_num += 1
                        # create a directory for <id> of the student
                        id_path = f"{self.dataset_path}{os.sep}{student_id}"
                        if not os.path.exists(id_path):
                            os.makedirs(id_path)
                        # saving the captured face in the <id> folder under static/images/dataset
                        cv2.imwrite(
                            f"{id_path}{os.sep}{str(increment_num)}.jpg",
                            img[startY:endY, startX:endX]
                        )
                    # display the resulting frame
                    cv2.imshow(f"Capturing Face - {self.app_title}", img)  # gray_frame
                    # wait for 100 milliseconds
                    k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
                    if k == 27:
                        break
                    elif increment_num >= 10:  # Take 30 or 60 face sample and stop video
                        break
                else:  # video not detected
                    break

            # when everything is done
            cap.release()
            cv2.destroyAllWindows()

            # add details in student_details.csv file
            row = [student_id, name]
            with open(f"files{os.sep}student_details.csv", 'a+') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(row)
            csv_file.close()

        else:
            # if student_id input is correct then
            if self.is_number(student_id):
                # ask to input correct alphabetic name
                print("Enter Name(alphabets only): ")

            # if name input is correct then
            if name.isalpha():
                # ask to input correct numeric ID
                print("Enter ID(numbers only): ")

    # helper method -> returns faces and id_list
    @classmethod
    def get_images_and_labels(cls, path):
        # join the path of the parent folder to all image paths
        id_paths = [os.path.join(path, f) for f in os.listdir(path)]
        # print(">>> ID paths:", id_paths)
        # initialize face list
        faces = []
        # initialize ID list
        ids = []
        detector = cv2.CascadeClassifier(cls.haar_cascade_path)

        # now looping through all the image paths and loading the IDs and the images
        for id_path in id_paths:
            # getting the ID from the image
            _id = int(os.path.split(id_path)[1])
            image_paths = [os.path.join(id_path, f) for f in os.listdir(id_path)]
            for image_path in image_paths:
                # loading the image and converting it to gray scale
                pil_image = Image.open(image_path).convert('L')
                # Now we are converting the PIL image into numpy array
                img_numpy = np.array(pil_image, 'uint8')
                # extract the face from the training image sample
                face = detector.detectMultiScale(img_numpy)
                for (x, y, w, h) in face:
                    faces.append(img_numpy[y:y+h, x:x+w])
                    ids.append(_id)
        # print(">>> Faces:", faces)
        # print(">>> IDs:", ids)
        return faces, ids

    @classmethod
    def train(cls):
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        faces, ids = cls.get_images_and_labels(cls.dataset_path)
        recognizer.train(faces, np.array(ids))
        # save the model into files/trainer.yml
        recognizer.save(f"files{os.sep}trainer.yml")
        # recognizer.save  # worked on Mac but not on Pi
        # Print the numer of faces trained and end program
        print("\n [INFO] {0} faces trained.".format(len(np.unique(ids))))

    def recognize_n_attendance(self):
        # reading trained dataset
        recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
        recognizer.read("files" + os.sep + "trainer.yml")

        # using haar cascade
        face_cascade = cv2.CascadeClassifier(self.haar_cascade_path)

        # preparing pandas dataframe
        df = pd.read_csv("files" + os.sep + "student_details.csv")
        col_names = ['ID', 'Name', 'Date', 'Time']
        attendance_df = pd.DataFrame(columns=col_names)

        # store input video stream capture in cap variable
        cam = cv2.VideoCapture(self.input_video)
        font = cv2.FONT_HERSHEY_SIMPLEX

        while True:
            # capture frame-by-frame
            ret, img = cam.read()
            if ret is True:  # video is detected
                # convert frame to grayscale
                # img = cv2.flip(img, -1)  # Flip vertically
                gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # detect faces using haar cascade detector
                faces = face_cascade.detectMultiScale(gray_frame, 1.2, 5)
                for (x, y, w, h) in faces:
                    _id, confidence = recognizer.predict(gray_frame[y:y+h, x:x+w])

                    # you can specify your limit here. Default is 'if confidence < 100:'
                    # but i'm getting  wrong results even with confidence of 97.
                    if confidence < 75:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (225, 0, 0), 2)
                        # detect name from database here from _id
                        confidence_percent = f"  {round(100 - confidence)}"
                        current_time = time.time()
                        date = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d')
                        timestamp = datetime.datetime.fromtimestamp(current_time).strftime('%H:%M:%S')
                        student_name = df.loc[df['ID'] == _id]['Name'].values[0]
                        display_text = student_name
                        # print(">>> Confidence:", confidence)
                        attendance_df.loc[len(attendance_df)] = [_id, student_name, date, timestamp]
                        cv2.putText(img, display_text, (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                        cv2.putText(img, str(confidence_percent), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
                    else:
                        display_text = "Unknown"
                        # confidence_percent = f"  {round(100 - confidence)}"
                        # cv2.rectangle(img, (x, y), (x + w, y + h), (225, 0, 0), 2)
                        # capture unknown images

                        # file_number = len(os.listdir(self.unknown_images_path)) + 1
                        # cv2.imwrite(
                        #     f"{self.unknown_images_path}{os.sep}image_{str(file_number)}.jpg",
                        #     gray_frame[y:y+h, x:x+w]
                        # )
                        # display text on video frame if unknown person detected
                        cv2.putText(img, display_text, (x + 5, y - 5), font, 1, (255, 0, 0), 2)
                        # cv2.putText(img, str(confidence_percent), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
                attendance_df = attendance_df.drop_duplicates(subset=['ID'], keep='first')
                cv2.imshow(f"Recognizing Faces - {self.app_title}", img)
                k = cv2.waitKey(1) & 0xff  # Press 'ESC' for exiting video
                if k == 27:
                    break
            else:  # video not detected
                break

        # get current time and date
        current_time = time.time()
        date = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d')
        timestamp = datetime.datetime.fromtimestamp(current_time).strftime('%H:%M:%S')
        hour, minute, second = timestamp.split(":")

        # create a csv(comma separated value) file and append current date and time to its name
        file_name = f"Attendance{os.sep}{date}_{hour}-{minute}-{second}.csv"
        attendance_df.to_csv(file_name, index=False)

        # when everything is done
        cam.release()
        cv2.destroyAllWindows()
        print("Attendance Successful!")

    @classmethod
    def create_encodings(cls):
        # grab the paths to the input images in our dataset
        print("[INFO] quantifying faces...")
        image_paths = list(paths.list_images(cls.dataset_path))

        # initialize the list of known encodings and known names
        known_encodings = []
        known_ids = []

        # load our serialized model from disk
        net = cv2.dnn.readNetFromCaffe(prototxt=cls.prototxt_path, caffeModel=cls.caffemodel_path)

        # loop over the image paths
        for (index, image_path) in enumerate(image_paths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(index + 1, len(image_paths)))
            _id = image_path.split(os.path.sep)[-2]

            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(image_path)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # grab the image frame dimensions and convert it to a blob
            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(
                cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0)
            )

            # pass the blob through the network and obtain the detections and
            # predictions
            net.setInput(blob)
            detections = net.forward()

            # loop over the detections
            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence < 0.5:
                    continue

                # compute the (x, y)-coordinates of the bounding box for the
                # object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # detect the (x, y)-coordinates of the bounding boxes
                # corresponding to each face in the input frame, then compute
                # the facial embeddings for each face
                boxes = [(startY, endX, endY, startX)]
                # compute the facial embedding for the face
                encodings = face_recognition.face_encodings(rgb, boxes)

                # loop over the encodings
                for encoding in encodings:
                    # add each encoding + name to our set of known names and
                    # encodings
                    known_encodings.append(encoding)
                    known_ids.append(_id)

        # dump the facial encodings + names to disk
        print("[INFO] serializing encodings...")
        data = {"encodings": known_encodings, "ids": known_ids}
        f = open(cls.encodings_file, "wb")
        f.write(pickle.dumps(data))
        f.close()

    def recognize_dlib(self):
        print("[INFO] loading encodings...")
        data = pickle.loads(open(self.encodings_file, "rb").read())

        print("[INFO] starting video stream...")
        # store input video stream in cap variable
        cap = cv2.VideoCapture(self.input_video)
        # load our serialized model from disk
        net = cv2.dnn.readNetFromCaffe(prototxt=self.prototxt_path, caffeModel=self.caffemodel_path)

        # loop over the frames from the video stream
        while True:
            # grab the frame from the video stream
            ret, img = cap.read()

            # convert the input frame from BGR to RGB then resize it to have
            # a width of 750px (to speedup processing)
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # rgb = imutils.resize(img, width=750)
            r = img.shape[1] / float(rgb.shape[1])

            # grab the image frame dimensions and convert it to a blob
            (h, w) = img.shape[:2]
            blob = cv2.dnn.blobFromImage(
                cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0)
            )

            # pass the blob through the network and obtain the detections and
            # predictions
            net.setInput(blob)
            detections = net.forward()

            # loop over the detections
            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence < 0.5:
                    continue

                # compute the (x, y)-coordinates of the bounding box for the
                # object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # detect the (x, y)-coordinates of the bounding boxes
                # corresponding to each face in the input frame, then compute
                # the facial embeddings for each face
                boxes = [(startY, endX, endY, startX)]

                encodings = face_recognition.face_encodings(rgb, boxes)
                ids = []

                # loop over the facial embeddings
                for encoding in encodings:
                    # attempt to match each face in the input image to our known
                    # encodings
                    matches = face_recognition.compare_faces(data["encodings"], encoding, self.tolerance)
                    _id = "Unknown"

                    # check to see if we have found a match
                    if True in matches:
                        # find the indexes of all matched faces then initialize a
                        # dictionary to count the total number of times each face
                        # was matched
                        matched_indexes = [i for (i, b) in enumerate(matches) if b]
                        counts = {}

                        # loop over the matched indexes and maintain a count for
                        # each recognized face
                        for matched_index in matched_indexes:
                            _id = data["ids"][matched_index]
                            counts[_id] = counts.get(_id, 0) + 1

                        # determine the recognized face with the largest number
                        # of votes (note: in the event of an unlikely tie Python
                        # will select first entry in the dictionary)
                        _id = max(counts, key=counts.get)
                    # update the list of names
                    ids.append(_id)
                # loop over the recognized faces
                for ((top, right, bottom, left), name) in zip(boxes, ids):
                    # rescale the face coordinates
                    top = int(top * r)
                    right = int(right * r)
                    bottom = int(bottom * r)
                    left = int(left * r)
                    top_left = (left, top)
                    bottom_right = (right, bottom)

                    # draw the predicted face name on the image
                    cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
                    y = top - 15 if top - 15 > 15 else top + 15
                    cv2.putText(img, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            # display the output frames to the screen
            cv2.imshow(f"Recognizing Faces - {self.app_title}", img)
            k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting from the loop
            if k == 27:
                break

        # do a bit of cleanup
        cap.release()
        cv2.destroyAllWindows()
