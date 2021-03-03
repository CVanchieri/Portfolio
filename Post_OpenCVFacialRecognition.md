---
layout: page
title:
image: 
nav-menu: false
description: null
show_tile: false

---

![twitter](https://github.com/CVanchieri/DSPortfolio/blob/master/assets/images/ImageFacialRecognition/face_recognition.png?raw=true) <br>

## Image facial recognition using OpenCV.
There is a Pipfile in the repo with 2 folders, 1 for the face images and 1 for the test image.

---

#### Necessary imports.
```
import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
```

#### Step 1: The face images need to be encoded, this function will go through the images in the folder and encode them.
```
### encode all the face images ###
def encoded_faces():
# returns a dict of (name, image encoded)
    encoded = {}
    for dirpath, dnames, fnames in os.walk("./face_images"): # look through each image in face_iamges folder 
        for f in fnames: 
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("face_images/" + f) # load each file 
                encoding = fr.face_encodings(face)[0] # get the face encoding 
                encoded[f.split(".")[0]] = encoding # split encoding add to dict

    return encoded
```

#### Step 2: The test image needs to be encoded as well, this function will encode a single image.
```
### encode image from file name ### 
def unknown_image(img):
    face = fr.load_image_file("face_images/" + img) # load the image file 
    encoding = fr.face_encodings(face)[0] # get the face encoding 

    return encoding
```

#### Step 3: Search for faces in the face images and the test image, check to see if there is a comparable match, draw rectangles around the faces located, and add names if a match was found.
```
### find the faces and label if known ###
def search_face(im):
# param 'im' is str of file path
# returns a list of face names
    face_names = [] # create a list for the face names found 
    faces = encoded_faces() # set the function
    faces_encoded = list(faces.values()) # create a list of the encoded faces values 
    known_face_names = list(faces.keys()) # creat a list of the faces key values 
    img = cv2.imread(im, 1) # read in the image
    face_locations = face_recognition.face_locations(img) # find the face locations from the image 
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations) # find the unkown face encodings
```
```
    ### loop through unkown face encodings ###
    for face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        match_list = face_recognition.compare_faces(faces_encoded, face_encoding) # see if the face is a match 
        name = "Unknown" 
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding) # find face distances 
        best_match = np.argmin(face_distances) # find the smallest distance from known face to new face 
        if match_list[best_match]: # if a match 
            name = known_face_names[best_match] # set the name 
        face_names.append(name) # add the name to the list 
```
```
    ### create the visual face boxes and text ### 
        for (top, right, bottom, left), name in zip(face_locations, face_names): # loop through face_locations and face_names
            # Draw a box around the face
            cv2.rectangle(img, (left-20, top-20), (right+20, bottom+40), (0, 255, 0), 1) # set the box parameters 
            font = cv2.FONT_HERSHEY_DUPLEX # set the font 
            cv2.putText(img, name, (left -20, bottom +75), font, 1.0, (0, 0, 255), 2) # set the text parameters 
```
```
    ### return the image with face names if found ###
    while True: 
        cv2.imshow('Face Recgonition Results', img) # show the title and image 
        if cv2.waitKey(1) & 0xFF == ord('q'): # set wait key and q exit command 
            return face_names 
```
```
### run the function on the image to search ### 
print(search_face('Barak_Joe.jpg')) # alternative example 
```
![FaceRec](https://github.com/CVanchieri/DSPortfolio/blob/master/assets/images/ImageFacialRecognition/BarakJoe.png?raw=true) <br>
```
print(search_face('test_images/Jumanji_Cast.jpg'))
```
![FaceRec](https://github.com/CVanchieri/DSPortfolio/blob/master/assets/images/ImageFacialRecognition/JumanjiCast.png?raw=true) <br>

#### Summary
I have been working on increasing my knowledge on computer vision techniques and the OpenCV library is a really great tool and not super difficult to use.  I am looking forward to seeing how this is works and is implemented in a more advanced way such as live video.  More and more computer vision is implemented everywhere around us, it makes it more itneresting and fun knowing the behind the scenes of how it may be working.

Any suggestions or feedback is greatly appreciated, I am still learning and am always open to suggestions and comments.

GitHub repo
[Link]({{'https://github.com/CVanchieri/DSPortfolio/tree/master/posts/OpenCVImageFacialRecognitionPost'}})





---
[[<< Back]](https://cvanchieri.github.io/DSPortfolio/Tile1_Projects.html)
