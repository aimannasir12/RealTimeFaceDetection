import cv2
import os
import pickle
import face_recognition
from datetime import datetime
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://realtimefacedetection-f4004-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storageBucket':'realtimefacedetection-f4004.appspot.com'
})

bucket=storage.bucket()

cap=cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,180)

imgBackground=cv2.imread('Resources/background.png')
folderModePath='Resources/Modes'
modePathList=os.listdir(folderModePath)
imgModeList=[]
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))

#load the encoding file
print("Loading encoded file...")
file=open('EncodeFile.p','rb')
encodeListKnownWithIds=pickle.load(file)
[encodeListKnown,studentIds]=encodeListKnownWithIds
file.close()
print("Encode file loaded")

modeType=0
counter=0
id=-1
imgStudent=[]

while True:
    success,img=cap.read()
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame=face_recognition.face_locations(imgS)
    encodeCurFrame=face_recognition.face_encodings(imgS,faceCurFrame)
    imgBackground[280:280+180,75:75+320]=img
    imgBackground[20:767, 510:930] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=0.8)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            #print(faceDis)
            #print(matches)
            for i in faceDis:
                if i<0.45:
                    print("Unknown face detected")
            if matches[matchIndex]:
                # print("Known face detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 105 + x1, 250 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground,"Loading...",(275,400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1
        if counter != 0:
            if counter == 1:
                # Get the data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                # Get the image from the storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                # Update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total attendance'] += 1
                    ref.child('total attendance').set(studentInfo['total attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[20:767, 510:930] = imgModeList[modeType]

            if modeType != 3:
                if counter <= 10:
                    # imgBackground[772:772+215,200:200+215]=imgStudent
                    imgBackground[20:767, 510:930] = imgModeList[modeType]
                    cv2.putText(imgBackground, str(id), (715, 393),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['School']), (715, 507),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)

            if 10 < counter < 30:
                modeType = 2
                imgBackground[20:767, 510:930] = imgModeList[modeType]

            counter += 1

            if counter >= 30:
                counter = 0
                modeType = 0
                studentInfo = []
                imgStudent = []
                imgBackground[20:767, 510:930] = imgModeList[modeType]


    else:
        modeType=0
        counter=0




    #cv2.imshow("Face Attendance", imgS)
    cv2.imshow("Face Attendance",imgBackground)
    cv2.waitKey(1)
