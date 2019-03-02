//model=arduino nano 328
#include <EEPROM.h>
//pin definition
#define LDR A2             //environment
#define LDR0 A0            //photoresister(light-dependent resistor)
#define AUDIO0 2
#define SERVO0 3
#define LASER0 4
#define LDR1 A1            //photoresister(light-dependent resistor)
#define AUDIO1 5
#define SERVO1 6
#define LASER1 7
#define BEAM 11

//record
int loserCount=0;
int winnerCount=0;

//LDR
float ldrTemp=0;          //temporarily store old data
float ldrValue0=0;        //sensed value
float ldrChange0=0;       //delta
unsigned long ldrTime0=0; //end time of scanning in ms.
bool ldrStatus0=0;        //1 for reacting
float ldrValue1=0;        //sensed value
float ldrChange1=0;       //delta
unsigned long ldrTime1=0; //end time of scanning in ms.
bool ldrStatus1=0;        //1 for reacting

//servo
const int UPPER=4000;     //upper limit of OCR1
const int LOWER=2200;     //lower limit of OCR1
const int STEP_INC0=12;   //increasing step of OCR1A
const int STEP_DEC0=-100; //decreasing step of OCR1A
const int STEP_INC1=100;  //increasing step of OCR1B
const int STEP_DEC1=-12;  //decreasing step of OCR1B
volatile int ocr1a_step=0;//step of OCR1A
volatile int ocr1b_step=0;//step of OCR1B

void setup(){
  digitalWrite(AUDIO0,LOW);
  digitalWrite(SERVO0,LOW);
  digitalWrite(LASER0,LOW);
  digitalWrite(AUDIO1,LOW);
  digitalWrite(SERVO1,LOW);
  digitalWrite(LASER1,LOW);
  analogWrite(BEAM,128);
  
  pinMode(AUDIO0,OUTPUT);
  pinMode(SERVO0,OUTPUT);
  pinMode(LASER0,OUTPUT);
  pinMode(AUDIO1,OUTPUT);
  pinMode(SERVO1,OUTPUT);
  pinMode(LASER1,OUTPUT);
  pinMode(BEAM,OUTPUT);
  
  loserCount=EEPROM.read(1)*256+EEPROM.read(0);
  winnerCount=EEPROM.read(3)*256+EEPROM.read(2);
  sendRatio();
  
  //timer1
  TCCR1A=0;                       //Reset Timer1 Control Register A
  TCCR1B=_BV(CS11);               //Timer1 Prescaler=8, 30.51Hz
  OCR1A=LOWER;                    //Output Compare Register A
  OCR1B=UPPER;                    //Output Compare Register B
  TIMSK1=_BV(OCIE1A)+_BV(OCIE1B)+_BV(TOIE1);//Enable Timer1 Output Compare Match A,B Interrupt and Overflow Interrupt
  
  Serial.begin(9600);
  sendRatio();
}
void loop(){
  //night
  if(analogRead(LDR)<800){
    //sense
    ldrTemp=ldrValue0;
    ldrValue0=analogRead(LDR0);
    ldrChange0=ldrValue0-ldrTemp;
    //scan
    if(ldrStatus0){
      if(millis()>ldrTime0){
        ldrStatus0=0;
        stopScan0();
      }
    }
    else{
      if(ldrChange0>20){
        ldrTime0=millis()+3000;
        ldrStatus0=1;
        startScan0();
        ++loserCount;
        storeLoser();
        sendRatio();
      }
    }
    ldrTemp=ldrValue1;
    ldrValue1=analogRead(LDR1);
    ldrChange1=ldrValue1-ldrTemp;
    if(ldrStatus1){
      if(millis()>ldrTime1){
        ldrStatus1=0;
        stopScan1();
      }
    }
    else{
      if(ldrChange1>20){
        ldrTime1=millis()+3000;
        ldrStatus1=1;
        startScan1();
        ++winnerCount;
        storeWinner();
        sendRatio();
      }
    }
    delay(5);
  }
  //daylight
  else{
    startScan0();
    delay(3000);
    stopScan0();
    delay(1000);
    startScan1();
    delay(3000);
    stopScan1();
    delay(1000);
  }
}

void storeLoser(){
  EEPROM.write(0,loserCount%256);
  EEPROM.write(1,loserCount/256);
}

void storeWinner(){
  EEPROM.write(2,winnerCount%256);
  EEPROM.write(3,winnerCount/256);
}

void sendRatio(){
  Serial.println((long)100*winnerCount/(loserCount+winnerCount));
}

void startScan0(){
  digitalWrite(AUDIO0,HIGH);
  TCCR1B=0;                       //pause Timer1
  ocr1a_step=STEP_INC0;            //start scanning
  TCCR1B=_BV(CS11);               //resume Timer1
  digitalWrite(LASER0,HIGH);
  digitalWrite(AUDIO0,LOW);
}

void stopScan0(){
  digitalWrite(LASER0,LOW);
  TCCR1B=0;                       //pause Timer1
  ocr1a_step=0;                   //stop scanning
  OCR1A=LOWER;                    //place servo at LOWER position
  TCCR1B=_BV(CS11);               //resume Timer1
}

void startScan1(){
  digitalWrite(AUDIO1,HIGH);
  TCCR1B=0;                       //pause Timer1
  ocr1b_step=STEP_DEC1;           //start scanning
  TCCR1B=_BV(CS11);               //resume Timer1
  digitalWrite(LASER1,HIGH);
  digitalWrite(AUDIO1,LOW);
}

void stopScan1(){
  digitalWrite(LASER1,LOW);
  TCCR1B=0;                       //pause Timer1
  ocr1b_step=0;                   //stop scanning
  OCR1B=UPPER;                    //place servo at UPPER position
  TCCR1B=_BV(CS11);               //resume Timer1
}

ISR(TIMER1_OVF_vect){             //ISR for timer1 overflow
  digitalWrite(SERVO0,HIGH);
  digitalWrite(SERVO1,HIGH);
  OCR1A+=ocr1a_step;              //modify duty cycle
  OCR1B+=ocr1b_step;              //modify duty cycle
  if(OCR1A>UPPER){                //limit detection
    OCR1A=UPPER;
    ocr1a_step=STEP_DEC0;
    digitalWrite(LASER0,LOW);
  }
  if(OCR1A<LOWER){
    OCR1A=LOWER;
    ocr1a_step=STEP_INC0;
    digitalWrite(LASER0,HIGH);
  }
  if(OCR1B>UPPER){
    OCR1B=UPPER;
    ocr1b_step=STEP_DEC1;
    digitalWrite(LASER1,HIGH);
  }
  if(OCR1B<LOWER){
    OCR1B=LOWER;
    ocr1b_step=STEP_INC1;
    digitalWrite(LASER1,LOW);
  }
}

ISR(TIMER1_COMPA_vect){           //ISR for timer1 compare match A
  digitalWrite(SERVO0,LOW);
}

ISR(TIMER1_COMPB_vect){           //ISR for timer1 compare match B
  digitalWrite(SERVO1,LOW);
}
