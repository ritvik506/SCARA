'''
Detects Rectangle and prints which direction the shape is wrt centre of frame
Logic- 
Find centre of frame
Find centre of Rectangle
Compare the Centres to identify which quadrant the shape is in
Finds the x distance and y distance between the midpoint and shape-centre
Rotate the Servo to align x and y coordinates- Angle of rotation calculated by inverse kinematics
Stop the motion once the x and y distances fall below 5 pixels
'''
import cv2
# import RPi.GPIO as GPIO
# from time import sleep
import math

theta1, theta2 = 0, 0

# Setting up the GPIO Pins for PWM
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(11, GPIO.OUT)
# GPIO.setup(3, GPIO.OUT)
# servo_1 = GPIO.pwm(11, 50)
# servo_2 = GPIO.pwm(3, 50)


def main():
    '''
    cap=cv2.VideoCapture(0)
    while True:
        ret,frame=cap.read()
        # print(f"Midpoint {midpoint}")
        midpoint=find_midpoint(frame)
        cv2.circle(frame,midpoint,10,(255,0,0),-1)
        find_shape(frame)
        if cv2.waitKey(1)==ord('q'):
            break
    '''

    frame = cv2.imread("Shapes_img2.jpg")
    while True:  # Loop runs till the centre of the shape aligns with centre of frame
        midpoint = find_midpoint(frame)
        shape_centre = find_shape(frame)
        flag = decide_quadrant(frame, midpoint, shape_centre)
        if flag == 1:
            break

        cv2.imshow("frame", frame)
        cv2.waitKey(10)
    cv2.destroyAllWindows()


def find_midpoint(img):  # Finds the midpoint of camera feed(frame) and marks a point
    size = img.shape
    midpoint = []
    for i in range(2):
        midpoint.append(int(size[i]/2))
    midpoint = (midpoint[1], midpoint[0])
    cv2.circle(img, midpoint, 5, (255, 0, 0), -1)
    return midpoint


# def SetAngle():  # Sets the angle(obtained from IK), to each Servo motor
#     global theta1
#     global theta2
#     duty_1 = theta1 / 18 + 2
#     duty_2 = theta2 / 18 + 2

#     GPIO.output(3, True)
#     GPIO.output(11, True)

#     servo_1.ChangeDutyCycle(duty_1)
#     servo_2.ChangeDutyCycle(duty_2)
#     sleep(1)
#     GPIO.output(3, False)
#     GPIO.output(11, False)
#     servo_1.ChangeDutyCycle(0)
#     servo_2.ChangeDutyCycle(0)


def find_shape(img):  # Finds the Rectangle in an array of shapes and marks the centre of the shape. This is compared to the midpoint of the frame and accordingly the servos are instructed to rotate.
    imgGry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thrash = cv2.threshold(imgGry, 240, 255, cv2.CHAIN_APPROX_NONE)
    contours, hierarchy = cv2.findContours(
        thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    max_area = 0
    cnts = []
    for contour in contours:
        # cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            cnts.append(contour)
    cnt = sorted(contours, key=lambda x: cv2.contourArea(x))[-1]
    # cv2.drawContours(img, cnt, -1, (0, 255, 0), 3)
    M = cv2.moments(cnt)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    shape_centre = (cX, cY)
    cv2.circle(img, shape_centre, 5, (0, 0, 255), -1)
    return shape_centre


# The Shape position is obtained wrt midpoint of frame. The x and y distance is then calculated and subsequently the angle of rotation.
def decide_quadrant(img, midpoint, shape_centre):
    global theta1
    global theta2

    x_mid, y_mid = midpoint[0], -midpoint[1]  # making y coordinate positive
    x, y = shape_centre[0], -shape_centre[1]

    x_dist = x-x_mid
    y_dist = y-y_mid

    if(x > x_mid):
        if(y > y_mid):
            print("Shape is on top-right of centre")

        else:
            print("Shape is bottom-right of centre")

    else:
        if(y > y_mid):
            print("Shape is on top-left of centre")
        else:
            print("Shape is bottom-right of centre")
    print(f"X distance={x_dist}\nY distance={y_dist}")

    if(abs(y-y_mid) < 5 and abs(x-x_mid) < 5):
        return 1
    else:
        # Servo rotation based on difference
        x_dist /= 10
        y_dist /= 10
        theta1 = math.acos(x_dist/(math.sqrt(x_dist ** 2+y_dist ** 2))) - \
            math.acos((x_dist ** 2+y_dist ** 2+125) /
                      (30*math.sqrt(x_dist ** 2+y_dist ** 2)))
        theta2 = math.acos((x_dist-15*math.cos(theta1))/10)-theta1
        print(
            f"Theta1: {theta1*180/math.pi}\nTheta2: {theta2*180/math.pi}")
        # SetAngle()
        return 0


if __name__ == "__main__":
    main()
