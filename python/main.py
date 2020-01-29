
from controller import *
from bt import connect_bluetooth, BluetoothWriter
from driving import SpeedController

MAC = "98:D3:32:11:17:5F"
sock = connect_bluetooth(MAC)
writer = BluetoothWriter(sock)
speed = SpeedController(writer)

writer.write(25, ord('F'), 127, ord('F'), 127)

def control(js):
	# axes = [js.get_axis(i) for i in range(js.get_numaxes())]
	# hats = [js.get_hat(i) for i in range(js.get_numhats())]
	buttons = [js.get_button(i) for i in range(js.get_numbuttons())]

	# if any(abs(value) > 0.05 for value in axes):
	# 	print(axes)

	if any(pressed for pressed in buttons):
		print(buttons)

	speed.setSpeeds(js.get_axis(0), js.get_axis(1))

try:
	controller_init()
	controller_loop(control)
	controller_cleanup()

except KeyboardInterrupt:
	pass
