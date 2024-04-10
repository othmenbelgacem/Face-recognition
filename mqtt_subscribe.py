import pickle
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db
import paho.mqtt.client as mqtt

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://machinelearning-6efab-default-rtdb.firebaseio.com/',
    'storageBucket': 'machinelearning-6efab.appspot.com/images'
})
ref = db.reference('facedetection')

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("myapplication")


def on_message(client, userdata, message):
    detected_objects = message.payload.decode()
    print(f"Received Detected Objects: {detected_objects}")

    # Assuming detected_objects is a string representation of the object details
    # Parse the string to extract the relevant information, including the 'id'
    # Example: Assuming the id is the first part of the string (you should adjust this based on your actual format)
    id = detected_objects.split(',')[0].split(': ')[1]
    confidence = detected_objects.split(',')[2].split(': ')[1]


    studentInfo = db.reference(f'facedetection/{id}').get()
    datetimeObject = datetime.strptime(studentInfo['Last_attendance_time'], "%Y-%m-%d %H:%M:%S")
    second_detect = (datetime.now() - datetimeObject).total_seconds()
    print(second_detect)

    if second_detect > 30:
        ref = db.reference(f'facedetection/{id}')
        studentInfo['total_attendance'] += 1
        ref.child('total_attendance').set(studentInfo['total_attendance'])
        ref.child('Last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ref.child('Confidence').set(confidence)



client.on_message = on_message
client.connect(mqttBroker)
client.subscribe("object_detection_topic")
client.loop_forever()