String msg = "";
void setup() {
 	Serial.begin(9600);
 
}
void loop() {
  readSerialPort();
  int num = msg.toInt();
  if (num == 200) {
    sendData("332,163,283,602,1533,1955,89");
    // exit(0);
  }
  if(num == 1){
    sendData(msg);
    exit(0);
  }
  // delay(10);
}
void readSerialPort() {
  msg = "";
  while (Serial.available() > 0) {
    msg = Serial.readString();
  }
  
  Serial.flush();
}



void sendData(String val1) {
 	//write data
 	Serial.print(val1 + "\n");
   delay(500);
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