#include <SD.h>
#include <Ethernet.h>
#include <Wire.h>
int output[5] ;
float resultT[5][5] = {{0}};
int ans = 0;
File myFile;

byte mac[] = {  
  0x98, 0x4F, 0xEE, 0x01, 0x9D, 0xEA };

void setup()
{
  Serial.begin(9600);
  delay(3000);

//SD
  sd_init();

//internet
  internet_init();

//wire
  Wire.begin(); // join i2c bus (address optional for master)
  
}


void loop() {
  Wire.beginTransmission(4); // transmit to device #4
  
  SD.remove("result.txt");

  //ping and store in result.txt
  ping2file();
  
  //read result and store in resultT[][]
  read_file(); 
  
  //cat
  system("cat /media/mmcblk0p1/result.txt  > /dev/ttyGS0");
  
  //calculate and store in outpu[]
  map2led();   
  
  for(int i = 0; i < 5; i++){
    Wire.write(output[i]);              // sends one byte 
  }
  delay(200); 
  Wire.endTransmission();    // stop transmitting

}

void sd_init(){
  Serial.print("Initializing SD card...");
  pinMode(10, OUTPUT);
   
  if (!SD.begin(4)) {
    Serial.println("initialization failed!");
    return;
  }
  Serial.println("initialization done.");
}

void internet_init(){
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
 
}

void ping2file(){
  system("ping -c 3 140.112.30.32 | awk 'NR>=2 && NR<=6 {print $7}' | cut -d '=' -f2  >> /media/mmcblk0p1/result.txt"); 
  system("ping -c 3 140.112.30.35 | awk 'NR>=2 && NR<=6 {print $7}' | cut -d '=' -f2  >> /media/mmcblk0p1/result.txt"); 
  system("ping -c 3 140.112.30.38 | awk 'NR>=2 && NR<=6 {print $7}' | cut -d '=' -f2  >> /media/mmcblk0p1/result.txt"); 
  system("ping -c 3 140.112.30.41 | awk 'NR>=2 && NR<=6 {print $7}' | cut -d '=' -f2  >> /media/mmcblk0p1/result.txt"); 
  system("ping -c 3 140.112.30.44 | awk 'NR>=2 && NR<=6 {print $7}' | cut -d '=' -f2  >> /media/mmcblk0p1/result.txt"); 
}

void read_file(){
 int i = 0, j = 0;    
  myFile = SD.open("result.txt");
  if (myFile) {
    Serial.println("result.txt:");
    // read from the file until there's nothing else in it:
    while (myFile.available()) {    //do we need this line?
        if(i == 5)  //big
            break;
        resultT[i][j] = myFile.parseFloat();
        j++;
        if(j == 3){  //small
          i++;
          j = 0;
        }  
    }
    // close the file:
    myFile.close();
  } else {
    // if the file didn't open, print an error:
    Serial.println("error opening result.txt");
  }
 
}

void map2led(){
    for(int i=0 ; i<5 ; i++){
	  double sum = 0 ;
	  for(int j=1 ; j<3 ; j++){
		  sum = sum + resultT[i][j] * resultT[i][j] ;
	  }
	 int temp = 9 - int((sqrt(sum*2)-3.8) * 4 + 6) ;
	 if(temp > 8)	temp =  8 ;
	 else if(temp < 1)	temp = 1 ;
         output[i] = temp ;
         Serial.println(output[i]) ;
    }
}
