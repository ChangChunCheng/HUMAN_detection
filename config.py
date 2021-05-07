import os
import sys

basedir = os.path.abspath(os.path.dirname(__file__))

class ModelConfig(object):
    TF_POSE_TYPE = 'cmu' # cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small
    FRAME_SIZE = (640,480)

class BaseConfig(ModelConfig):
    PROJECT_NAME = os.environ['PROJECT_NAME']
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.getcwd(), 'files', 'upload'))
    PROCESSED_FOLDER = os.path.abspath(os.path.join(os.getcwd(), 'files', 'processed'))

class DevelopmentConfig(BaseConfig):
    MODE = 'development'
    VIDEO_FPS = 1

class TestingConfig(BaseConfig):
    MODE = 'testing'
    VIDEO_FPS = 1

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}

# print(config['development'].PROJECT_NAME)