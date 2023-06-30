/**
 * @file main.cpp
 * @author Gavin Roberts (gsroberts@ucsd.edu)
 * @brief Sets up a MPU9255 object in SPI mode and tracks the relative motion of the sensor 
 * @version 0.1
 * @date 2023-06-28
 * 
 * @copyright Copyright Triton NeuroTech (c) 2023
 */
#include <MPU9255.h>

// an MPU9255 object on SPI bus 0 and chip select pin 10
MPU9255 IMU(SPI, 10);

// IMU registers
int status;

// Measured IMU data
float accel[3]; 	// m/s^2
float gyro[3];		// rad/s
float mag[3]; 		// uT

// Differential IMU data
float da[3];		// m/s^2
float dg[3];		// rad/s
float dm[3];		// uT

// Estimated Attitude data
float quat[4];		// Quaternion
float pos[3];		// m
float velocity[3];	// m/s

// Time data
float dt;			// s
float t;			// s

void setup()
{
    // serial to display data
    debug_begin(115200);
	#if defined debug_print
    while (!Serial)
    {
    }
	#endif

    // start communication with IMU
	debugln("Initializing IMU");
    status = IMU.begin();
	debugln("Status Recieved");
    if (status < 0)
    {
        debugln("IMU initialization unsuccessful");
        debugln("Check IMU wiring or try cycling power");
        debug("Status: ");
        debugln(status);
        while (1)
        {
        }
    }
	
	debugln("Setting DLPF bandwidth to 20 Hz");
    status = IMU.setDlpfBandwidth(MPU9255::DLPF_BANDWIDTH_20HZ);
	debugln( status > 0 ? "Success" : "Failure" );

	debugln("Setting SRD to 19 for a 50 Hz update rate");
    status = IMU.setSrd(19);
	debugln( status > 0 ? "Success" : "Failure" );

	debugln("Enabling data ready interrupt");
    status = IMU.enableDataReadyInterrupt();
	debugln( status > 0 ? "Success" : "Failure" );

	debugln("Setting interrupt pin active high");
    pinMode(0, INPUT);
    attachInterrupt(0, getIMU, RISING);

	debugln("IMU initialized successfully");
}

void loop() {
	
}

void getIMU()
{
    // read the sensor
    IMU.readSensor();
    // // display the data
    // debug2(IMU.getAccelX_mss(), 6);
    // debug("\t");
    // debug2(IMU.getAccelY_mss(), 6);
    // debug("\t");
    // debug2(IMU.getAccelZ_mss(), 6);
    // debug("\t");
    // debug2(IMU.getGyroX_rads(), 6);
    // debug("\t");
    // debug2(IMU.getGyroY_rads(), 6);
    // debug("\t");
    // debug2(IMU.getGyroZ_rads(), 6);
    // debug("\t");
    // debug2(IMU.getMagX_uT(), 6);
    // debug("\t");
    // debug2(IMU.getMagY_uT(), 6);
    // debug("\t");
    // debug2(IMU.getMagZ_uT(), 6);
    // debug("\t");
    // debugln2(IMU.getTemperature_C(), 6);
}
