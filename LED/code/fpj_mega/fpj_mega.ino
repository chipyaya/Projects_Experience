#include <Wire.h>
int ans[5] = {0};
void setup()
{
  //led
  for(int i = 2; i <= 22; i++){
    pinMode(i, OUTPUT);
  }
  for(int i = 30; i <= 53; i++){
    pinMode(i, OUTPUT);
  }
  
  //wire
  Wire.begin(4);                // join i2c bus with address #4
  delay(2000);
  Serial.println("Initial");
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output

}

void loop(){
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany){
    Serial.println("Begin");
    for(int i = 0; i < 5; i++){
      ans[i] = Wire.read();
      Serial.println(ans[i]);  
    }
  
    for(int j = 0; j < 2; j++){
      if(ans[j] <= 0 || ans[j] >= 9){
          Serial.println("ans wrong!!");
          return;
      }
      for(int i = 0; i < ans[j]; i++){
        if((2+8*j+i) == 13){
          Serial.println("haha");
          digitalWrite(22, HIGH);
        }
        else{     
          digitalWrite(2+8*j+i, HIGH);
        }
      }
      for(int i = ans[j]; i < 9; i++){
         if((2+8*j+i) == 13){
             digitalWrite(22, LOW);
         }
         else{    
           digitalWrite(2+8*j+i, LOW);
         }
      }     
      delay(10000);
    }
    
   for(int j = 2; j < 5; j++){
     if(ans[j] <= 0 || ans[j] >= 9){
          Serial.println("ans wrong!!");
          return;
      }
      for(int i = 0; i < ans[j]; i++){
         digitalWrite(30+8*(j-2)+i, HIGH);
      }
      for(int i = ans[j]; i < 9; i++){
          digitalWrite(30+8*(j-2)+i, LOW);
      }     
      delay(10000);
   }     
  
}
