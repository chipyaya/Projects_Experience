$parentPath=Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
echo "Present COM port:"
[System.IO.Ports.SerialPort]::getportnames()
echo ""
echo "Please connect Arduino Board and press Enter."
pause
[System.IO.Ports.SerialPort]::getportnames()
echo ""
$num=read-host "Please enter the port number of Arduino Board(only number)"

$port=new-Object System.IO.Ports.SerialPort COM$num,9600,None,8,one
echo "Press Alt+F4 to terminate.(with 5 sec. delay)"
$port.open()
while(1){ $port.ReadLine() | out-file -filepath $parentPath\heartBeat.txt}