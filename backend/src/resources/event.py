from flask_restful import Resource
from flask_jwt_extended import jwt_required


event_list = [
    {
        "id": "1",
        "name": "Auto Expo",
        "description": "lorem ipsum",
        "date": "2020-06-12T04:09:23.511Z"
    },
    {
        "id": "2",
        "name": "Auto Expo",
        "description": "lorem ipsum",
        "date": "2020-06-12T04:09:23.511Z"
    },
    {
        "id": "3",
        "name": "Auto Expo",
        "description": "lorem ipsum",
        "date": "2020-06-12T04:09:23.511Z"
    },
    {
        "id": "4",
        "name": "Auto Expo",
        "description": "lorem ipsum",
        "date": "2020-06-12T04:09:23.511Z"
    },
    {
        "id": "5",
        "name": "Auto Expo",
        "description": "lorem ipsum",
        "date": "2020-06-12T04:09:23.511Z"
    },
    {
        "id": "6",
        "name": "Auto Expo",
        "description": "lorem ipsum",
        "date": "2020-06-12T04:09:23.511Z"
    }
]


class Events(Resource):
    @classmethod
    def get(cls):
        return event_list, 200


class SpecialEvents(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return event_list, 200
