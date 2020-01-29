
from controller import controller_loop

def control(js):
	axes = [js.get_axis(i) for i in range(js.get_numaxes())]
	# hats = [js.get_hat(i) for i in range(js.get_numhats())]
	buttons = [js.get_button(i) for i in range(js.get_numbuttons())]

	if any(abs(value) > 0.05 for value in axes):
		print(axes)

	if any(pressed for pressed in buttons):
		print(buttons)

try:
	controller_loop(control)
except KeyboardInterrupt:
	pass
