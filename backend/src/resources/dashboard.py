from flask_restful import Resource
from flask_jwt_extended import jwt_optional, get_jwt_identity


class Dashboard(Resource):
    @classmethod
    @jwt_optional
    def get(cls):
        user_id = get_jwt_identity()
        if user_id:
            return {'message': 'Success! You are now logged in.'}, 200
        return {'message': 'Failure! More data available if you log in.'}, 200
