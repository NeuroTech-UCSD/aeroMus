/**
 * @file main.cpp
 * @author Gavin Roberts (gsroberts@ucsd.edu)
 * @brief Sets up a MPU925XFIFO object in SPI mode and prints out the raw data
 * @version 0.1
 * @date 2023-06-28
 * 
 * @copyright Copyright Triton NeuroTech (c) 2023
 */
#include <MPU9255.h>

// an MPU925X object with the MPU-925X sensor on SPI bus 0 and chip select pin 10
MPU9255 IMU(SPI, 10);
int status;

int[3] accel;
int[3] gyro;
int[3] mag;

void getIMU();

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
    status = IMU.setDlpfBandwidth(MPU925X::DLPF_BANDWIDTH_20HZ);
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
    // display the data
    debug2(IMU.getAccelX_mss(), 6);
    debug("\t");
    debug2(IMU.getAccelY_mss(), 6);
    debug("\t");
    debug2(IMU.getAccelZ_mss(), 6);
    debug("\t");
    debug2(IMU.getGyroX_rads(), 6);
    debug("\t");
    debug2(IMU.getGyroY_rads(), 6);
    debug("\t");
    debug2(IMU.getGyroZ_rads(), 6);
    debug("\t");
    debug2(IMU.getMagX_uT(), 6);
    debug("\t");
    debug2(IMU.getMagY_uT(), 6);
    debug("\t");
    debug2(IMU.getMagZ_uT(), 6);
    debug("\t");
    debugln2(IMU.getTemperature_C(), 6);
}
