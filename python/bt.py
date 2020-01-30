
import bluetooth
import struct

def connect_bluetooth(mac: str):
	try:
		print(f"Connecting to MAC address {mac}")
		sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		sock.connect((mac, 1))
		print(f"Connected to {mac}")

		return sock

	except bluetooth.btcommon.BluetoothError as e:
		print(e)
		return None

class BluetoothWriter:
	def __init__(self, sock):
		self.__socket = sock

	# opcode and params must be 0-127
	def write(self, opcode: int, *params: int):
		integers = [opcode, *params]
		print(integers)
		data = "".join(chr(c) for c in integers)
		self.__socket.send(data)
