# This is a j2534 interface library for Python

These scripts are for testing purposes ONLY at this time. 

They assume an openport with a dll located in:
"C:/Program Files (x86)/OpenECU/OpenPort 2.0/drivers/openport 2.0/"


And they only work with a 32bit python version right now. 


Most of what I'm going to attempt is a translation of the tactrix cpp sample code.  I.e. a python wrapper to the J2534 dll.


j2534.py is the main library file


tactrix.py is a few enum's used for response codes etc (though the relevant ones were pulled into j2534 for portability)


test.py is a harness to imports the library and the makes calls to:

*open the interface
*connect to the interface
*send arbitrary data
*read something back
*disconnect from the interface
*close the interface

PassThruReadMsgs *does* loop through the rxQueue in the interface and read 1 message at a time.  it only returns messages with valid rxStatus codes.  The idea behind this is that there would be a queue in python running in a thread that can read back data continuously.  It returns None on an empty buffer so the application needs to handle that accordingly.

Example output (used against an emulator):

```bash
Opening Pass through device
    ERR_SUCCESS

Getting device information
    ERR_SUCCESS
    firmware: b'1.00.0003'
    dllVersion: b'1.00.0003 (DEBUG) June 3 2013 15:02:00'
    apiVersion: b'04.04'

Connecting to pass through device
    ERR_SUCCESS

Setting up a flow contorl filter for ISO15765
    ERR_SUCCESS

Clearing the rxBuffer
    ERR_SUCCESS

Sending bytes to switch to extended diag: 1003
    Transmit: ERR_SUCCESS
    Receive: ERR_SUCCESS, Num Messages: 1
    Response: 500303234567

Sending bytes to read vin (0x22 f1 90): 22f190
    Transmit: ERR_SUCCESS
    Receive: ERR_SUCCESS, Num Messages: 1
    Response: 486b10c10890

Sending bytes to read ECU Hardware Number (0x22 f1 91): 22f191
    Transmit: ERR_SUCCESS
    Receive: ERR_SUCCESS, Num Messages: 1
    Response: 486b10c10891

Sending bytes to read ASW Version number (0x22 f1 89): 22f189
    Transmit: ERR_SUCCESS
    Receive: ERR_SUCCESS, Num Messages: 1
    Response: 486b10c10889

Disconnecting from pass through device
    ERR_SUCCESS

Closing Pass through device
    ERR_SUCCESS
```
