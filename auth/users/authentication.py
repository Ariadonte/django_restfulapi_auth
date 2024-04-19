import datetime
import jwt

from dynamic_preferences.registries import global_preferences_registry

global_preferences = global_preferences_registry.manager()


def create_jwt_token(user_id):
    payload = {
        'id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=global_preferences['general__jwt_expire_time_in_seconds']),
        'iat': datetime.datetime.utcnow(),
    }

    return jwt.encode(payload, 'secret', algorithm='HS256')
