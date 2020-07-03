import os
import pickle
from typing import Union
from datetime import date as dt

import cv2
import numpy as np
import face_recognition

from src.models import StudentModel, AttendanceModel
from src.settings import (
    DATASET_PATH,
    HAAR_CASCADE_PATH, PROTOTXT_PATH, CAFFEMODEL_PATH,
    DLIB_MODEL, DLIB_TOLERANCE, ENCODINGS_FILE
)


class CliAppUtils:
    app_title = "Attendance System"

    def __init__(self, input_video: Union[int, str]):
        self.input_video = input_video

    def check(self):
        # store input video stream capture in cap variable
        cap = cv2.VideoCapture(self.input_video)
        while cap.isOpened():
            # capture frame-by-frame
            ret, frame = cap.read()
            if not ret:  # video is not detected
                continue
            # display the resulting frame
            cv2.imshow(f"Checking Camera - {self.app_title}", frame)

            k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break
        # when everything is done
        cap.release()
        cv2.destroyAllWindows()

    @classmethod
    def save_n_create(cls, name: str) -> str:
        student = StudentModel(name=name)
        # save student to database
        student.save_to_db()

        # create a directory for <id> of the student
        id_path = f"{DATASET_PATH}{os.sep}{student.id}"
        if not os.path.exists(id_path):
            os.makedirs(id_path)
        return id_path

    # Capture Image function definition
    def detect_n_capture(self):
        name = input("Enter Student's Name: ")

        id_path = self.save_n_create(name)
        # store input video stream in cap variable
        cap = cv2.VideoCapture(self.input_video)
        face_classifier = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
        increment_num = 0

        # loop over the frames from the video stream
        while True:
            # capture frame-by-frame
            ret, img = cap.read()
            if not ret:  # video is not detected
                break
            # detect faces using haar cascade detector
            faces = face_classifier.detectMultiScale(img, 1.0485258, 6)

            for(x, y, w, h) in faces:
                increment_num += 1

                # saving the captured face in the <id> folder under static/images/dataset
                cv2.imwrite(
                    f"{id_path}{os.sep}{str(increment_num)}.jpg",
                    img
                )  # img[startY:endY, startX:endX]
                # draw the bounding box of the face along with the associated
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                # display the resulting frame
                cv2.imshow(f"Capturing Face - {self.app_title}", img)
            # wait for 100 milliseconds
            k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break
            elif increment_num >= 15:  # Take 30 or 60 face sample and stop video
                break

        # when everything is done
        cap.release()
        cv2.destroyAllWindows()

    @classmethod
    def train_classifier(cls):
        """
        Train KNN Classifier by storing results in `files/encodings.pickle` file
        """
        # TODO: Store encodings in SQL database rather than `files/encodings.pickle` file
        try:
            print("[INFO] loading encodings...")
            data = pickle.loads(open(ENCODINGS_FILE, "rb").read())
            # initialize the list of known encodings and known names
            known_encodings = data["encodings"]
            known_ids = data["ids"]
        except FileNotFoundError:
            # initialize the list of known encodings and known names
            known_encodings = []
            known_ids = []

        # get single unique ids by converting into set
        # for each _id convert it into int
        unique_ids = [int(_id) for _id in set(known_ids)]

        # get all id_paths and join the path of the parent folder to each id_path
        id_paths = [os.path.join(DATASET_PATH, f) for f in os.listdir(DATASET_PATH)]
        # print(">>> ID paths:", id_paths)

        # now looping through all the id_paths and loading the images in that id_path
        for id_path in id_paths:
            # getting the ID from the image
            _id = int(os.path.split(id_path)[1])
            if _id in unique_ids:
                continue
            # grab the paths to the input images of that ID
            image_paths = [os.path.join(id_path, f) for f in os.listdir(id_path)]
            for i, image_path in enumerate(image_paths):
                print(f"[INFO] ID: {_id}, processing image {i + 1}/{len(image_paths)}")
                # load the input image and convert it from RGB (OpenCV ordering)
                # to dlib ordering (RGB)
                image = cv2.imread(image_path)
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # detect the (x, y)-coordinates of the bounding boxes
                # corresponding to each face in the input frame, then compute
                # the facial embeddings for each face
                boxes = face_recognition.face_locations(rgb, model=DLIB_MODEL)
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
        f = open(ENCODINGS_FILE, "wb")
        f.write(pickle.dumps(data))
        f.close()

    # def recognize_n_attendance_dnn(self):
    #     print("[INFO] loading encodings...")
    #     data = pickle.loads(open(ENCODINGS_FILE, "rb").read())
    #     # print(len(data['encodings']) == len(data['ids']))
    #
    #     print("[INFO] starting video stream...")
    #     # store input video stream in cap variable
    #     cap = cv2.VideoCapture(self.input_video)
    #     # load our serialized model from disk
    #     net = cv2.dnn.readNetFromCaffe(prototxt=PROTOTXT_PATH, caffeModel=CAFFEMODEL_PATH)
    #
    #     # find if today's attendance exists in the database
    #     attendance = AttendanceModel.find_by_date(date=dt.today())
    #     # if not
    #     if attendance is None:
    #         # create new instance for today's attendance
    #         attendance = AttendanceModel()
    #
    #     # loop over the frames from the video stream
    #     while True:
    #         # grab the frame from the video stream
    #         ret, img = cap.read()
    #
    #         # convert the input frame from BGR to RGB then resize it to have
    #         # a width of 750px (to speedup processing)
    #         rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #         # rgb = imutils.resize(img, width=750)
    #         r = img.shape[1] / float(rgb.shape[1])
    #
    #         # grab the image frame dimensions and convert it to a blob
    #         (h, w) = img.shape[:2]
    #         blob = cv2.dnn.blobFromImage(
    #             cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0)
    #         )
    #
    #         # pass the blob through the network and obtain the detections and
    #         # predictions
    #         net.setInput(blob)
    #         detections = net.forward()
    #
    #         # loop over the detections
    #         for i in range(0, detections.shape[2]):
    #             # extract the confidence (i.e., probability) associated with the
    #             # prediction
    #             confidence = detections[0, 0, i, 2]
    #
    #             # filter out weak detections by ensuring the `confidence` is
    #             # greater than the minimum confidence
    #             if confidence < 0.5:
    #                 continue
    #
    #             # compute the (x, y)-coordinates of the bounding box for the
    #             # object
    #             box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
    #             (startX, startY, endX, endY) = box.astype("int")
    #
    #             # detect the (x, y)-coordinates of the bounding boxes
    #             # corresponding to each face in the input frame, then compute
    #             # the facial embeddings for each face
    #             boxes = [(startY, endX, endY, startX)]
    #
    #             encodings = face_recognition.face_encodings(rgb, boxes)
    #             names = []
    #
    #             # loop over the facial embeddings
    #             for encoding in encodings:
    #                 # attempt to match each face in the input image to our known encodings
    #                 matches = face_recognition.compare_faces(data["encodings"], encoding, DLIB_TOLERANCE)
    #                 # name to be displayed on video
    #                 display_name = "Unknown"
    #
    #                 # check to see if we have found a match
    #                 if True in matches:
    #                     # find the indexes of all matched faces then initialize a
    #                     # dictionary to count the total number of times each face
    #                     # was matched
    #                     matched_indexes = [i for (i, b) in enumerate(matches) if b]
    #                     counts = {}
    #
    #                     # loop over the matched indexes and maintain a count for
    #                     # each recognized face
    #                     for matched_index in matched_indexes:
    #                         _id = data["ids"][matched_index]
    #                         counts[_id] = counts.get(_id, 0) + 1
    #
    #                     # determine the recognized face with the largest number
    #                     # of votes (note: in the event of an unlikely tie Python
    #                     # will select first entry in the dictionary)
    #                     _id = max(counts, key=counts.get)
    #                     if _id:
    #                         # find matched student in the database by id
    #                         student = StudentModel.find_by_id(_id)
    #                         # if student's attendance is not marked
    #                         if not attendance.is_marked(student):
    #                             # then mark student's attendance
    #                             attendance.students.append(student)
    #                             # commit changes to database
    #                             attendance.save_to_db()
    #                         # update displayed name to student's name
    #                         display_name = student.name
    #                 # append the name to be displayed in names list
    #                 names.append(display_name)
    #             # loop over the recognized faces
    #             for ((top, right, bottom, left), display_name) in zip(boxes, names):
    #                 if display_name == "Unknown":
    #                     continue
    #                 # rescale the face coordinates
    #                 top = int(top * r)
    #                 right = int(right * r)
    #                 bottom = int(bottom * r)
    #                 left = int(left * r)
    #                 top_left = (left, top)
    #                 bottom_right = (right, bottom)
    #
    #                 # draw the predicted face name on the image
    #                 cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
    #                 y = top - 15 if top - 15 > 15 else top + 15
    #                 cv2.putText(img, display_name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    #
    #         # display the output frames to the screen
    #         cv2.imshow(f"Recognizing Faces - {self.app_title}", img)
    #         k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting from the loop
    #         if k == 27:
    #             break
    #
    #     # do a bit of cleanup
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     print("Attendance Successful!")

    def recognize_n_attendance(self):
        print("[INFO] loading encodings...")
        data = pickle.loads(open(ENCODINGS_FILE, "rb").read())
        # print(len(data['encodings']) == len(data['ids']))

        print("[INFO] starting video stream...")
        # store input video stream in cap variable
        cap = cv2.VideoCapture(self.input_video)

        # find if today's attendance exists in the database
        attendance = AttendanceModel.find_by_date(date=dt.today())
        # if not
        if attendance is None:
            # create new instance for today's attendance
            attendance = AttendanceModel()

        # create in dictionary for known students from database to avoid multiple queries
        known_students = {}

        # loop over the frames from the video stream
        while True:
            # grab the frame from the video stream
            ret, img = cap.read()

            # convert the input frame from BGR to RGB then resize it to have
            # a width of 750px (to speedup processing)
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # rgb = imutils.resize(img, width=750)
            r = img.shape[1] / float(rgb.shape[1])

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input frame, then compute
            # the facial embeddings for each face
            boxes = face_recognition.face_locations(rgb, model=DLIB_MODEL)

            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []

            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known encodings
                matches = face_recognition.compare_faces(data["encodings"], encoding, DLIB_TOLERANCE)
                # name to be displayed on video
                display_name = "Unknown"

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
                    if _id:
                        if _id in known_students.keys():
                            # find matched student in the known_students by id
                            student = known_students[_id]
                        else:
                            # find matched student in the database by id
                            student = StudentModel.find_by_id(_id)
                            known_students[_id] = student
                        # if student's attendance is not marked
                        if not attendance.is_marked(student):
                            # then mark student's attendance
                            attendance.students.append(student)
                            # commit changes to database
                            attendance.save_to_db()
                        # update displayed name to student's name
                        display_name = student.name
                # append the name to be displayed in names list
                names.append(display_name)
            # loop over the recognized faces
            for ((top, right, bottom, left), display_name) in zip(boxes, names):
                if display_name == "Unknown":
                    continue
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
                cv2.putText(img, display_name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            # display the output frames to the screen
            cv2.imshow(f"Recognizing Faces - {self.app_title}", img)
            k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting from the loop
            if k == 27:
                break

        # do a bit of cleanup
        cap.release()
        cv2.destroyAllWindows()
        print("Attendance Successful!")
