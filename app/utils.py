import cv2
import base64
import numpy as np

def base64_it(data: bytes):
    return base64.encodebytes(data).decode('ascii')

def encode(image):
    encode = cv2.imencode('.png', image)[1].tobytes()
    encode = base64_it(encode)
    return encode

def decode(encoded):
    im_byte = base64.decodebytes(encoded.encode('ascii'))
    decoded = cv2.imdecode(
        np.asarray(bytearray(im_byte), dtype='uint8'),
        cv2.IMREAD_COLOR
    )
    return decoded