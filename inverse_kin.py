import math

x = 15
y = 15

theta1 = math.acos(x/(math.sqrt(x ** 2+y ** 2))) - \
    math.acos((x ** 2+y ** 2+125)/(30*math.sqrt(x ** 2+y ** 2)))
theta2 = math.acos((x-15*math.cos(theta1))/10)-theta1
print(f"Theta1: {theta1*180/math.pi}\nTheta2: {theta2*180/math.pi}")
