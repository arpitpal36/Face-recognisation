import csv

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import mysql.connector

# importing images directly instead of importing one by one
path = 'imagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)

# adding names in list classname
for cl in myList:
    currImg = cv2.imread(f'{path}/{cl}')
    images.append(currImg)
    # appending the name only without .jpg
    classNames.append(os.path.splitext(cl)[0])

print(classNames)


# find encoding of image

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


# mydb = mysql.connector.connect(host="localhost", user="arpit", passwd="0122")


def markAttendance(name):
    with open('attendance.csv', 'r+') as f:
        mydatalist = f.readlines()
        namelist = []
        for line in mydatalist:
            entry = line.split(',')
            namelist.append(entry[0])

        if name not in namelist:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')


#
# with open('attendance.csv') as f:
#         f = csv.reader(f, delimiter=',')
#         all_value= []
#         for row in f:
#             value = (row[0])
#             all_value.append(value)
#
# query = "insert into `Attendance`(`Name` , `Time`) values (%s,%s)"
# mycursor = mydb.cursor()
# mycursor.executemany(query, all_value)
# mydb.commit()


encodeListKnown = findEncodings(images)
print('Encoding Complete')

# web cam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    #                    pixelSize , Scale (1/4)
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # for multiple images in one frame
    facesCurrFrame = face_recognition.face_locations(imgS)
    encodesCurrFrame = face_recognition.face_encodings(imgS, facesCurrFrame)

    # find encoding for multiple frames
    for encodeFace, faceLoc in zip(encodesCurrFrame, facesCurrFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        # min value of the list will be the best match
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            # y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)
            markAttendance(name)


    #  shows the webcam on screen
    cv2.imshow('webcam', img)
    cv2.waitKey(1)

# find face
# faceLoc = face_recognition.face_locations(imgElon)[0]
# encode
# encodeElon = face_recognition.face_encodings(imgElon)[0]

# faceLocTest = face_recognition.face_locations(imgTest)[0]
# # encode
# encodeTest = face_recognition.face_encodings(imgTest)[0]
# cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)
# # compare faces
# results = face_recognition.compare_faces([encodeElon],encodeTest)
# # distance
#
# faceDis = face_recognition.face_distance([encodeElon],encodeTest)

# imgElon = face_recognition.load_image_file('images basic/Elon Musk.jpg')
# imgElon = cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB)
# imgTest = face_recognition.load_image_file('images basic/Elon Test.jpg')
# imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)
