# author: tedfoodlin
# FRC Vision testing with OpenCV
# Convex hull then contour approximation

import cv2
import numpy as np
import sys

# for use with OSX
sys.path.append('/usr/local/lib/python2.7/site-packages')


# ---------------- CONSTANTS --------------- #
# capture video from camera
cap = cv2.VideoCapture(0)

# lower and upper limits for the green we are looking for (untuned)
lower_green = np.array([30, 20, 10])
upper_green = np.array([70, 255, 255])

# temporary test color (pink highlighter)
lower_pink = np.array([150, 60, 60])
upper_pink = np.array([170, 255, 255])

# center of the frame on a mac
frameCenterY = 716/2
frameCenterX = 1278/2
# ------------------------------------------- #


# ---------------- FUNCTIONS ---------------- #
# removes everything but specified color
def masking(lower, upper):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame,frame,mask=mask)
    return res, mask

# turns a contour into a polygon
def polygon(c):
    hull = cv2.convexHull(c)
    epsilon = 0.025 * cv2.arcLength(hull, True)
    goal = cv2.approxPolyDP(hull, epsilon, True)
    return goal

# detect center
def calc_center(M):
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    return cx, cy
# ------------------------------------------- #


# iterative tracking
while(True):
    ret, frame = cap.read()

    # remove everything but specified color
    res, mask = masking(lower_pink, upper_pink)

    # draw center of camera
    cv2.circle(res, (frameCenterX, frameCenterY), 5, (0, 0, 255), -1)
    # draw line for x position (we have set shooting angles for y)
    cv2.line(res, (frameCenterX, 0), (frameCenterX, frameCenterY * 2), (0, 0, 255), 2)

    # find contour of goal
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour (closest goal) in the mask
        c = max(cnts, key=cv2.contourArea)

        # make sure the largest contour is large enough to be significant
        area = cv2.contourArea(c)
        if area > 1500:
            # make suggested contour into a polygon
            goal = polygon(c)

            # make sure goal contour has 4 sides
            if len(goal) == 4:
                # draw the contour
                cv2.drawContours(res, [goal], 0, (255, 0, 0), 5)

                # calculate centroid
                M = cv2.moments(goal)
                if M['m00'] > 0:
                    cx, cy = calc_center(M)
                    center = (cx, cy)

                    # draw and print center
                    cv2.circle(res, center, 5, (255, 0, 0), -1)
                    print(center)

                    # if it is aligned with the center y-axis
                    # it is ready to shoot
                    if cx < (frameCenterX+10) and cx > (frameCenterX-10):
                        print("X Aligned")
                    # otherwise, tell robot to turn left or right to align with goal
                    else:
                        if cx > frameCenterX:
                            print("Turn Right")
                        elif cx < frameCenterX:
                            print("Turn Left")

                    if cy < (frameCenterY+10) and cy > (frameCenterY-10):
                        print("Y Aligned")
                    # if it is aligned with the center x-axis
                    # that's good, but we don't need that (unless ur 987) lol
                    else:
                        if cy > frameCenterY:
                            print("Aim Lower")
                        elif cy < frameCenterY:
                            print("Aim Higher")
            else:
                print("Goal contour not found")
        else:
            print("Goal contour not found")

        cv2.imshow("res", res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
