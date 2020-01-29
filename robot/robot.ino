
#include "include/L298.h"

#define TIMEOUT 1000

L298 frontMotors;
long lastCommandTime;

// flash the LED, used for debugging mostly
void notify() {
	digitalWrite(LED_BUILTIN, HIGH);
	delay(1000);
	digitalWrite(LED_BUILTIN, LOW);
	delay(1000);
}

// called when the robot hits a timeout for receiving input
void abort() {
	frontMotors.stop();
}

// checks for a timeout and aborts if timeout has occurred
void checkTimeout() {
	if (millis() - lastCommandTime > TIMEOUT) {
		abort();
	}
}

// reads an integer from serial, blocking until one is available
int read_num() {
	while (!Serial.available()) checkTimeout();
	int b0 = Serial.read();
	return b0;
}

// returns a speed scaler for a given direction
int direction(int i) {
	return i == 'F' ? 1 : -1;
}

void setup() {
	Serial.begin(9600);
	pinMode(LED_BUILTIN, OUTPUT);

	// set up the front motor pins
	frontMotors.setLeftMotorPins(9, 6, 7);
	frontMotors.setRightMotorPins(3, 4, 5);
	frontMotors.setup();

	// initialise a timer
	lastCommandTime = millis();

	notify();
}

void loop() {
	if (Serial.available() < 5) {
		int opcode = read_num();

		switch (opcode) {
			case 25:
				int lf = read_num();
				int ls = read_num();
				int rf = read_num();
				int rs = read_num();

				frontMotors.setLeftMotorSpeed(ls * direction(lf) * 2);
				frontMotors.setRightMotorSpeed(rs * direction(rf) * 2);
				lastCommandTime = millis();

				break;
		}
	}

	checkTimeout();
}
