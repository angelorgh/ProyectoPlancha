void run(AccelStepper* motor,long targetPos, float motorSpeed, float motorAccel, int dir, uint8_t limitSwitch)
{
  motor->setMaxSpeed(motorSpeed);
  motor->setAcceleration(motorAccel);
  motor->moveTo(targetPos);
  
  if (dir==1)
  {
    if(targetPos != motor->currentPosition() )
    {
      motor->run();
    }
  }
  if (dir==2)
  {
    if(targetPos != motor->currentPosition() && digitalRead(limitSwitch)==0)
    {
      motor->run();
    }
  }
    
}

void doublerun(AccelStepper* motor,long targetPos, AccelStepper* motor1,long targetPos1, float motorSpeed, float motorAccel, int dir,uint8_t limitSwitch)
{
  motor->setMaxSpeed(motorSpeed);
  motor->setAcceleration(motorAccel);
  motor->moveTo(targetPos);

  motor1->setMaxSpeed(motorSpeed);
  motor1->setAcceleration(motorAccel);
  motor1->moveTo(targetPos1);

if (dir==1)
{
  if(targetPos != motor->currentPosition())
  {
    motor->run();
  }
 if(targetPos1 != motor1->currentPosition())
  {
    motor1->run();
  }
}

if (dir==2)
{
  if(targetPos != motor->currentPosition() && digitalRead(limitSwitch)==0)
  {
    motor->run();
  }
 if(targetPos1 != motor1->currentPosition() && digitalRead(limitSwitch)==0)
  {
    motor1->run();
  }
}
}
void planchando(int pasadas) //fabric be a even number so based on a calculation determine 
{
      if (bandera==0)
      {
      doublerun(&LFRONTIRON,-10000, &RFRONTIRON,10000,RFRONTIRON_SPEED,RFRONTIRON_ACCEL,SUBE,OPTFRONT_SWITCH); 
      doublerun(&LBACKIRON,10000,&RBACKIRON,-10000,RBACKIRON_SPEED,RBACKIRON_ACCEL,SUBE,OPTBACK_SWITCH);
       if (LFRONTIRON.currentPosition() == LFRONTIRON.targetPosition())
        {
          bandera=1;  
        }  
      }

       if (bandera==1)
      {
      doublerun(&LFRONTIRON,0, &RFRONTIRON,0,RFRONTIRON_SPEED,RFRONTIRON_ACCEL,SUBE,OPTFRONT_SWITCH); 
      doublerun(&LBACKIRON,0,&RBACKIRON,0,RBACKIRON_SPEED,RBACKIRON_ACCEL,SUBE,OPTBACK_SWITCH);
      
      if (LFRONTIRON.currentPosition() == LFRONTIRON.targetPosition() || (digitalRead(OPTFRONT_SWITCH)==1 || digitalRead(OPTBACK_SWITCH)==1))
        {
          bandera=0; 
          counter=counter+1;

           if (counter==pasadas) 
          {
            bandera=0;
            counter=0;
            status=6;
          }
          
        } 
      }
}

