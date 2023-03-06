int num = 0;
//Include libraries
#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is plugged into pin 2 on the Arduino
#define ONE_WIRE_BUS 2
// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);
// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

void setup() {
   Serial.begin(115200);
  while (!Serial);
  pinMode(8, OUTPUT);
  sensors.begin();
}
void loop() {
  readSerialPort();
  delay(1000);
  if(num == 100){
    Serial.println("332,163,283,602,1533,1955,89");
  }
  if(num == 200){
    digitalWrite(8, HIGH);
    sendData(num);
    // while(num !=300){
    //   readSerialPort();
    //   if(num ==0){
    //     num = 200;
    //   }
    //   digitalWrite(8, HIGH);
    //   sendData(num);
    // }
    
  }
  if(num == 300){
    digitalWrite(8, LOW);
    Serial.println(355);
  }
  
}
void readSerialPort() {
  //num = 0;
  
  while(!Serial.available());
  num = Serial.parseInt();  
}

void sendData(int val) {
  //Serial.println(val);
  sensors.requestTemperatures();  
  Serial.println(sensors.getTempCByIndex(0)); // Why "byIndex"? You can have more than one IC on the same bus. 0 refers to the first IC on the wire
  //Update value every 1 sec.
  delay(1000);
  //write data
}