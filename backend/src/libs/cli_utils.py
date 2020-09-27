import os
import pickle
from typing import Union
from datetime import date as dt

import cv2
import face_recognition

from src.models import StudentModel, AttendanceModel
from src.settings import (
    DATASET_PATH,
    HAAR_CASCADE_PATH,
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

    def recognize_n_attendance(self):
        print("[INFO] loading encodings...")
        data = pickle.loads(open(ENCODINGS_FILE, "rb").read())
        # print(len(data['encodings']) == len(data['ids']))

        print("[INFO] starting video stream...")
        # store input video stream in cap variable
        cap = cv2.VideoCapture(self.input_video)

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
                            if not AttendanceModel.is_marked(dt.today(), student):
                                # then mark student's attendance
                                student_attendance = AttendanceModel(student=student)
                                # commit changes to database
                                student_attendance.save_to_db()
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
