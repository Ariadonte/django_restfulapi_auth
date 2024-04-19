from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.types import IntPreference

jwt_expire_time = Section('general')
refresh_token_expire_time = Section('general')


@global_preferences_registry.register
class JwtExpireTime(IntPreference):
    section = jwt_expire_time
    name = 'jwt_expire_time_in_seconds'
    default = 30
    required = True


@global_preferences_registry.register
class RefreshTokenExpireTime(IntPreference):
    section = refresh_token_expire_time
    name = 'refresh_token_expire_time_in_days'
    default = 30
    required = True

