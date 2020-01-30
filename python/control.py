
from time import clock

FREQUENCY = 20
DRIVE_OPCODE_PRIMARY = 25
DRIVE_OPCODE_SECONDARY = 26
TIMEOUT = 1
FORWARD = ord('F')
BACKWARD = ord('B')

LSTICK_H = 0
LSTICK_V = 1
RSTICK_H = 2
RSTICK_V = 3

X = 0
CIRCLE = 1
SQUARE = 3
TRIANGLE = 4
LT = 6
RT = 7
LT2 = 8
RT2 = 9
LSTICK = 13
RSTICK = 14

################################################################################

def sign(x):
	return 1 if x >= 0 else -1

def transform_axes(horizontal, vertical):
	l = sqrt(horizontal * horizontal + vertical * vertical)

	if l == 0:
		return 0, 0
	elif l < 0.3:
		horizontal *= 0.3 / l
		vertical *= 0.3 / l

	speed = -vertical
	turnSpeed = 0.75 * horizontal / (1 + abs(speed))
	speedScale = 1 / (0.01 + abs(speed) + abs(turnSpeed))

	if speedScale > 1: speedScale = 1

	return (speed + turnSpeed) * speedScale, (speed - turnSpeed) * speedScale

################################################################################


class SpeedController:
	def __init__(self, opcode, writer):
		self.__writer = writer
		self.__opcode = opcode
		self.__ll = None
		self.__lr = None
		self.__lt = -1000 # pro skills

	def setSpeeds(self, left, right):
		time = clock()

		left = min(max(int(left * 127), -127), 127)
		right = min(max(int(right * 127), -127), 127)

		if left != self.__ll or right != self.__lr or time - self.__lt > TIMEOUT / 2:
			if time - self.__lt > 1/FREQUENCY:
				self.__ll = left
				self.__lr = right
				self.__lt = time

				lf = FORWARD
				rf = FORWARD

				if left < 0:
					lf = BACKWARD
					left = -left

				if right < 0:
					rf = BACKWARD
					right = -right

				self.__writer.write(self.__opcode, lf, left, rf, right)
