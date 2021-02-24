from connections import J2534Connection
import logging

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)
f_handler = logging.StreamHandler()
logger.addHandler(f_handler)


conn = J2534Connection(windll='C:/Program Files (x86)/OpenECU/OpenPort 2.0/drivers/openport 2.0/op20pt32.dll', rxid=0x7E8, txid=0x7eE)
conn.open()

data = [b'\x10\x03',b'\x22\xf1\x89',b'\x22\x06', b'\x22\xf1\x89',b'\x22\xf1\x89']


for param in data:
    logger.debug("Requesting: " + str(param.hex()))
    conn.send(param)
    response = None
    #while response is None:
    response = conn.wait_frame()
    if response:
        print("Response: " + str(response.hex()))

conn.close()

