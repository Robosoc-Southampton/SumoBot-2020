
#include "include/L298.h"

L298 frontMotors;

void setup() {
	Serial.begin(9600);

	frontMotors.setLeftMotorPins(9, 6, 7);
	frontMotors.setRightMotorPins(3, 4, 5);
	frontMotors.setup();
}

void loop() {
	while (!Serial.available()); Serial.read();

	frontMotors.setLeftMotorSpeed(-255);
	frontMotors.setRightMotorSpeed(255);

	delay(1000);

	frontMotors.stop();
}
