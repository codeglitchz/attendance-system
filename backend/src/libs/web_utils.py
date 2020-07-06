import pickle
from typing import Dict
from datetime import date as dt

import cv2
import imutils
import numpy as np
import face_recognition

from src.settings import (
    DLIB_MODEL, DLIB_TOLERANCE,
    ENCODINGS_FILE
)
from src.libs.base_camera import BaseCamera
from src.models import StudentModel, AttendanceModel


class RecognitionCamera(BaseCamera):
    video_source = 0
    # this class variable will help to process every other frame of video to save time
    process_this_frame = True

    @classmethod
    def set_video_source(cls, source):
        cls.video_source = source

    @classmethod
    def frames(cls):
        print("[INFO] starting video stream...")
        camera = cv2.VideoCapture(cls.video_source)

        # store input video stream in camera variable
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        print("[INFO] loading encodings...")
        data = pickle.loads(open(ENCODINGS_FILE, "rb").read())
        # print(len(data['encodings']) == len(data['ids']))

        # find if today's attendance exists in the database
        attendance = AttendanceModel.find_by_date(date=dt.today())
        # if not
        if attendance is None:
            # create new instance for today's attendance
            attendance = AttendanceModel()

        # create in dictionary for known students from database to avoid multiple queries
        known_students = {}
        while True:
            # read current frame
            _, img = camera.read()
            yield cls.recognize_n_attendance(img, attendance, data, known_students)

    @classmethod
    def recognize_n_attendance(cls, frame: np.ndarray, attendance: AttendanceModel,
                               data: Dict, known_students: Dict) -> bytes:
        # convert the input frame from BGR to RGB then resize it to have
        # a width of 750px (to speedup processing)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = imutils.resize(rgb_frame, width=750)
        r = frame.shape[1] / float(rgb.shape[1])

        boxes = []
        encodings = []
        names = []

        # Only process every other frame of video to save time
        if cls.process_this_frame:
            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input frame, then compute
            # the facial embeddings for each face
            boxes = face_recognition.face_locations(rgb, model=DLIB_MODEL)

            encodings = face_recognition.face_encodings(rgb, boxes)

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
        cls.process_this_frame = not cls.process_this_frame
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
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, display_name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        # display the output frames to the screen
        return cv2.imencode('.jpg', frame)[1].tobytes()
