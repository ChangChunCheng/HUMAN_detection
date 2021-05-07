import requests
import os
from services.detection.utils import ImageTransformer
import cv2


files = {
    'image':
        '/mnt/dbs/HUMAN_detection/src/services/detection/test/input/apink1.jpg'
}
image = cv2.imread(files['image'])

print(ImageTransformer.cv2_base64(image))
