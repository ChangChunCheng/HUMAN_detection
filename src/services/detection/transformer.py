import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.absolute()))
from datetime import datetime
import logging
logger = logging.getLogger('Detection testing log.')
logger.setLevel(logging.ERROR)
import numpy as np
import inspect
from tf_pose import common


class Transformer():

    def __init__(self):
        attributes = inspect.getmembers( \
            common.CocoPart, \
            lambda a:not(inspect.isroutine(a)) \
        )
        body_keys = {}
        for a in attributes:
            if \
                not \
                ( \
                    a[0].startswith('__') \
                    and \
                    a[0].endswith('__') \
                ) \
                and \
                (a[0] not in {'name', 'value'}) :
                body_keys[a[1].value] = a[0]
        self.body_keys = body_keys
    
    def get_body_kyes(self):
        return self.body_keys

    def transform(self, human, face_rotation):
        body_point = {}
        for body_key in human.body_parts.keys():
            body_point[self.body_keys[body_key]] = {
                'x': str(human.body_parts[body_key].x),
                'y': str(human.body_parts[body_key].y),
                'score': str(human.body_parts[body_key].score)
            }
        face_rotation = {
            'yaw': str(face_rotation[0]),
            'pitch': str(face_rotation[1]),
            'roll': str(face_rotation[2])
        }
        return body_point, face_rotation

if __name__ == '__main__':
    transformer = Transformer()
    print(transformer.get_body_kyes())