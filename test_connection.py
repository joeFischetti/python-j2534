from connections import J2534Connection
import logging
import time

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)
f_handler = logging.StreamHandler()
logger.addHandler(f_handler)


conn = J2534Connection(windll='C:/Program Files (x86)/OpenECU/OpenPort 2.0/drivers/openport 2.0/op20pt32.dll', rxid=0x7E8, txid=0x7E0)
conn.open()

data = [b'\x10\x03',b'\x22\xf1\x89',b'\x01\x06', b'\x22\xf1\x91',b'\x01\x0c',b'\x01\x04',b'\x01\x05']


for param in data:
    logger.debug("Requesting: " + str(param.hex()))
    conn.send(param)
    response = None
    #while response is None:
    response = conn.wait_frame()
    if response:
        print("Response: " + str(response.hex()))


conn.close()

