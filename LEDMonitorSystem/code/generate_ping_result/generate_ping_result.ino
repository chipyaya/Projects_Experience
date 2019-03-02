#include <SD.h>
#include <Ethernet.h>

File myFile;
byte mac[] = {  
  0x98, 0x4F, 0xEE, 0x01, 0x9D, 0xEA };

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


//internet
  system("ifdown eth0");
  system("ifup eth0");

  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    // no point in carrying on, so do nothing forevermore:
  }
  Serial.print("My IP address: ");
  for (byte thisByte = 0; thisByte < 4; thisByte++) {
    // print the value of each byte of the IP address:
    Serial.print(Ethernet.localIP()[thisByte], DEC);
    Serial.print("."); 
  }
  Serial.println();
  
  system("rm  -f /media/mmcblk0p1/result.txt ");
  system("ls /media/mmcblk0p1 > /dev/ttyGS0");
  system("ping -c 5 8.8.8.8 | awk 'NR>=2 && NR<=6 {print $7}' | cut -d '=' -f2  > /media/mmcblk0p1/result.txt"); 
  system("cat /media/mmcblk0p1/result.txt  > /dev/ttyGS0");
  
}

void loop()
{
  // nothing happens after setup
}
