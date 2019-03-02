#include <SimpleSDAudio.h>
void setup(){
  SdPlay.setSDCSPin(10);
  SdPlay.init(SSDA_MODE_FULLRATE | SSDA_MODE_STEREO | SSDA_MODE_AUTOWORKER);
}
void loop(){
  if(digitalRead(2)==HIGH){
    SdPlay.setFile("001.afs");//001=>魯, 003=>溫
    SdPlay.play();
    delay(2000);
  }
}
