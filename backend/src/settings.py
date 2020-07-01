from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
PROPAGATE_EXCEPTIONS = True
SECRET_KEY = config('SECRET_KEY')
JWT_SECRET_KEY = config('JWT_SECRET_KEY')
