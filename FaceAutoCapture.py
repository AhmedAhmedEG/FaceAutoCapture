from FaceDetectionModule import FaceDetector
from multiprocessing import Process
from datetime import datetime
from time import sleep
# import RPi.GPIO as GPIO
import vlc
import cv2
import sys
import os


def play_sound(name, d):
    sound = vlc.MediaPlayer(f"{name}.mp3")
    sound.play()
    sleep(d)
    sound.stop()
    sys.exit(0)


if __name__ == "__main__":
    # GPIO.setwarnings(False)
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.add_event_detect(4, GPIO.RISING, bouncetime=250)

    path = "Captures"
    if not os.path.isdir(path):
        os.mkdir(path)

    dir_name = datetime.now().strftime("%d.%m.%Y.%H.%M.%S")
    os.mkdir(os.path.join(path, dir_name))

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    detector = FaceDetector()

    faces_number = 0
    min_score = 0.8
    found_duration = 2
    lost_duration = 2
    sound_inst = None
    c = 0

    while True:
        _, img = cap.read()
        img, bboxs = detector.findFaces(img)

        # if GPIO.event_detected(4):
        #     cv2.imwrite(os.path.join(path, dir_name, f"{c}.png"), img)
        #     c += 1

        if len(bboxs) > faces_number:

            for f in bboxs[faces_number - 1:]:

                if f["score"] > min_score:
                    faces_number += 1

                    if sound_inst is not None and sound_inst.is_alive():
                        sound_inst.kill()

                    sound_inst = Process(target=play_sound, args=("found", found_duration, ))
                    sound_inst.start()

                    cv2.imwrite(os.path.join(path, dir_name, f"{c}.png"), img)
                    c += 1

        elif len(bboxs) < faces_number:

            if len(bboxs) == 0:
                faces_number -= 1

                if sound_inst is not None and sound_inst.is_alive():
                    sound_inst.kill()

                sound_inst = Process(target=play_sound, args=("lost", lost_duration, ))
                sound_inst.start()

            else:

                for f in bboxs[faces_number - 1:]:

                    if f["score"] > min_score:
                        faces_number -= 1

                        if sound_inst is not None and sound_inst.is_alive():
                            sound_inst.kill()

                        sound_inst = Process(target=play_sound, args=("lost", lost_duration, ))
                        sound_inst.start()

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
