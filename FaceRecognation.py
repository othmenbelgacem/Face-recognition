import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials, db, storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://machinelearning-6efab-default-rtdb.firebaseio.com/', 'storageBucket': 'machinelearning-6efab.appspot.com'})
ref = db.reference('facedetection')

# Importing student images
folderPath = 'images'
modePathlist = os.listdir(folderPath)
imglist = []
StudentIDs = []

for path in modePathlist:
    img = cv2.imread(os.path.join(folderPath, path))
    if img is not None:
        imglist.append(img)
        StudentIDs.append(os.path.splitext(path)[0])
        fileName = f'{folderPath}/{path}'
        bucket = storage.bucket()
        blob = bucket.blob(fileName)

        # Check if file already exists before uploading
        if not blob.exists():
            blob.upload_from_filename(fileName)
        else:
            print(f"File {fileName} already exists in Firebase Storage.")

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(img)

        if face_locations:
            encode = face_recognition.face_encodings(img, face_locations)[0]
            encodeList.append(encode)
        else:
            print("No face found in one or more images.")

    return encodeList

print("Encoding Started")
encodeListKnown = findEncodings(imglist)
encodeListKnownWithIds = [encodeListKnown, StudentIDs]
print(encodeListKnown)
print("Encoding Complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")
