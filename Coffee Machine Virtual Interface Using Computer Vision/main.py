import os
from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("Resources/Backgorund Image.png")

folderPathModes = "Resources/Models"
listImgModesPath = (os.listdir(folderPathModes))
listImgModes = []
for imgModePath in listImgModesPath :
    listImgModes.append(cv2.imread(os.path.join(folderPathModes,imgModePath )))


folderPathIcons = "Resources/Icons"
listImgIconsPath = (os.listdir(folderPathIcons))
listImgIcons = []
for imgIconsPath in listImgIconsPath :
    listImgIcons.append(cv2.imread(os.path.join(folderPathIcons, imgIconsPath )))

print(listImgIcons)
modeType = 0

selection = -1
counter = 0
selectionSpeed = 7
detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.8, minTrackCon=0.5)
modePositions = [(793,152),(793,272),(793,406)]
counterPause = 0
selectionList = [-1, -1, -1]
while True:
    success, img = cap.read()


    hands, img = detector.findHands(img, draw=True, flipType=True)
    imgBackground[139:139+480, 50:50+640] = img



    desired_shape = imgBackground[0:720, 847:1280].shape


    resized_img = cv2.resize(listImgModes[modeType], (desired_shape[1], desired_shape[0]))


    imgBackground[0:720, 847:1280] = resized_img




    if hands and counterPause == 0 and modeType < 3 :

        hand1 = hands[0]

        fingers1 = detector.fingersUp(hand1)
        print(f'H1 = {fingers1.count(1)}', end=" ")

        if fingers1.count(1) == 1:
            if selection != 1:
                counter = 1
            selection = 1
        elif fingers1.count(1) == 2:
            if selection != 2:
                counter = 1
            selection = 2
        elif fingers1.count(1) == 3:
            if selection != 3:
                counter = 1
            selection = 3
        elif fingers1.count(1) == 4 :
            if selection != 4 :
                 counter = 1
            selection = 4
        else:
            selection = -1
            counter = 0
        if counter > 0:
            counter += 1
            print(counter)

            cv2.ellipse(imgBackground, modePositions[modeType], (43, 43), 0, 0, counter * selectionSpeed,
                        (0, 255, 0), 10)

            if counter*selectionSpeed>360:
                selectionList[modeType] = selection
                modeType += 1
                counter = 0
                selection = -1
                counterPause = 1

    if counterPause > 0:
        counterPause += 1
        if counterPause > 60:
            counterPause = 0

    if selectionList[0] != -1 :
        resized_icon = cv2.resize(listImgIcons[selectionList[0] - 1], (65, 28))
        imgBackground[126:126 + 28, 763:763 + 65] = resized_icon
    if selectionList[1] != -1 :
        resized_icon = cv2.resize(listImgIcons[3 + selectionList[1]], (65, 28))
        imgBackground[256:256 + 28, 763:763 + 65] = resized_icon
    if selectionList[2] != -1 :
        resized_icon = cv2.resize(listImgIcons[7 + selectionList[2]], (65, 28))
        imgBackground[400:400 + 28, 763:763 + 65] = resized_icon



    cv2.imshow("BackgroundImage", imgBackground)
    cv2.waitKey(1)