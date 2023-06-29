#include <MPU9255.h>

void MPU9255::getAccel(int *accel)
{
    accel[0] = getAccelX_mss();
    accel[1] = getAccelY_mss();
    accel[2] = getAccelZ_mss();
}

void MPU9255::getGyro(int *gyro)
{
    gyro[0] = getGyroX_rads();
    gyro[1] = getGyroX_rads();
    gyro[2] = getGyroX_rads();
}

void MPU9255::getMag(int *mag)
{
    mag[0] = getMagX_uT();
    mag[1] = getMagY_uT();
    mag[2] = getMagZ_uT();
}