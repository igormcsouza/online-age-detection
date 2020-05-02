from flask import Flask, request, redirect, jsonify
from age_detector import AgeDetector as ad
import numpy as np
import cv2

app = Flask(__name__)

res = dict(
    roi=[], age=None, message='No file Found', 
    filename='', ageConfidence=None, image=None
)

@app.route('/age-detection', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify(res)

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            res['message'] = 'No selected file'
            return jsonify(res)
        
        res['message'] = 'Success'
        res['filename'] = file.filename

        filestr = file.read()
        npimg = np.fromstring(filestr, np.uint8)
        image = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)

        new_detection = ad(image, 'detectors/face-detector', 'detectors/age-detector', 0.5)
        answer = new_detection.detect()
        # res['image'] = answer['image']
        res['age'] = answer['age']
        res['ageConfidence'] = str(answer['ageConfidence'])
        # res['roi'] = answer['roi']

        return jsonify(res)