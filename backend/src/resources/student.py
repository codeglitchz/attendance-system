import os
import shutil
import pickle

import cv2
import face_recognition
from flask import request
from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask_jwt_extended import jwt_required

from src.db import Session
from src.libs import image_helper
from src.libs.strings import gettext
from src.models import StudentModel
from src.schemas import StudentSchema, ImageSchema
from src.settings import DATASET_PATH, ENCODINGS_FILE, DLIB_MODEL


student_schema = StudentSchema()
student_list_schema = StudentSchema(many=True)
image_schema = ImageSchema()


class StudentList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return student_list_schema.dump(StudentModel.find_all()), 200


class StudentAdd(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        student_json = request.get_json()

        student = student_schema.load(student_json, session=Session)

        try:
            student.save_to_db()
        except:
            return {"message": gettext('error_inserting')}, 500

        # create a directory for <id> of the student
        id_path = os.path.join(DATASET_PATH, str(student.id))
        if not os.path.exists(id_path):
            os.makedirs(id_path)
        # todo: now automatically train the images
        return student_schema.dump(student), 201


class StudentDelete(Resource):
    @classmethod
    @jwt_required
    def delete(cls, student_id: int):
        student = StudentModel.find_by_id(student_id)
        if student:
            student.delete_from_db()
            # delete the folder containing images of student in the dataset
            id_path = os.path.join(DATASET_PATH, str(student_id))
            if os.path.exists(id_path):
                shutil.rmtree(id_path)
            # remove student training data
            ids = []
            encodings = []
            try:
                print("[INFO] loading encodings...")
                data = pickle.loads(open(ENCODINGS_FILE, "rb").read())
                # initialize the list of known encodings and known names
                known_encodings = data["encodings"]
                known_ids = data["ids"]
                for index in range(len(known_ids)):
                    if known_ids[index] != student_id:
                        ids.append(known_ids[index])
                        encodings.append(known_encodings[index])
                data = {"encodings": encodings, "ids": ids}
                f = open(ENCODINGS_FILE, "wb")
                f.write(pickle.dumps(data))
                f.close()
            except FileNotFoundError:
                pass
            return {"message": gettext('student_deleted').format(student.name, student.id)}, 200

        return {"message": gettext('student_not_found')}, 404


class StudentCapture(Resource):
    @classmethod
    @jwt_required
    def post(cls, student_id: int):
        """
        Used to upload an images of student to the server.
        """
        data = image_schema.load(request.files)  # {"image": FileStorage}
        folder = os.path.join("dataset", str(student_id))  # static/images/dataset/1
        filename = str(len(os.listdir(os.path.join(DATASET_PATH, str(student_id)))) + 1)
        # image_path = image_helper.get_path(filename, folder)
        try:
            extension = image_helper.get_extension(data["image"].filename)
            save_as_filename = filename + extension
            image_path = image_helper.save_image(data["image"], folder=folder, name=save_as_filename)
            basename = image_helper.get_basename(image_path)
            return {"message": gettext("image_uploaded").format(basename)}, 201
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("image_illegal_extension").format(extension)}, 400


class TrainClassifier(Resource):
    """Train KNN Classifier by storing results in `files/encodings.pickle` file"""
    # TODO: Store encodings in SQL database rather than `files/encodings.pickle` file
    @classmethod
    @jwt_required
    def get(cls):
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
