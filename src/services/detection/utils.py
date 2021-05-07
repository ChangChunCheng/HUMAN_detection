import numpy as np
import cv2
import base64


class ImageTransformer:
    def __init__(self):
        pass

    @classmethod
    def cv2_base64(self, frame):
        base64_str = cv2.imencode('.jpg', frame)[1].tostring()
        base64_str = base64.b64encode(base64_str).decode('utf-8')
        return base64_str

    @classmethod
    def base64_cv2(self, base64_str):
        imgString = base64.b64decode(base64_str.encode('utf-8'))
        nparr = np.fromstring(imgString, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return frame
