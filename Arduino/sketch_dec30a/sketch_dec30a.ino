int num = 0;
void setup() {
 	Serial.begin(9600);
  pinMode(8, OUTPUT);
}
void loop() {
  readSerialPort();
  
  // int num = msg.toInt();
  // if (num == 200) {
  //   sendData("332,163,283,602,1533,1955,89");
  //   digitalWrite(8, HIGH);
  //   // exit(0);
  // }
  // int result = strcmp(msg, "");
  
  if(num != 0){
    digitalWrite(8, HIGH);
    sendData(num);
  }
  // if(num == 1){
  //   sendData(msg);
  //   exit(0);
  // }

  // delay(10);
}
void readSerialPort() {
  num = 0;
  while(!Serial.available());
  num = Serial.parseInt();  
}



void sendData(int val1) {
 	//write data
 	Serial.print(val1);
  Serial.print("\n");
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