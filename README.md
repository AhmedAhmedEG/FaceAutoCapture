# FaceAutoCapture
A python script that can auto capture images whenever it discovers a new face in a camera stream, it uses cvzone library which is a library that simplifies working with google's mediapipe.

You can change the min_score variable to change how much confidance the the model should be having to determine if the object that it captured is actually a real human face, it's a float number ranging from 0 to 1, the confidance appears as percentage in the script output stream.
