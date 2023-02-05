int num = 0;
void setup() {
   Serial.begin(115200);
  while (!Serial);
  pinMode(8, OUTPUT);
}
void loop() {
  readSerialPort();
  if(num != 0){
    digitalWrite(8, HIGH);
    sendData(num);
  }
}
void readSerialPort() {
  //num = 0;
  while(!Serial.available());
  num = Serial.parseInt();  
}

void sendData(int val1) {
  //write data
  Serial.print(val1);
  Serial.print('\n');
}