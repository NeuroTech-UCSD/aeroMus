
// copy and paste into preferences: https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json

const int analogInPin0 = A0;  //MAKE SURE THESE ARE CORRECT. 
const int analogInPin1 = A1;

int value0 = 0;        // value read from the pot
int value1 = 0;        // value output to the PWM (analog out)

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  // read the analog in value:
  value0 = analogRead(analogInPin0);
  value1 = analogRead(analogInPin1);

  // print the results to the Serial Monitor:
  Serial.println((String)(value0 + "," + value1));

  // wait 2 milliseconds before the next loop for the analog-to-digital
  // converter to settle after the last reading:
  delay(2);
}
