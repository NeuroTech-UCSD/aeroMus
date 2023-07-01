#include <MPU9255.h>

bool MPU9255::update()
{
	// get raw data
	a[0] = getAccelX_mss() * MSS_TO_G * 1000;
	a[1] = getAccelY_mss() * MSS_TO_G * 1000;
	a[2] = getAccelZ_mss() * MSS_TO_G * 1000;

	g[0] = getGyroX_rads();
	g[1] = getGyroY_rads();
	g[2] = getGyroZ_rads();

	m[0] = getMagX_uT();
	m[1] = getMagY_uT();
	m[2] = getMagZ_uT();

	// convert to same coordinate frame
    float an = -a[0];	// mG
    float ae = +a[1];	// mG
    float ad = +a[2];	// mG
    float gn = +g[0];	// rad/s
    float ge = -g[1];	// rad/s
    float gd = -g[2];	// rad/s
    float mn = +m[1];	// uT
    float me = -m[0];	// uT
    float md = +m[2];	// uT

	// create update arrays
    float _a[3] = {an, ae, ad};
    float _g[3] = {gn, ge, gd};
    float _m[3] = {mn, me, md};

	// update filter
    for (size_t i = 0; i < FILTER_ITERATIONS; ++i){
        filter.update(_a,_g,_m,q);
    }

	// convert to euler angles
	update_rpy();
    return true;
}