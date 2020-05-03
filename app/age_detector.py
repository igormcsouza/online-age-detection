import os
import cv2
import numpy as np

class AgeDetector:
    def __init__(self, image, face, age, confidence):
        # numpy array image
        self.image = image
        # folder for face detection binaries and age detection binaries
        self.face = face
        self.age = age
        # confidence cut
        self.confidence = confidence

    def _loading_detectors(self):
        print("[AGE_DETECTION][INFO] loading face detector model from disk...")
        prototxtPath = os.path.sep.join([self.face, "deploy.prototxt"])
        weightsPath = os.path.sep.join([
            self.face, "res10_300x300_ssd_iter_140000.caffemodel"
        ])
        faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

        print("[AGE_DETECTION][INFO] loading age detector model from disk...")
        prototxtPath = os.path.sep.join([self.age, "age_deploy.prototxt"])
        weightsPath = os.path.sep.join([self.age, "age_net.caffemodel"])
        ageNet = cv2.dnn.readNet(prototxtPath, weightsPath)

        return faceNet, ageNet

    def detect(self, size=(300, 300), mean=(104.0, 177.0, 123.0)):
        # Defining age buckers for our problem.
        AGE_BUCKETS = [
            "(0-2)", "(4-6)", "(8-12)", "(15-20)", "(25-32)",
            "(38-43)", "(48-53)", "(60-100)"
        ]
        
        faceNet, ageNet = self._loading_detectors()

        # More about blob thing below
        # https://www.pyimagesearch.com/2017/11/06/deep-learning-opencvs-blobfromimage-works/
        (h, w) = self.image.shape[:2]
        blob = cv2.dnn.blobFromImage(self.image, 1.0, size=size, mean=mean)

        print("[AGE_DETECTION][INFO] computing face detections...")
        faceNet.setInput(blob)
        detections = faceNet.forward()

        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]
            # filter out weak detections by ensuring the confidence is
            # greater than the minimum confidence
            if confidence > self.confidence:
                # compute the (x, y)-coordinates of the bounding box for the
                # object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                # extract the ROI of the face and then construct a blob from
                # *only* the face ROI
                face = self.image[startY:endY, startX:endX]
                faceBlob = cv2.dnn.blobFromImage(
                    face, 1.0, size=(227, 227),
                    mean=(78.4263377603, 87.7689143744, 114.895847746),
                    swapRB=False
                )
                # make predictions on the age and find the age bucket with
                # the largest corresponding probability
                ageNet.setInput(faceBlob)
                preds = ageNet.forward()
                i = preds[0].argmax()
                age = AGE_BUCKETS[i]
                ageConfidence = preds[0][i]
                # display the predicted age to our terminal
                text = "{}: {:.2f}%".format(age, ageConfidence * 100)
                print("[AGE_DETECTION][INFO] {}".format(text))
                # draw the bounding box of the face along with the associated
                # predicted age
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(self.image, (startX, startY), (endX, endY),
                    (0, 0, 255), 2)
                cv2.putText(
                    self.image, text, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, 
                    (0, 0, 255), 2
                )

        return {
            'image': self.image, 
            'age': age, 
            'ageConfidence': ageConfidence, 
            'roi': [(startX, startY), (endX, endY)]
        }

