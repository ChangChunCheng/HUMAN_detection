import os
import cv2
import base64
import json
import numpy as np
import requests
from dotenv import load_dotenv
from demo_file.utils import cv2_base64, base64_cv2

load_dotenv(dotenv_path='.env')

def stream(frame):
    data = {
        'image': cv2_base64(frame)
    }
    response = requests.post(
        'http://' + os.getenv("HOST_IP") + ':' + os.getenv("PORT") + '/api/stream',
        data = json.dumps(data),
        headers = {
            "Content-Type": "application/json"
        }
    )
    data = {}
    data['tf_pose'] = response.json()['tf_pose']
    data['fsa'] = response.json()['fsa']
    return data, frame

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        data, frame = stream(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # release camera
    cap.release()
    # close windows
    cv2.destroyAllWindows()