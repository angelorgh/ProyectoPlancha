void homing(AccelStepper* motor, long targetPos, float motorSpeed, float motorAccel, uint8_t limitSwitch)
{
  motor->setMaxSpeed(motorSpeed);
  motor->setAcceleration(motorAccel);
  motor->moveTo(targetPos);

  while(digitalRead(limitSwitch)==0)

    motor->run();    

  motor->setCurrentPosition(0);
}

void doorhoming(AccelStepper* motor, long targetPos, float motorSpeed, float motorAccel, int limitSwitch)
{
  motor->setMaxSpeed(motorSpeed);
  motor->setAcceleration(motorAccel);
  motor->moveTo(targetPos);
  Serial.print(digitalRead(limitSwitch));
  Serial.print("llegue");
  while(targetPos != motor->currentPosition()) 

    motor->run();    
    

  motor->setCurrentPosition(0);
}

void doublehoming(AccelStepper* motor, long targetPos,float motorSpeed, float motorAccel, 
AccelStepper* motor1, long targetPos1,float motorSpeed1, float motorAccel1, uint8_t limitSwitch)
{
  motor->setMaxSpeed(motorSpeed);
  motor->setAcceleration(motorAccel);
  motor->moveTo(targetPos);

  motor1->setMaxSpeed(motorSpeed1);
  motor1->setAcceleration(motorAccel1);
  motor1->moveTo(targetPos1);

  while(digitalRead(limitSwitch) == 0)
    motor->run(); 
    motor1->run();

  motor->setCurrentPosition(0);
  motor1->setCurrentPosition(0);
}
void fakehoming(AccelStepper* motor,float motorSpeed, float motorAccel)
{
  motor->setMaxSpeed(motorSpeed);
  motor->setAcceleration(motorAccel);
  motor->setCurrentPosition(0);
}

void gohome()
{
digitalWrite(CLOTHE_ENA, false);
homing(&CLOTHE,90000, CLOTHE_SPEED, CLOTHE_ACCEL,CLOTHE_SWITCH);

CLOTHE.runToNewPosition(5000);
Serial.print("clothe");

 digitalWrite(RDOOR_ENA, false);
 homing(&RDOOR,5000, RDOOR_SPEED,RDOOR_ACCEL,MGTRDOOR_SWITCH);
 RDOOR.runToNewPosition(300);
 

 digitalWrite(LDOOR_ENA, false);
 homing(&LDOOR,-5000, LDOOR_SPEED, LDOOR_ACCEL,MGTLDOOR_SWITCH);
 LDOOR.runToNewPosition(-300);
 Serial.print("mmg");

 digitalWrite(LFRONTIRON_ENA,false);
 digitalWrite(RFRONTIRON_ENA,false);
 doublehoming(&LFRONTIRON,100,LFRONTIRON_SPEED, LFRONTIRON_ACCEL, &RFRONTIRON, -100,RFRONTIRON_SPEED,RFRONTIRON_ACCEL, OPTFRONT_SWITCH);

 digitalWrite(LBACKIRON_ENA,false);
 digitalWrite(RBACKIRON_ENA,false);
 doublehoming(&LBACKIRON,100,LBACKIRON_SPEED, LBACKIRON_ACCEL, &RBACKIRON,-100, RBACKIRON_SPEED,RBACKIRON_ACCEL, OPTBACK_SWITCH);

}

