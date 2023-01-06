int num = 0;
void setup() {
 	Serial.begin(115200);
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
  num = 0;
  while(!Serial.available());
  num = Serial.parseInt();  
}

void sendData(int val1) {
 	//write data
 	Serial.print(val1);
  Serial.print('\n');
}

void simulate(){
  bool timer = false;
  int num = 0;
  while(timer = false){
    sendData("temp " + random(50, 100));
    num++;
    if(num >= 14000){
      timer = true;
    }
  }
}