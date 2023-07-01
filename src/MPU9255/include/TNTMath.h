#pragma once
#include <math.h>

#define PI 3.1415926535897932384626433832795
// #define DEG_TO_RAD 0.01745329251994329576923690768489
// #define RAD_TO_DEG 57.295779513082320876798154814105
#define MSS_TO_G 1.0 / 9.80665

namespace TNT {

    /**
     * @brief 3D Vector
     * 
     */
    typedef union {
        float array[3];

        struct {
            float x;
            float y;
            float z;
        } axis;
    } Vector3;

    /**
     * @brief Quaternion
     * 
     */
    typedef union {
        float array[4];

        struct {
            float w;
            float x;
            float y;
            float z;
        } element;
    } Quaternion;

    /**
     * @brief A 3x3 matrix in row-major order
     * 
     */
    typedef union {
        float array[3][3];

        struct {
            float m00;
            float m01;
            float m02;
            float m10;
            float m11;
            float m12;
            float m20;
            float m21;
            float m22;
        } element;
    } Matrix3x3;
}