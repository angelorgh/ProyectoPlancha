#include "WString.h"
#include <AccelStepper.h>
#include <Servo.h>
#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include <PID_v2.h>
//////////////////////////////////////////////////////////////////
int status = 0 ;
int time;
int x=0;
int flag=0; // flag para esperar por el inicio del codigo 

//////////////////////////////////////////////////////////////////
Adafruit_MLX90614 mlx = Adafruit_MLX90614();
//////////////////////////////////////////////////////////////////
#define ENA1A                2
#define ENA1B                3

#define ENA2A                18
#define ENA2B                19

#define stepAngleMotor 0.225           // Step angle (grados/paso)
#define stepAngleEncoder 360/(600*2)       // Step angle encoder 360 (grados/rev) / (600 (pulsos/rev) * 2 (pasos/pulso))  = (grados/paso)

volatile long EncoderENA1 = 0;
volatile long EncoderENA2 = 0;
//////////////////////////////////////////////////////////////////
#define RDOOR_PUL            34
#define RDOOR_DIR            36
#define RDOOR_ENA            38
#define MGTRDOOR_SWITCH      11
#define RDOOR_SPEED          750
#define RDOOR_ACCEL          300
#define ABRE                 1
#define CIERRA               2
#define RDOOROPEN            4000
#define RDOORCLOSE           -4000
AccelStepper RDOOR(AccelStepper::DRIVER, RDOOR_PUL, RDOOR_DIR);
//////////////////////////////////////////////////////////////////
#define LDOOR_PUL            48
#define LDOOR_DIR            50
#define LDOOR_ENA            52
#define MGTLDOOR_SWITCH      12
#define LDOOR_SPEED          750
#define LDOOR_ACCEL          300
AccelStepper LDOOR(AccelStepper::DRIVER, LDOOR_PUL, LDOOR_DIR);
//////////////////////////////////////////////////////////////////
#define CLOTHE_PUL        49
#define CLOTHE_DIR        51
#define CLOTHE_ENA        53
#define CLOTHE_SWITCH     8
#define CLOTHE_SPEED      2000
#define CLOTHE_ACCEL      1250
AccelStepper CLOTHE(AccelStepper::DRIVER, CLOTHE_PUL, CLOTHE_DIR);
//////////////////////////////////////////////////////////////////
#define LFRONTIRON_PUL    43
#define LFRONTIRON_DIR    45
#define LFRONTIRON_ENA    47
#define OPTFRONT_SWITCH   10
#define LFRONTIRON_SPEED  750
#define LFRONTIRON_ACCEL  300

#define SUBE                1
#define BAJA              2
AccelStepper LFRONTIRON(AccelStepper::DRIVER, LFRONTIRON_PUL, LFRONTIRON_DIR);
//////////////////////////////////////////////////////////////////
#define RFRONTIRON_PUL    22
#define RFRONTIRON_DIR    23
#define RFRONTIRON_ENA    24
#define RFRONTIRON_SPEED  750
#define RFRONTIRON_ACCEL  300
AccelStepper RFRONTIRON(AccelStepper::DRIVER, RFRONTIRON_PUL, RFRONTIRON_DIR);
//////////////////////////////////////////////////////////////////
#define LBACKIRON_PUL     28
#define LBACKIRON_DIR     29
#define LBACKIRON_ENA     30
#define OPTBACK_SWITCH    9
#define LBACKIRON_SPEED   750
#define LBACKIRON_ACCEL   300
AccelStepper LBACKIRON(AccelStepper::DRIVER, LBACKIRON_PUL, LBACKIRON_DIR);
//////////////////////////////////////////////////////////////////
#define RBACKIRON_PUL    25
#define RBACKIRON_DIR    26
#define RBACKIRON_ENA    27
#define RBACKIRON_SPEED  750
#define RBACKIRON_ACCEL  300
AccelStepper RBACKIRON(AccelStepper::DRIVER, RBACKIRON_PUL, RBACKIRON_DIR);
////////////////////////////////////////////////////////////////
int fabric ; 
int bandera=0;
int counter=0;
int temp;
int tempstatus;

