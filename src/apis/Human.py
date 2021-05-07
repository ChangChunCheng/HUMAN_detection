from fastapi import APIRouter, Request
from services.detection.utils import ImageTransformer
import services
import json
import documents

detertor = services.Human.Detect()
imagetransformer = ImageTransformer()

router = APIRouter()


@router.post('/stream')
def stream(image: documents.Human.Image):
    base64_frame = image.image
    frame = imagetransformer.base64_cv2(base64_frame)
    frame, human, face_rotation = detertor.detect(frame)
    result = detertor.callback_structure(
        frame, human, face_rotation)
    return json.dumps(result)
