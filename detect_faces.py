#import packages
import numpy as np
import argparse
import cv2

#construct argument parse
ap = argparse.ArgumentParser()

ap.add_argument("-i", "--image", required=True, help="path to input image")
ap.add_argument("-p", "--prototxt", required=True, help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True, help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probability to filter weak detections")

#parse the arguments
args = vars(ap.parse_args())

#load the model
print("[INFO] loading model ...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

#load the input image and construct a fixed image frame
image = cv2.imread(args["image"])
(h, w) = image.shape[:2]
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

#pass image through network and obtain detections and predictions
print("[INFO] computing object detections ...")
net.setInput(blob)
detections = net.forward()

#for each detections
for i in range(0, detections.shape[2]):
    #extract the confidence associated with the prediction
    confidence = detections[0, 0, i, 2]

    if confidence > args["confidence"]:
        #compute bounding box for object
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        #draw bounding box of the face with the probability
        text = "{:.2f}%".format(confidence * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
        cv2.putText(image, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

#show the output
cv2.imshow("Output", image)
cv2.waitKey(0)


