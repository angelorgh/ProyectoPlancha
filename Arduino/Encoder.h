void risingena1a()
{
    // Esta interrupcion se activa si hay un flanco de subida en el cable blanco del encoder
    if(digitalRead(ENA1A)==LOW)
    {
        EncoderENA1++;
    }
    else
    {
        EncoderENA1--;
    }
}
   
void risingena1b()
{
    // Esta interrupcion se activa si hay un flanco de subida en el cable verde del encoder
    if(digitalRead(ENA1B)==LOW)
    {
        EncoderENA1--;
    }
    else
    {
        EncoderENA1++;
    }
}
void risingena2a()
{
    // Esta interrupion se activa si hay un flanco de subida en el cable blanco del encoder
    if(digitalRead(ENA2A)==LOW)
    {
        EncoderENA2++;
    }
    else
    {
        EncoderENA2--;
    }
}
   
void risingena2b()
{
    // Esta interrupcion se activa si hay un flanco de subida en el cable verde del encoder
    if(digitalRead(ENA2B)==LOW)
    {
        EncoderENA2--;
    }
    else
    {
        EncoderENA2++;
    }
}

void missingsteps(AccelStepper* motor, int encodersteps,int dir)
{
  if (motor->currentPosition() +100*dir < encodersteps)
  {
    tempstatus=status;
    status=20;
  }

}
