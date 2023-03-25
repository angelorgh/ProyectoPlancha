#include "Define.h"
#include "Home.h"
#include "Encoder.h"
#include "Run.h"
//////////////////////////////////////////////////////////////////
void setup()
{
  Serial.begin(9600);
/////////////////////////////////////////////////
  mlx.begin();
/////////////////////////////////////////////////
  pinMode(ENA1A, INPUT_PULLUP);
  pinMode(ENA1B, INPUT_PULLUP);

  pinMode(ENA2A, INPUT_PULLUP);
  pinMode(ENA2B, INPUT_PULLUP);

  //attachInterrupt(digitalPinToInterrupt(ENA1A), risingena1a ,RISING);
  //attachInterrupt(digitalPinToInterrupt(ENA1B), risingena1b ,RISING);

  //attachInterrupt(digitalPinToInterrupt(ENA2A), risingena2a ,RISING);
 // attachInterrupt(digitalPinToInterrupt(ENA2B), risingena2b ,RISING);
////////////////,////////////////////////////////
  pinMode(RDOOR_ENA, OUTPUT);
  pinMode(MGTRDOOR_SWITCH , INPUT_PULLUP);

  pinMode(LDOOR_ENA, OUTPUT);
  pinMode(MGTLDOOR_SWITCH , INPUT_PULLUP);

  pinMode(CLOTHE_ENA, OUTPUT);
  pinMode(CLOTHE_SWITCH , INPUT);

  pinMode(LFRONTIRON_ENA, OUTPUT);
  pinMode(RFRONTIRON_ENA, OUTPUT);
  pinMode(OPTFRONT_SWITCH , INPUT);

  pinMode(LBACKIRON_ENA, OUTPUT);
  pinMode(RBACKIRON_ENA, OUTPUT);
  pinMode(OPTBACK_SWITCH,INPUT);
//////////////////////////////////////////////
   gohome();

}

void loop()
{

//run(&LDOOR,-4000,LDOOR_SPEED, LDOOR_ACCEL,2,MGTLDOOR_SWITCH);
//run(&RDOOR, 4000,RDOOR_SPEED, RDOOR_ACCEL,2,MGTRDOOR_SWITCH);
//doublerun(&LFRONTIRON,-5000,&RFRONTIRON,5000,RFRONTIRON_SPEED,RFRONTIRON_ACCEL); 
//doublerun(&LFRONTIRON,5000, &RFRONTIRON,-5000,RFRONTIRON_SPEED,RFRONTIRON_ACCEL,2,OPTFRONT_SWITCH);
//doublerun(&LBACKIRON,-100, &RBACKIRON,100,RBACKIRON_SPEED,RBACKIRON_ACCEL,2,OPTBACK_SWITCH);


 switch (status) 
 {
    temp = mlx.readObjectTempC() ;
    case 0:
    {
      if (flag==0)
      {
      Serial.print("Waitingstart");
      flag=1;
      }

      break;
    }
    case 1:
    {
      run(&LDOOR, 4500,LDOOR_SPEED, LDOOR_ACCEL,ABRE,MGTLDOOR_SWITCH);  
      run(&RDOOR, -4500,RDOOR_SPEED, RDOOR_ACCEL,ABRE,MGTRDOOR_SWITCH);

      doublerun(&LFRONTIRON,-5000, &RFRONTIRON,5000,RFRONTIRON_SPEED,RFRONTIRON_ACCEL,SUBE,OPTFRONT_SWITCH);   // SUBE LA PLANCHA A POSICION DE TOMAR MEDIDA 

      if (RFRONTIRON.currentPosition() == RFRONTIRON.targetPosition() || LDOOR.currentPosition() == LDOOR.targetPosition()  )
      {
        if (flag==0)
        {
        Serial.print("Waitingfabric");
        flag=1;
        }
      }
      break;
    }

    case 2:
    {
      doublerun(&LFRONTIRON,0, &RFRONTIRON,0,RFRONTIRON_SPEED,RFRONTIRON_ACCEL,BAJA,OPTFRONT_SWITCH);  

      if (RFRONTIRON.currentPosition() == RFRONTIRON.targetPosition() || digitalRead(OPTFRONT_SWITCH)==1)
      {
        status=3;
      }
      break;
    }
  
  case 3:
    {
      run(&CLOTHE,-45000,CLOTHE_SPEED,CLOTHE_ACCEL,ABRE,CLOTHE_SWITCH);
      if (CLOTHE.currentPosition() == CLOTHE.targetPosition())
      {
        status=4;
      }
      break;
    }
    case 4:
    {
        //run(&LDOOR,-4500,LDOOR_SPEED, LDOOR_ACCEL,CIERRA,MGTLDOOR_SWITCH);  
        //run(&RDOOR, 4500,RDOOR_SPEED, RDOOR_ACCEL,CIERRA,MGTRDOOR_SWITCH);  
        //if (LDOOR.currentPosition() == LDOOR.targetPosition())
       // {
        status=5;  
        //Serial.print("Planchando");
        //}  
      break;
  }
    case 5:
    {
       planchando(2);

      break;
    }
     case 6:
    {
      //doublerun(&LDOOR,3750,&RDOOR,-4000,RDOOR_SPEED,RDOOR_ACCEL);    
      //if (LDOOR.currentPosition() == LDOOR.targetPosition()  )
      //{
        status=7;
      //}
      break;
    }
      case 7:
    {
      run(&CLOTHE,-85000,CLOTHE_SPEED,CLOTHE_ACCEL,ABRE,CLOTHE_SWITCH);
      if (CLOTHE.currentPosition() == CLOTHE.targetPosition())
      {
        status=8;
      }
      break;
    }
     case 8:
    {
      run(&CLOTHE,85000,CLOTHE_SPEED,CLOTHE_ACCEL,CIERRA,CLOTHE_SWITCH);
      if (LDOOR.currentPosition() == LDOOR.targetPosition()  )
      {
        status=0;
      }
      break;
    }
     case 20:
    {
      if (flag==0)
      {
      Serial.print("Waitingstart");
      flag=1;
      }
      break;
    }
   
 }
 }
 
void serialEvent()
{
    if (status == 0) 
      {
        status = Serial.parseInt();     /// WAIT FOR THE START STATUS
      }
    if (status == 1) 
      {
        fabric = Serial.parseInt();     /// fabric type 
        if (fabric != 0)
        {
          status=2;
        }
      }
      if (status == 20) 
      {
        status = Serial.parseInt();
        status = tempstatus;     /// WAIT FOR THE START STATUS
      }
}