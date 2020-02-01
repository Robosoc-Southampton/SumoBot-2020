
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

def scaleSpeed(s):
	return s * 0.5

def jointControl(l, r):
	secondaryMotors.setSpeeds(l, r)
	primaryMotors.setSpeeds(scaleSpeed(l), scaleSpeed(r))

def newState():
	return (False, False)

def control(js, state, dt):
	held = [i for i in range(js.get_numbuttons()) if js.get_button(i)]
	hv = js.get_hat(0)
	nonFullButtons = [b for b in held if b != LT and b != RT and b != X and b != LT2 and b != RT2]

	hp = js.get_axis(RSTICK_H)
	vp = js.get_axis(RSTICK_V)

	hs = js.get_axis(LSTICK_H)
	vs = js.get_axis(LSTICK_V)

	if (abs(hs) > abs(hp)):
		hp = hs

	if (abs(vs) > abs(vp)):
		vp = vs
		
	lp, rp = transform_axes(hp, vp)

	lhat = hv[0] < -0.5
	rhat = hv[0] > +0.5

	# reset post-release forward state when control taken back
	if abs(hp) > 0.2 or abs(vp) > 0.2 or len(nonFullButtons) > 0:
		state = (False, False)

	if X in held: # full forward keep
		primaryMotors.setSpeeds(1, 1)
		secondaryMotors.setSpeeds(1, 1)
		state = (True, False)

	elif LT in held: # full left keep
		primaryMotors.setSpeeds(-0.8, 0.8)
		secondaryMotors.setSpeeds(-1, 1)
		state = (True, False)

	elif RT in held: # full right keep
		primaryMotors.setSpeeds(0.8, -0.8)
		secondaryMotors.setSpeeds(1, -1)
		state = (True, False)

	elif LT2 in held: # back left keep
		primaryMotors.setSpeeds(-0.8, 0.8)
		secondaryMotors.setSpeeds(-1, 1)
		state = (False, True)

	elif RT2 in held: # back right keep
		primaryMotors.setSpeeds(0.8, -0.8)
		secondaryMotors.setSpeeds(1, -1)
		state = (False, True)

	elif state[0]: # post-release full forward
		primaryMotors.setSpeeds(1, 1)
		secondaryMotors.setSpeeds(1, 1)

	elif state[1]: # post-release full backward
		jointControl(-1, -1)

	elif SQUARE in held and CIRCLE in held: # partial forward
		jointControl(1, 1)

	elif SQUARE in held: # partial left
		jointControl(0.3, 1)

	elif CIRCLE in held: # partial right
		jointControl(1, 0.3)

	else: # drive normally
		jointControl(lp, rp)

	return state

try:
	controller_init()
	controller_loop(control, newState())
	controller_cleanup()
	sock.close()

except KeyboardInterrupt:
	pass
