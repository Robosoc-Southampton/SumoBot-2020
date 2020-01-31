
from controller import *
from bt import connect_bluetooth, BluetoothWriter
from control import *

DRIVE_NORMAL = 0
DRIVE_FORWARD = 1

MAC = "98:D3:32:11:17:5F"
sock = connect_bluetooth(MAC)
writer = BluetoothWriter(sock)
primaryMotors = SpeedController(DRIVE_OPCODE_PRIMARY, writer)
secondaryMotors = SpeedController(DRIVE_OPCODE_SECONDARY, writer)

def scaleSpeeds(l, r):
	return l * 0.7, r * 0.7

def jointControl(l, r):
	lp, rp = scaleSpeeds(l, r)
	secondaryMotors.setSpeeds(l, r)
	primaryMotors.setSpeeds(lp, rp)

def newState():
	return (False, 0)

def control(js, state, dt):
	held = [i for i in range(js.get_numbuttons()) if js.get_button(i)]
	hv = js.get_hat(0)
	nonFullButtons = [b for b in held if b != SQUARE and b != CIRCLE and b != X]

	hp = js.get_axis(RSTICK_H)
	vp = js.get_axis(RSTICK_V)
	lp, rp = transform_axes(hp, vp)

	hs = js.get_axis(LSTICK_H)
	vs = js.get_axis(LSTICK_V)
	ls, rs = transform_axes(hs, vs)

	lhat = hv[0] < -0.5
	rhat = hv[0] > +0.5

	# reset post-release forward state when control taken back
	if abs(hp) > 0.2 or abs(vp) > 0.2 or len(nonFullButtons) > 0 or lhat or rhat:
		state = (False, state[1])

	# reset turn parameter if not turning
	if not lhat and not rhat:
		state = (state[0], 0)

	if X in held: # full forward and keep after release
		primaryMotors.setSpeeds(1, 1)
		secondaryMotors.setSpeeds(1, 1)
		state = (True, state[1])

	elif SQUARE in held: # full left
		primaryMotors.setSpeeds(-0.8, 0.8)
		secondaryMotors.setSpeeds(-1, 1)
		state = (True, state[1])

	elif CIRCLE in held: # full right
		primaryMotors.setSpeeds(0.8, -0.8)
		secondaryMotors.setSpeeds(1, -1)
		state = (True, state[1])

	elif LT in held and RT in held: # full forward
		jointControl(1, 1)

	elif state[0]: # post-release full forward
		primaryMotors.setSpeeds(1, 1)
		secondaryMotors.setSpeeds(1, 1)

	elif lhat: # arc back left
		state = (state[0], min(1, state[1] + dt * 0.5))
		jointControl(-state[1], -1)

	elif rhat: # arc back right
		state = (state[0], min(1, state[1] + dt * 0.5))
		jointControl(-1, -state[1])

	elif LT in held: # partial left
		jointControl(0.3, 1)

	elif RT in held: # partial right
		jointControl(1, 0.3)

	else: # drive normally
		jointControl(lp + ls * 0.2, rp + rs * 0.2)

	return state

try:
	controller_init()
	controller_loop(control, newState())
	controller_cleanup()
	sock.close()

except KeyboardInterrupt:
	pass
