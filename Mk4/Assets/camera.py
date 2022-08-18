import cv2
import numpy as np
import face_recognition
import os

from Mk3 import speak


def findEncoding(images):
    print(len(images))
    encodeList = []
    for img in images:
        print(len(img))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def face_rec():
    path = "Access_members"
    images = []
    names = []
    mylist = os.listdir(path)
    # print(mylist)
    for cl in mylist:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        names.append(os.path.splitext(cl)[0])
    # print(names)
    encodeListKnown = findEncoding(images)
    name = ""
    i = 0
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        i += 1
        # print(i)
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgS)
        # print(facesCurFrame)
        if facesCurFrame:
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    name = names[matchIndex]
                if name in names:
                    # print("okay")
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    name = name.upper()
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    cv2.imshow("webcam", img)
                    cv2.waitKey(1)
                    speak("You are recognized!")
                    cv2.destroyAllWindows()
                    return True

                else:
                    speak("sorry sir!,I couldn't recognize you!")

        else:
            speak("Could You please allow me to scan your Face!")

        cv2.imshow("webcam", img)
        cv2.waitKey(1)


def New_access(name):
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgS)
        if len(facesCurFrame) == 1:
            y1, x2, y2, x1 = facesCurFrame[0][0], facesCurFrame[0][1], facesCurFrame[0][2], facesCurFrame[0][3]
            new_face = img[y1 - 40:y2 + 20, x1:x2]
            path = "{}/{}/{}{}".format("Images", "Access_members", name, ".jpg")
            cv2.imwrite(path, new_face)
            cv2.rectangle(img, (x1, y1 - 40), (x2, y2 + 20), (0, 255, 0), 2)
            cv2.imshow("webcam", img)
            cv2.waitKey(1)
            cv2.destroyAllWindows()
            return

        elif len(facesCurFrame) >= 2:
            speak("I am getting more than one face")
            speak("I can't give access more than one at a time")
        else:
            speak("sorry sir! I couldn't recognize you")
        cv2.imshow("webcam", img)
        cv2.waitKey(1)
