import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from django.conf import settings
import urllib.request



class FaceCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        path=os.path.join(settings.BASE_DIR,'media/')
        images=[]
        classNames = []
        myList = os.listdir(path)
        print(myList)
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        self.images=images
        self.classNames=classNames
        self.encodeListKnown = self.findEncodings()
        print('Encoding Complete')

    def __del__(self):
        self.video.release()

    def findEncodings(self):
        encodeList = []
        for img in self.images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def markAttendance(self):
        with open(os.path.join(settings.BASE_DIR,'attendance/attendance.csv'),'r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if self.name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{self.name},{dtString}')

    def get_frame(self):


        success, img = self.video.read()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace,faceLoc in zip(encodeCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(self.encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(self.encodeListKnown,encodeFace)
            #print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = self.classNames[matchIndex].upper()
                #print(name)
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                self.name=name
                self.markAttendance()

        ret, jpeg = cv2.imencode('.jpg',img)
        return jpeg.tobytes()

    



    




# faceLoc =face_recognition.face_locations(imgElon)[0]
# encodeElon=face_recognition.face_encodings(imgElon)[0]
# cv2.rectangle(imgElon,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
#
# faceLocTest =face_recognition.face_locations(imgTest)[0]
# encodeTest=face_recognition.face_encodings(imgTest)[0]
# cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)
#
#
# results=face_recognition.compare_faces([encodeElon],encodeTest)
# faceDis=face_recognition.face_distance([encodeElon],encodeTest)