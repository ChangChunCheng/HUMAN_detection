### https://github.com/ZheC/tf-pose-estimation
import os
from argparse import ArgumentParser
import numpy as np
import cv2
import onnxruntime

from fsanet_pytorch.face_detector import FaceDetector
from fsanet_pytorch.utils import draw_axis

def main(image, out):
    face_d = FaceDetector()
    sess = onnxruntime.InferenceSession(os.path.join('detection', 'fsanet_pytorch', 'pretrained', 'fsanet-1x1-iter-688590.onnx'))
    sess2 = onnxruntime.InferenceSession(os.path.join('detection', 'fsanet_pytorch', 'pretrained', 'fsanet-var-iter-688590.onnx'))

    frame = cv2.imread(image)
    frame = cv2.resize(frame, (640,480))
    face_bb = face_d.get(frame)
    for (x1,y1,x2,y2) in face_bb:
        face_roi = frame[y1:y2+1,x1:x2+1]

        #preprocess headpose model input
        face_roi = cv2.resize(face_roi,(64,64))
        face_roi = face_roi.transpose((2,0,1))
        face_roi = np.expand_dims(face_roi,axis=0)
        face_roi = (face_roi-127.5)/128
        face_roi = face_roi.astype(np.float32)

        #get headpose
        res1 = sess.run(["output"], {"input": face_roi})[0]
        res2 = sess2.run(["output"], {"input": face_roi})[0]
        
        yaw,pitch,roll = np.mean(np.vstack((res1,res2)),axis=0)

        frame = draw_axis(frame,yaw,pitch,roll,tdx=(x2-x1)//2+x1,tdy=(y2-y1)//2+y1,size=50)
        cv2.imwrite(out,frame)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-i", dest='image', type=str, default=None,
                        help="Path of picture")
    parser.add_argument("-o", dest='out', type=str, default=None,
                        help="Path of output picture")
    args = parser.parse_args()
    main(args.image, args.out)