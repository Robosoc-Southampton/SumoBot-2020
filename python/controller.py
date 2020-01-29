
from time import sleep

import pygame

def controller_init():
	pygame.init()
	pygame.joystick.init()

def controller_loop(fn):
	running = True

	while running:
		try:
			while pygame.joystick.get_count() == 0:
				print("No joystick connected, waiting...")
				sleep(1)

			js = pygame.joystick.Joystick(0)
			js.init()

			print(f"Connected to joystick {js.get_name()}")
			print(f"\tHas {js.get_numaxes()} axes, {js.get_numballs()} balls, " +
				f"{js.get_numbuttons()} buttons, and {js.get_numhats()} hats")

			while running:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						running = False

				fn(js)

			js.quit()

		except Exception as e:
			# No joystick found, wait for a bit before trying again

			print("Something went wrong in controller loop:")
			print(e)
			sleep(0.1)

def controller_cleanup():
	pygame.joystick.quit()
	pygame.quit()
