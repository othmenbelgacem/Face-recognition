import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://machinelearning-6efab-default-rtdb.firebaseio.com/'})
ref = db.reference('facedetection')

data = {
    "334555": {
        "name": "ons jabeur",
        "job title": "tennis player",
        "starting_year": 2010,
        "total_attendance": 6,
        "Confidence": "0",
        "year": 29,
        "Last_attendance_time": "2022-12-11 00:54:34"
    },
    "538252": {
        "name": "Othmen belgacem",
        "job title": "Data Quality",
        "starting_year": 2021,
        "total_attendance": 3,
        "Confidence": "0",
        "year": 25,
        "Last_attendance_time": "2022-12-11 00:54:34"
    },
"538222": {
        "name": "Bill Gates",
        "job title": "Co-founding of Microsoft",
        "starting_year": 1972,
        "total_attendance": 9,
        "Confidence": "0",
        "year": 68,
        "Last_attendance_time": "2022-12-11 00:54:34"
    },
"538242": {
        "name": "elon musk",
        "job title": "CEO of Tesla Motors",
        "starting_year": 1995,
        "total_attendance": 6,
        "Confidence": "0",
        "year": 52,
        "Last_attendance_time": "2022-12-11 00:54:34"
    },
"738921": {
"name": "Mark Zuckerberg",
"job title": "CEO of Meta",
"starting_year": 2004,
"total_attendance": 8,
"Confidence": "0",
"year": 39,
"Last_attendance_time": "2022-11-30 09:21:15"
},

"621837": {
"name": "Satya Nadella",
"job title": "CEO of Microsoft",
"starting_year": 2014,
"total_attendance": 7,
"Confidence": "0",
"year": 56 ,
"Last_attendance_time": "2022-12-05 14:42:09"
},

"359812": {
"name": "Tim Cook",
"job title": "CEO of Apple Inc.",
"starting_year": 1998,
"total_attendance": 9,
"Confidence": "0",
"year": 63,
"Last_attendance_time": "2022-12-08 18:10:45"
},

"485721": {
"name": "Sheryl Sandberg",
"job title": "COO of Facebook",
"starting_year": 2008,
"total_attendance": 6,
"Confidence": "0",
"year": 54,
"Last_attendance_time": "2022-12-10 11:35:22"
},

"126543": {
"name": "Jeff Bezos",
"job title": "Executive Chairman of Amazon",
"starting_year": 1994,
"total_attendance": 10,
"Confidence": "0",
"year": 71,
"Last_attendance_time": "2022-12-13 20:15:18"
},

"932167": {
"name": "Sundar Pichai",
"job title": "CEO of Alphabet Inc.",
"starting_year": 2004,
"total_attendance": 8,
"Confidence": "0",
"year": 61,
"Last_attendance_time": "2022-12-16 09:53:30"
},

"874239": {
"name": "Ginni Rometty",
"job title": "Former CEO of IBM",
"starting_year": 2012,
"total_attendance": 5,
"Confidence": "0",
"year": 34,
"Last_attendance_time": "2022-12-09 16:28:11"
},

"563298": {
"name": "Jack Dorsey",
"job title": "CEO of Square, Inc.",
"starting_year": 2009,
"total_attendance": 7,
"Confidence": "0",
"year": 38,
"Last_attendance_time": "2022-12-12 22:45:56"
},
"789012": {
"name": "Brian Chesky",
"job title": "CEO of Airbnb",
"starting_year": 2008,
"total_attendance": 6,
"Confidence": "0",
"year": 44,
"Last_attendance_time": "2022-12-15 08:36:27"
},
}

for key, value in data.items():
    ref.child(key).set(value)
