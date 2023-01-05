String nom = "Arduino";
String msg = "";
void setup() {
 	Serial.begin(9600);
}
void loop() {
 	readSerialPort();
 	if (msg == "Start") {
    sendData("332,163,283,602,1533,1955,89");
    simulate();
 	}
 	delay(500);
}
void readSerialPort() {
 	msg = "";
 	if (Serial.available()) {
    delay(10);
    while (Serial.available() > 0) {
        msg += (char)Serial.read();
    }
    Serial.flush();
 	}
}
void sendData(String msg) {
 	//write data
 	Serial.print(msg + "\n");
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