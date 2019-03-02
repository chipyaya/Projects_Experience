@echo off
cls
echo.
echo Status for device COM8:
echo -----------------------
echo     Baud:            9600
echo     Parity:          None
echo     Data Bits:       8
echo     Stop Bits:       1
echo     Timeout:         ON
echo     XON/XOFF:        OFF
echo     CTS handshaking: OFF
echo     DSR handshaking: OFF
echo     DSR sensitivity: OFF
echo     DTR circuit:     OFF
echo     RTS circuit:     OFF
echo.
echo Press Ctrl+C to terminate.

set HB=0
echo %HB% >heartBeat.txt
set i=0
:START

::0bpm 10sec
millisleep 10000

::70bpm 10sec
set i=0
:L0
set /a "i+=1"
set /a "HB+=1"
echo %HB% >heartBeat.txt
millisleep 857
if %i% LSS 12 goto L0

::80bpm 20sec
set i=0
:L1
set /a "i+=1"
set /a "HB+=1"
echo %HB% >heartBeat.txt
millisleep 750
if %i% LSS 27 goto L1

::90bpm 10sec
set i=0
:L2
set /a "i+=1"
set /a "HB+=1"
echo %HB% >heartBeat.txt
millisleep 667
if %i% LSS 15 goto L2

::80bpm 20sec
set i=0
:L3
set /a "i+=1"
set /a "HB+=1"
echo %HB% >heartBeat.txt
millisleep 750
if %i% LSS 27 goto L3

::70bpm 10sec
set i=0
:L4
set /a "i+=1"
set /a "HB+=1"
echo %HB% >heartBeat.txt
millisleep 857
if %i% LSS 12 goto L4

::0bpm 20sec
millisleep 20000

::80bpm 80sec
set i=0
:L6
set /a "i+=1"
set /a "HB+=1"
echo %HB% >heartBeat.txt
millisleep 750
if %i% LSS 107 goto L6

goto START