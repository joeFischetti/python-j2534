# This is a j2534 interface library for Python

These scripts are for testing purposes ONLY at this time. Still waiting for my interface to actually confirm that I can communicate with it.

They assume an openport with a dll located in:
"C:/Program Files (x86)/OpenECU/OpenPort 2.0/drivers/openport 2.0/"

And they only work with a 32bit python version right now. 

Most of what I'm going to attempt is a translation of the tactrix cpp sample code.  I.e. a python wrapper to the J2534 dll.

j2534.py is the main library file

tactrix.py is a few enum's used for response codes etc

test.py is a harness to imports the library and the makes calls to:
open the interface
connect to the interface
send arbitrary data
read something back
disconnect from the interface
close the interface


