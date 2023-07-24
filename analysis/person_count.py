# Unsuccessful attempt at counting the number of people in the room by using the haarcascade_frontalface_default classifier on videos recorded by a smartphone
# https://github.com/kipr/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
import cv2
import pandas as pd

FILENAME = "videos/TimeVideo_20220729_231417.mp4"

fps = 1
save_intervall = 1000
start = 160
debug = True
min_faces = 0

video = cv2.VideoCapture(FILENAME)
video.set(cv2.CAP_PROP_FPS, 0.1)
success, image = video.read()
count = 0

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

data = pd.read_csv("faces.csv", index_col=0)
data = data.append({"frame": 0, "num_faces": 0}, ignore_index=True)
data = data.astype({"frame":'int', "num_faces":'int'})

while success:
    if count >= start and count%fps == 0:
        image = image[390:620, 200:900]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=1,
            minSize=(50, 50),
            flags = cv2.CASCADE_SCALE_IMAGE
        )

        data = data.append({"frame": count, "num_faces": len(faces)}, ignore_index=True)
        print(count, len(faces))
        
        if debug and len(faces) >= min_faces:
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            cv2.imshow("Faces found", image)
            cv2.waitKey(0)

    if count%save_intervall == 0:
        data.to_csv("faces.csv")

    success, image = video.read()
    count += 1