
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://realtimefacedetection-f4004-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref=db.reference('Students')
data={
    "20191CSE0750":
        {
            "Name":"Aiman Nasir",
            "School":"Engineering",
            "Branch":"Computer Science and Engineering",
            "Batch":"2019-2023",
            "Standing":"Good",
            "total attendance":10,
            "last_attendance_time":"2022-03-03 09:00:00"

        },
    "20191CSE0577":
        {
            "Name":"Sneha M. S.",
            "School":"Engineering",
            "Branch":"Computer Science and Engineering",
            "Batch":"2019-2023",
            "Standing":"Good",
            "total attendance":9,
            "last_attendance_time":"2022-03-03 08:45:00"

        },
    "20191CSE0604":
        {
            "Name":"Sai Dheeraj Surampally",
            "School":"Engineering",
            "Branch":"Computer Science and Engineering",
            "Batch":"2019-2023",
            "Standing":"Bad",
            "total attendance":8,
            "last_attendance_time":"2022-03-03 10:00:00"

        },
    "20191CSE0725":
        {
            "Name":"Pinnepalli Basava Vyshnavi",
            "School":"Engineering",
            "Branch":"Computer Science and Engineering",
            "Batch":"2019-2023",
            "Standing":"Good",
            "total attendance":7,
            "last_attendance_time":"2022-03-03 09:30:00"

        },
    "20191CSE0747":
        {
            "Name":"Amalanadhuni Sai Pavan Kalyan",
            "School":"Engineering",
            "Branch":"Computer Science and Engineering",
            "Batch":"2019-2023",
            "Standing":"Bad",
            "total attendance":6,
            "last_attendance_time":"2022-03-03 09:40:00"

        },
"20191CSE0744":
        {
            "Name":"Indra Sena Reddy",
            "School":"Engineering",
            "Branch":"Computer Science and Engineering",
            "Batch":"2019-2023",
            "Standing":"Good",
            "total attendance":5,
            "last_attendance_time":"2022-03-03 09:50:00"

        },
"2020LCS0001":
        {
            "Name":"Rajnish Sharma",
            "School":"Engineering",
            "Branch":"Computer Science and Engineering",
            "Batch":"2019-2023",
            "Standing":"Bad",
            "total attendance":10,
            "last_attendance_time":"2022-03-03 10:55:00"

        }
    }

for key,value in data.items():
    ref.child(key).set(value)