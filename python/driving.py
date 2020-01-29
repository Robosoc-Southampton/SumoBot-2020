
from time import clock

FREQUENCY = 20
DRIVE_OPCODE = 25
TIMEOUT = 1
FORWARD = ord('F')
BACKWARD = ord('B')

class SpeedController:
	def __init__(self, writer):
		self.__writer = writer
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

				print(chr(lf), left, chr(rf), right)

				self.__writer.write(DRIVE_OPCODE, lf, left, rf, right)
