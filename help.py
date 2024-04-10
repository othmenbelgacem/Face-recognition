import pickle
import face_recognition
import cv2
import os
import numpy as np
import cvzone
from ultralytics import YOLO
import math
import time
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import firebase_admin
from datetime import datetime
import paho.mqtt.client as mqtt

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("real_time_object_detection")
client.connect(mqttBroker)

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://iot-detection-438f9-default-rtdb.europe-west1.firebasedatabase.app/','storageBucket':'iot-detection-438f9.appspot.com'})
ref = db.reference('facedetection')

# Load YOLO model
model = YOLO("../Yolo-weights/yolov8l.pt")
class_names = ["person"]

# Configure webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 450)

# Load background image and models for face recognition
imgBackground = cv2.imread('resources/background3.png')
folderModePath = 'resources/models'
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

# Load face encoding file
print("Loading Encode File ...")
with open('EncodeFile.p', 'rb') as file:
    encodeListKnownWithIds = pickle.load(file)

encodeListKnown, StudentIDs = encodeListKnownWithIds
print("Encode File Loaded")
ModeType = 0
counter = 0
id= -1
imgStudent =[]
bucket =storage.bucket()
while True:
    # Capture frame from webcam
    success, img = cap.read()
    # Detect objects using YOLO
    results = model(img, stream=True)
    detected_objects = []

    # Process YOLO results
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1

            conf = round(float(box.conf[0]), 2)

            # Class Name
            cls = int(box.cls[0])
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")

            # Check if the class index is within the valid range and it's a person
            if 0 <= cls < len(class_names) and class_names[cls] == "person":


                # Draw rectangle and text on the image
                cvzone.cornerRect(img, (x1, y1, w, h))
                cvzone.putTextRect(img, f'{class_names[cls]} {conf}', (max(0, x1), max(35, y1)))

    #*****************************************************
    # Resize and process the image for face recognition
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Perform face recognition
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    dy = 50
    imgBackground[162 + dy: 162 + 480 + dy, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[ModeType]
    # Check for matching faces
    if faceCurFrame :
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = [any(face_recognition.compare_faces([encode], encodeFace)[0] for encode in encodeListKnown)]
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            #print("matches", matches)
            print("faceDis", faceDis)
#ggggggg
            matchIndex = np.argmin(faceDis)
            min_face_dis = np.min(faceDis)
            #print("Match Index", matchIndex)
            if min_face_dis > 0.5:
                ModeType = 2
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[ModeType]
            else:

           #****************************************************************************************

                id = StudentIDs[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    ModeType = 1
            if counter != 0:
                counter == 1
                studentInfo = db.reference(f'facedetection/{id}').get()  # Added parentheses to call the get method
                #print(studentInfo)
                blob = bucket.get_blob(f'images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                # Update data of attendance



                if ModeType != 3 :
                    if 40 < counter < 60:
                        ModeType = 2
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[ModeType]

                    if counter <= 30:
                        cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
                        cv2.putText(imgBackground, str(studentInfo['job title']), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                        cv2.putText(imgBackground, str(id), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                        cv2.putText(imgBackground, str(studentInfo['Confidence']), (885, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)
                        cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)
                        cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)

                        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414 - w) // 2
                        cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                        imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                        #******************************************************************
                        # Add detected object details to the list
                        detected_objects.append(
                            f'ID: {id}, Class: {class_names}, Confidence: {conf}, Time: {current_time}'
                        )

                    if detected_objects:
                        # Publish the detected objects to MQTT
                        detected_objects_str = '\n'.join(detected_objects)
                        client.publish("object_detection_topic", detected_objects_str)


                    counter += 1
                    if counter >=20 :
                        counter =0
                        ModeType =0
                        studentInfo =[]
                        imgStudent=[]
    else :
        ModeType=0
        counter =0

    # Show the final image
    cv2.imshow("Face Attendance", imgBackground)

    # Break the loop if 'q' key is pressed
    cv2.waitKey(1)
