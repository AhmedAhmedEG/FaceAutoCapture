from cvzone.FaceDetectionModule import FaceDetector
from datetime import datetime
from time import sleep
import vlc
import cv2
import os

if not os.path.isdir("Captures"):
    os.mkdir("Captures")

dir_name = datetime.now().strftime("%d.%m.%Y.%H.%M.%S")
os.mkdir(os.path.join("Captures", dir_name))

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)

detector = FaceDetector()
found = vlc.MediaPlayer("found.mp3")
lost = vlc.MediaPlayer("lost.mp3")

faces_number = 0
min_score = 0.8
c = 0

while True:
    _, img = cap.read()
    img, bboxs = detector.findFaces(img)

    if len(bboxs) > faces_number:

        for f in bboxs[faces_number - 1:]:

            if f["score"] > min_score:
                faces_number += 1

                found.play()
                sleep(0.5)
                found.stop()

                cv2.imwrite(os.path.join("Captures", dir_name,f"{c}.png"), img)
                c += 1

    elif len(bboxs) < faces_number:

        if len(bboxs) == 0:
            faces_number -= 1

            lost.play()
            sleep(0.5)
            lost.stop()

        else:

            for f in bboxs[faces_number - 1:]:

                if f["score"] > min_score:
                    faces_number -= 1

                    lost.play()
                    sleep(0.5)
                    lost.stop()

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()