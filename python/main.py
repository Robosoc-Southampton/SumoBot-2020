
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

def newState():
	return (False, 0)

def control(js, state, dt):
	held = [i for i in range(js.get_numbuttons()) if js.get_button(i)]
	hv = js.get_hat()
	nonFullButtons = [b for b in held if b != SQUARE and b != CIRCLE and b != X]

	hp = js.get_axis(RSTICK_H)
	vp = js.get_axis(RSTICK_V)
	lp, rp = transform_axes(hp, vp)

	hs = js.get_axis(LSTICK_H)
	vs = js.get_axis(LSTICK_V)
	ls, rs = transform_axes(hs, vs)

	lhat = hv < -0.5
	rhat = hv > +0.5

	# reset post-release forward state when control taken back
	if abs(hp) > 0.2 or abs(vp) > 0.2 or len(nonFullButtons) > 0 or lhat or rhat:
		state = (False, state[1])

	# reset turn parameter if not turning
	if not lhat and not rhat:
		state = (state[0], 0)

	if (LT in held and RT in held) or X in held: # full forward
		primaryMotors.setSpeeds(1, 1)
		secondaryMotors.setSpeeds(1, 1)

		# keep full forward after release
		if X in held: state = (True, state[1])

	elif SQUARE in held: # full left
		primaryMotors.setSpeeds(-0.8, 0.8)
		secondaryMotors.setSpeeds(-1, 1)
		state = (True, state[1])

	elif CIRCLE in held: # full right
		primaryMotors.setSpeeds(0.8, -0.8)
		secondaryMotors.setSpeeds(1, -1)
		state = (True, state[1])

	elif state[0]: # post-release full forward
		primaryMotors.setSpeeds(1, 1)
		secondaryMotors.setSpeeds(1, 1)

	elif lhat: # arc back left
		state = (state[0], min(1, state[1] + dt * 1.1))
		primaryMotors.setSpeeds(-state[1], -1)
		secondaryMotors.setSpeeds(0, 0)

	elif rhat: # arc back right
		state = (state[0], min(1, state[1] + dt * 1.1))
		primaryMotors.setSpeeds(-1, -state[1])
		secondaryMotors.setSpeeds(0, 0)

	elif LT in held: # partial left
		primaryMotors.setSpeeds(0.1, 1)
		secondaryMotors.setSpeeds(1, 1)

	elif RT in held: # partial right
		primaryMotors.setSpeeds(1, 0.1)
		secondaryMotors.setSpeeds(1, 1)

	else: # drive normally
		primaryMotors.setSpeeds(lp, rp)
		secondaryMotors.setSpeeds(ls, rs)

	return state

try:
	controller_init()
	controller_loop(control, newState())
	controller_cleanup()
	sock.close()

except KeyboardInterrupt:
	pass
