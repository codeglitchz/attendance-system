import os
import shutil
import pickle

from flask import request
from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask_jwt_extended import jwt_required

from src.db import Session
from src.libs import image_helper
from src.libs.train_classifier import TrainClassifier
from src.libs.strings import gettext
from src.models import StudentModel
from src.schemas import StudentSchema, ImageSchema
from src.settings import DATASET_PATH, ENCODINGS_FILE


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
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("image_illegal_extension").format(extension)}, 400

        # train images when submitted successfully
        TrainClassifier.train()
        return {"message": gettext("image_uploaded").format(basename)}, 201
