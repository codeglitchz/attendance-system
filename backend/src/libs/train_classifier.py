import os
import pickle

import cv2
import face_recognition

from src.settings import DATASET_PATH, ENCODINGS_FILE, DLIB_MODEL


class TrainClassifier:
    """Train KNN Classifier by storing results in `files/encodings.pickle` file"""
    # TODO: Store encodings in SQL database rather than `files/encodings.pickle` file
    @classmethod
    def train(cls):
        try:
            print("[INFO] loading encodings...")
            with open(ENCODINGS_FILE, "rb") as ef:
                data = pickle.loads(ef.read())
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
                try:
                    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                except cv2.error:
                    # delete image that cannot be processed
                    try:
                        os.remove(image_path)
                    except (FileNotFoundError, PermissionError):
                        pass
                    continue

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
