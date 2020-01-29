
from controller import *
from bt import connect_bluetooth, BluetoothWriter
from control import *

DRIVE_NORMAL = 0
DRIVE_FORWARD = 1

MAC = "98:D3:32:11:17:5F"
sock = connect_bluetooth(MAC)
writer = BluetoothWriter(sock)
primaryMotors = SpeedController(DRIVE_OPCODE_FRONT, writer) # TODO: swap front/back
secondaryMotors = SpeedController(DRIVE_OPCODE_BACK, writer)

def newState():
	return False

def control(js, state):
	held = [i for i in range(js.get_numbuttons()) if js.get_button(i)]
	nonTriggerButtons = [b for b in held if b != LT and b != RT]

	hp = js.get_axis(RSTICK_H)
	vp = js.get_axis(RSTICK_V)
	lp, rp = transform_axes(hp, vp)

	hs = js.get_axis(RSTICK_H)
	vs = js.get_axis(RSTICK_V)
	ls, rs = transform_axes(hs, vs)

	if hp > 0.2 or vp > 0.2 or len(nonTriggerButtons) > 0:
		state = False

	if LT in held and RT in held: # full forward
		primaryMotors.setSpeeds(1, 1)
		secondaryMotors.setSpeeds(1, 1)

	elif LT in held: # full left
		primaryMotors.setSpeeds(-1, 1)
		secondaryMotors.setSpeeds(-1, 1)
		state = True

	elif RT in held: # full right
		primaryMotors.setSpeeds(1, -1)
		secondaryMotors.setSpeeds(1, -1)
		state = True

	elif state: # full forward after full left/right
		primaryMotors.setSpeeds(1, 1)
		secondaryMotors.setSpeeds(1, 1)

	elif SQUARE in held: # arc back left
		primaryMotors.setSpeeds(-0.3, -1)
		secondaryMotors.setSpeeds(0, 0)

	elif CIRCLE in held: # arc back right
		primaryMotors.setSpeeds(-1, -0.3)
		secondaryMotors.setSpeeds(0, 0)

	else: # drive normally
		primaryMotors.setSpeeds(lp, rp)
		secondaryMotors.setSpeeds(ls, rs)

	return state

try:
	controller_init()
	controller_loop(control, newState())
	controller_cleanup()

except KeyboardInterrupt:
	pass
