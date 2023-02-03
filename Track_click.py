import cv2
import numpy as np
import imutils

tracker = cv2.TrackerCSRT_create()
cap = cv2.VideoCapture('test.mp4')

# camera görüntüsü için
#cap = cv2.VideoCapture(0)

ix, iy = -1, -1
clicked = 0

def mouseCallback(event, x, y, flags, param):
    global ix
    global iy
    global clicked
    global rectangle

    if event == cv2.EVENT_LBUTTONDOWN:
        ix = x  # saves the position of the last click
        iy = y
        rect = ix, iy, 15, 15
        tracker.init(img, rect)
        clicked = 1

        print(clicked)


cv2.namedWindow('img')
cv2.setMouseCallback('img', mouseCallback)  # mouse callback has to be set only once

while True:
    _, img = cap.read()

    img = imutils.resize(img, width=1024)
    #img = cv2.resize(img, (640, 480))

    sensitivity = 100
    low = np.array([0, 0, 255 - sensitivity])
    high = np.array([255, sensitivity, 255])
    mask = cv2.inRange(img, low, high)

    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, tresh = cv2.threshold(hsv, 220, 255, 0)
    contours, hierarchy = cv2.findContours(tresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



    if clicked == 1:
        track_success, rectan = tracker.update(img)
        if track_success:
            print(rectan[0], rectan[1])
            cv2.circle(img, (rectan[0], rectan[1]), 15, (0, 0, 255), 2)

    # cv2.imshow('img',img)
    # cv2.imshow('mask',mask)

    cv2.imshow('tresh', tresh)
    cv2.imshow("img", img)

    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
