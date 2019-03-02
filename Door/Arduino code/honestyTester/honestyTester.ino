//model=arduino nano
//pin definition
#define TCRT5000 A0       //sensor output
#define HB A1             //filtered output
#define SERVO 2
#define LASER 3
#define BREATHE 11

//servo
const int UPPER=3000;     //upper limit of OCR1A
const int LOWER=2200;     //lower limit of OCR1A
const int STEP_INC=10;    //increasing step of OCR1A
const int STEP_DEC=-200;  //decreasing step of OCR1A
volatile int ocr1a_step=0;  //step of OCR1A

//heart beat
const float RATIO=0.25;   //ratio of change of value in smoothing
const float THR=30;       //threshold
float value=1023;         //value of input(smoothed)
float change=0;           //change of value
unsigned long hbTime=0;   //time of last trigger in milliseconds
unsigned long HBCount=0;  //heart beat count

//breathe
long bthInd=0;            //breathe index
char bthDir=1;            //breathe direction
unsigned long bthTime=0;  //time of starting holding bthInd in milliseconds

void setup(){
  Serial.begin(9600);
  pinMode(SERVO,OUTPUT);
  digitalWrite(LASER,LOW);
  pinMode(LASER,OUTPUT);
  TCCR1A=0;                       //Reset Timer1 Control Register A
  TCCR1B=_BV(CS11);               //Timer1 Prescaler=8, 30.51Hz
  OCR1A=LOWER;                    //Output Compare Register A
  TIMSK1=_BV(OCIE1A)+_BV(TOIE1);  //Enable Timer1 Output Compare Match A Interrupt and Overflow Interrupt
}

void loop(){
  //wait for trigger
  while(analogRead(TCRT5000)<180);
  
  //start scanning
  TCCR1B=0;                       //pause Timer1
  ocr1a_step=STEP_INC;            //start scanning
  TCCR1B=_BV(CS11);               //resume Timer1
  digitalWrite(LASER,HIGH);
  
  //heart beat & breathing light
  value=analogRead(HB);
  while(analogRead(TCRT5000)>180){
    change=RATIO*(analogRead(HB)-value);
    value+=change;
    //Serial.println(change);     //for adjustment
    if(millis()-hbTime>300)if(change>THR){
      hbTime=millis();
      Serial.println(++HBCount);
    }
    
    //breathing light
    if(bthInd>0 && bthInd<255){
      analogWrite(BREATHE,(383-bthInd)*bthInd*bthInd/32513);
      bthInd+=bthDir;
    }
    else if(bthInd==255){
      analogWrite(BREATHE,255);
      bthTime=millis();
      bthInd=256;
    }
    else if(bthInd==256 && millis()-bthTime>500){
      bthInd=254;
      bthDir=-1;
    }
    else if(bthInd==0){
      analogWrite(BREATHE,0);
      bthTime=millis();
      bthInd=-1;
    }
    else if(bthInd==-1 && millis()-bthTime>500){
      bthInd=1;
      bthDir=1;
    }
    delay(3);
  }
  
  //stop scanning
  digitalWrite(LASER,LOW);
  analogWrite(BREATHE,LOW);
  TCCR1B=0;                       //pause Timer1
  ocr1a_step=0;                   //stop scanning
  OCR1A=LOWER;                    //place servo at LOWER position
  TCCR1B=_BV(CS11);               //resume Timer1
}

ISR(TIMER1_OVF_vect){             //ISR for timer1 overflow
  digitalWrite(SERVO,HIGH);
  OCR1A+=ocr1a_step;              //modify duty cycle
  if(OCR1A>UPPER){                //limit detection
    OCR1A=UPPER;
    ocr1a_step=STEP_DEC;
    digitalWrite(LASER,LOW);
  }
  if(OCR1A<LOWER){
    OCR1A=LOWER;
    ocr1a_step=STEP_INC;
    digitalWrite(LASER,HIGH);
  }
}

ISR(TIMER1_COMPA_vect){           //ISR for timer1 compare match A
  digitalWrite(SERVO,LOW);
}
