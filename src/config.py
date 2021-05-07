from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    MODE: str = "DEVELOPMENT"

    APP_NAME: str = "HUMAN_detection"
    ADMIN_EMAIL: str = "jacky850509@gmail.com"

    # cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small
    TF_POSE_TYPE = 'mobilenet_thin'


@lru_cache()
def settings():
    return Settings()
