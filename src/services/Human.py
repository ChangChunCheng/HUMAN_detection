from config import settings
from services.detection.transformer import Transformer
from services.detection.detector import Detector
from services.detection.utils import ImageTransformer


class Detect():
    def __init__(self):
        self.TRANSFORMER = Transformer()
        self.DETECTOR = Detector(
            tf_pose_type=settings().TF_POSE_TYPE,
            target_size=(640, 480),
            resize_out_ratio=4.0
        )
        self.IMAGETRANSFORMER = ImageTransformer()

    def detect(self, frame):
        '''
        frame detect and draw human on image
        # input: image/video/webcam frame
        # output: 
        #   1. frame with draw
        #   2. human key points from tf_pose
        #   3. yaw, pitch, roll from fsa-net
        '''
        frame = self.DETECTOR.resize(frame)
        humans, face_rotation = self.DETECTOR.detect(frame)
        if len(humans) == 0 or len(face_rotation) == 0:
            return frame, None, None
        frame = self.DETECTOR.draw(frame, [humans[0]], face_rotation[0])
        human, face_rotation = self.TRANSFORMER.transform(
            humans[0], face_rotation[0])
        return frame, human, face_rotation

    def callback_structure(self, frame, human, face_rotation):
        return {
            'frame': self.IMAGETRANSFORMER.cv2_base64(frame),
            'tf_pose': human,
            'fsa': face_rotation
        }
