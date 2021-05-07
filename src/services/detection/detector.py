from services.detection.tf_pose.networks import get_graph_path, model_wh
from services.detection.tf_pose.estimator import TfPoseEstimator
from services.detection.fsanet_pytorch.utils import draw_axis
from services.detection.fsanet_pytorch.face_detector import FaceDetector
import onnxruntime
import torch
import tensorflow as tf
import cv2
import numpy as np
import logging
from datetime import datetime
from pathlib import Path
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logger = logging.getLogger('Detection testing log.')
logger.setLevel(logging.ERROR)


class Detector():
    '''
    Human and face detection with tf-pose-estimation and headpose-fsanet-pytorch.
    tf-pose using tf2.0
    tf-pose-estimation: https://github.com/ildoonet/tf-pose-estimation
    tf-pose with tf2.0: https://medium.com/@gsethi2409/pose-estimation-with-tensorflow-2-0-a51162c095ba
    headpose-fsanet-pytorch: https://github.com/omasaht/headpose-fsanet-pytorch
    '''

    def __init__(
        self,
        fsa_net_path=os.path.join(
            'src', 'services', 'detection', 'fsanet_pytorch', 'pretrained'),
        tf_pose_type='mobilenet_thin',
        target_size=(640, 480),
        resize_out_ratio=4.0
    ):
        self.fsa_net_path = fsa_net_path
        self.tf_pose_type = tf_pose_type
        self.target_size = target_size
        # import model
        self.face_d = FaceDetector()
        self.fsa_sess1 = onnxruntime.InferenceSession(
            os.path.join(
                self.fsa_net_path,
                'fsanet-1x1-iter-688590.onnx'
            )
        )
        self.fsa_sess2 = onnxruntime.InferenceSession(
            os.path.join(
                self.fsa_net_path,
                'fsanet-var-iter-688590.onnx'
            )
        )
        self.tf_pose = TfPoseEstimator(
            get_graph_path(self.tf_pose_type),
            target_size=self.target_size,
            trt_bool='F'
        )
        self.tf_pose_resize_out_ratio = resize_out_ratio

    def resize(self, image, target_size=(640, 480), method=cv2.INTER_NEAREST):
        return cv2.resize(
            image,
            target_size,
            interpolation=method
        )

    def __detect(self, image):
        w, h = model_wh(str(self.target_size[0])+'x'+str(self.target_size[1]))
        # tf-pose estimator detect
        humans = self.tf_pose.inference(
            image,
            resize_to_default=(w > 0 and h > 0),
            upsample_size=self.tf_pose_resize_out_ratio
        )
        # fsa-net detect
        # 1. face detect
        face_bb = self.face_d.get(image)
        # 2. yaw, pitch, roll detection with headpose
        face_rotation = {}
        for index, (x1, y1, x2, y2) in enumerate(face_bb):
            face_roi = image[y1:y2+1, x1:x2+1]
            # preprocess headpose model input
            face_roi = cv2.resize(face_roi, (64, 64))
            face_roi = face_roi.transpose((2, 0, 1))
            face_roi = np.expand_dims(face_roi, axis=0)
            face_roi = (face_roi-127.5)/128
            face_roi = face_roi.astype(np.float32)
            # get headpose
            res1 = self.fsa_sess1.run(["output"], {"input": face_roi})[0]
            res2 = self.fsa_sess2.run(["output"], {"input": face_roi})[0]
            yaw, pitch, roll = np.mean(np.vstack((res1, res2)), axis=0)
            face_rotation.update({index: [yaw, pitch, roll]})
        return humans, face_rotation

    def detect(self, image):
        return self.__detect(image)

    def draw(self, image, humans, face_rotation):
        image = TfPoseEstimator.draw_humans(
            image, humans,
            imgcopy=False
        )
        image = draw_axis(
            image,
            face_rotation[0],
            face_rotation[1],
            face_rotation[2],
            tdx=image.shape[0], \
            # tdx=(x2-x1)//2+x1, \
            tdy=10, \
            # tdy=(y2-y1)//2+y1, \
            size=50
        )
        return image


if __name__ == "__main__":
    detection = Detector()
    image = cv2.imread(os.path.join('src', 'services',
                       'detection', 'test', 'input', 'apink1.jpg'))
    image = detection.resize(image)
    humans, face_rotation = detection.detect(image)
    image = detection.draw(image, [humans[0]], face_rotation[0])
    cv2.imwrite(os.path.join('src', 'services', 'detection',
                'test', 'output', 'apink1.jpg'), image)
