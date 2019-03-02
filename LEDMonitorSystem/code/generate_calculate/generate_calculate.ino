#include <SD.h>
File myFile;

void setup()
{
 // Open serial communications and wait for port to open:
  Serial.begin(9600);
  
  delay(3000);

  Serial.print("Initializing SD card...");
  // On the Ethernet Shield, CS is pin 4. It's set as an output by default.
  // Note that even if it's not used as the CS pin, the hardware SS pin 
  // (10 on most Arduino boards, 53 on the Mega) must be left as an output 
  // or the SD library functions will not work. 
   pinMode(10, OUTPUT);
   
  if (!SD.begin(4)) {
    Serial.println("initialization failed!");
    return;
  }
  Serial.println("initialization done.");
  
  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.

  //remove calculate.sh before writing
  //Success? unknown
  system("rm -f media/mmcblk0p1/calculate.sh");
  
  //Writing
  myFile = SD.open("calculate.sh", FILE_WRITE);
  
  // if the file opened okay, write to it:
  if (myFile) {
    Serial.print("Writing to calculate.sh...");
    myFile.println("sum=0");
    myFile.println("for i in 1 2 3 4 5");
    myFile.println("do");
    myFile.println("        read time");
    myFile.println("        sum=$(($sum+$time))");
    myFile.println("done");
    myFile.println("echo $(($sum/5))");

    // close the file:
    myFile.close();
    Serial.println("done.");
  } else {
    // if the file didn't open, print an error:
    Serial.println("error opening calculate.sh");
  }
  
  system("cat /media/mmcblk0p1/calculate.sh > /dev/ttyGS0");
 
}

void loop()
{
  // nothing happens after setup
}
