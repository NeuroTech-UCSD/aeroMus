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

float accel[3];
float gyro[3];
float mag[3];

// IMU registers
int status;

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
	
	debug("Setting digital LPF bandwidth to 20 Hz: ");
    status = IMU.setDlpfBandwidth(MPU9255::DLPF_BANDWIDTH_20HZ);
	debugln( status > 0 ? "Success" : "Failure! Exit code: " + status );

	debug("Setting default sdr (19): ");
    status = IMU.setSrd(DEFAULT_SDR);
	debugln( status > 0 ? "Success" : "Failure! Exit code: " + status );

	debug("Enabling data ready interrupt: ");
    status = IMU.enableDataReadyInterrupt();
	debugln( status > 0 ? "Success" : "Failure! Exit code: " + status );

	calibrateIMU();

	debugln("Setting interrupt pin active high");
    pinMode(2, INPUT);
    attachInterrupt(0, getIMU, RISING);
	// pinMode(3, INPUT);
	// attachInterrupt(1, calibrateIMU, RISING);

	debugln("IMU initialized successfully");
	
}


void loop() {
	
}

void getIMU()
{
    // read the sensor
    IMU.readSensor();
	
	// get the data
	IMU.update();

	float rpy[3];
	IMU.getRPY(rpy);

	debug("Roll: ");
	debug2(rpy[0], 6);
	debug(", Pitch: ");
	debug2(rpy[1], 6);
	debug(", Yaw: ");
	debugln2(rpy[2], 6);
}

void calibrateIMU()
{
	debugln("Calibrating IMU");
	debug("Now calibrating accelerometer: ");
	status = IMU.calibrateAccel();
	debugln( status > 0 ? "Success" : "Failure! Exit code: " + status );
	debug("Now calibrating gyroscope: ");
	status = IMU.calibrateGyro();
	debugln( status > 0 ? "Success" : "Failure! Exit code: " + status );
	debug("Now calibrating magnetometer: ");
	status = IMU.calibrateMag();
	debugln( status > 0 ? "Success" : "Failure! Exit code: " + status );
	debugln("Calibration complete");
}