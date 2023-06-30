#pragma once
#include <Arduino.h>
#include <MPU925X.h>
#include <SPI.h>

#if defined DEBUG
	#define debug_begin(x)		Serial.begin(x)
	#define debug(x)			Serial.print(x)
	#define debug2(x,y)			Serial.print(x,y)
	#define debugln(x)			Serial.println(x)
	#define debugln2(x,y)		Serial.println(x,y)
#else
	#define debug_begin(x)
	#define debug(x)
	#define debug2(x,y)
	#define debugln(x)
	#define debugln2(x,y)
#endif

void getIMU();

class MPU9255 : public MPU925X
{
public:
	MPU9255(TwoWire &bus, uint8_t address) : MPU925X(bus, address) {}
	MPU9255(SPIClass &bus, uint8_t csPin) : MPU925X(bus, csPin) {}

	void getAccel(int *accel);
	void getGyro(int *gyro);
	void getMag(int *mag);
};