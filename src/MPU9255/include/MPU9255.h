#pragma once
#include <Arduino.h>
#include <MPU925X.h>
#include <Madgwick.h>
#include <TNTMath.h>
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


#define DEFAULT_SDR 19
#define DEFAULT_SAMPLE_RATE 1000 / (DEFAULT_SDR + 1) 		// default: 50 Hz
#define MICROS_PER_READING 1000000 / DEFAULT_SAMPLE_RATE 	// default: 20000 us

#define FILTER_ITERATIONS 1
#define DEFAULT_MAGNETIC_DECLINATION 11.09f // San Diego June 30, 2023

void getIMU();
void calibrateIMU();

class MPU9255 : public MPU925X
{
public:
	MPU9255(TwoWire &bus, uint8_t address) : MPU925X(bus, address) {}
	MPU9255(SPIClass &bus, uint8_t csPin) : MPU925X(bus, csPin) {}

	float magnetic_declination = DEFAULT_MAGNETIC_DECLINATION;

	float a[3] {0.f, 0.f, 0.f};
    float g[3] {0.f, 0.f, 0.f};
    float m[3] {0.f, 0.f, 0.f};
	float q[4] = {1.0f, 0.0f, 0.0f, 0.0f};
	float rpy[3] {0.f, 0.f, 0.f};
	float lin_acc[3] {0.f, 0.f, 0.f};

	Madgwick filter;

	bool update();
	void update_rpy() {
		float qw, qx, qy, qz;
		qw = q[0];
		qx = q[1];
		qy = q[2];
		qz = q[3];
		float a12, a22, a31, a32, a33;
        a12 = 2.0f * (qx * qy + qw * qz);
        a22 = qw * qw + qx * qx - qy * qy - qz * qz;
        a31 = 2.0f * (qw * qx + qy * qz);
        a32 = 2.0f * (qx * qz - qw * qy);
        a33 = qw * qw - qx * qx - qy * qy + qz * qz;
        rpy[0] = atan2f(a31, a33);
        rpy[1] = -asinf(a32);
        rpy[2] = atan2f(a12, a22);
        rpy[0] *= 180.0f / PI;
        rpy[1] *= 180.0f / PI;
        rpy[2] *= 180.0f / PI;
        rpy[2] += magnetic_declination;
        if (rpy[2] >= +180.f)
            rpy[2] -= 360.f;
        else if (rpy[2] < -180.f)
            rpy[2] += 360.f;

        lin_acc[0] = a[0] + a31;
        lin_acc[1] = a[1] + a32;
        lin_acc[2] = a[2] - a33;
	}

	void getRPY(float *rtn_rpy){
		rtn_rpy[0] = rpy[0];
		rtn_rpy[1] = rpy[1];
		rtn_rpy[2] = rpy[2];
	}
};