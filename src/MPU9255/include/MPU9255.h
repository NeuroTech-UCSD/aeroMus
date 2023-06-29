#pragma once
#include <Arduino.h>
#include <MPU925X.h>

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

class MPU9255 : public MPU925X
{
	
};