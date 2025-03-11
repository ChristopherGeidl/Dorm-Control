#include <ESP32Servo.h>

static const int servoPin = 13;

Servo servo;

void setup() {

  Serial.begin(921600);
  servo.attach(servoPin);
  servo.write(0);
}

void loop() {
  servo.write(90);
  delay(1000);
  servo.write(180);
  delay(1000);
  servo.write(0);
  delay(2000);
}