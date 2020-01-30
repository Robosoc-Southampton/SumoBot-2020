
#include "include/L298.h"

#define TIMEOUT 1000
#define PRIMARY_MOTOR_CONTROL 25
#define SECONDARY_MOTOR_CONTROL 26

L298 primaryMotors;
L298 secondaryMotors;
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
	primaryMotors.stop();
	secondaryMotors.stop();
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
	return Serial.read();
}

// returns a speed scaler for a given direction
int direction(int i) {
	return i == 'F' ? 1 : -1;
}

void setup() {
	Serial.begin(9600);

	pinMode(LED_BUILTIN, OUTPUT);
	pinMode(A0, OUTPUT);
	pinMode(A1, OUTPUT);
	pinMode(A2, OUTPUT);
	pinMode(A3, OUTPUT);
	pinMode(10, OUTPUT);
	pinMode(11, OUTPUT);

	// set up the primary motor pins
	primaryMotors.setLeftMotorPins(9, 6, 7);
	primaryMotors.setRightMotorPins(3, 4, 5);
	primaryMotors.setup();

	secondaryMotors.setLeftMotorPins(10, A1, A0);
	secondaryMotors.setRightMotorPins(11, A2, A3);
	secondaryMotors.setup();

	// initialise a timer
	lastCommandTime = millis();

	notify();
}

void loop() {
	if (Serial.available() >= 5) {
		int opcode = read_num();
		int lf = read_num();
		int ls = read_num();
		int rf = read_num();
		int rs = read_num();
		int l = ls * direction(lf) * 2;
		int r = rs * direction(rf) * 2;

		lastCommandTime = millis();

		if (opcode == PRIMARY_MOTOR_CONTROL) {
			primaryMotors.setLeftMotorSpeed(l);
			primaryMotors.setRightMotorSpeed(r);
		}
		else if (opcode == SECONDARY_MOTOR_CONTROL) {
			secondaryMotors.setLeftMotorSpeed(l);
			secondaryMotors.setRightMotorSpeed(r);
		}
		else {
			notify();
		}
	}

	checkTimeout();
}
