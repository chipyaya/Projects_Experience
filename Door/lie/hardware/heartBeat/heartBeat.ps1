$parentPath=Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$port=new-Object System.IO.Ports.SerialPort COM5,9600,None,8,one
$port.open()
while(1){ $port.ReadLine() | out-file -encoding utf8 -filepath $parentPath\heartBeat.txt}
