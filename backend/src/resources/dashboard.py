from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.libs.strings import gettext


class Dashboard(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls):
        user_id = get_jwt_identity()
        if user_id:
            return {'message': gettext('you_are_logged_in')}, 200
        return {'message': gettext('login_to_continue')}, 401
