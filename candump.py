from connections import J2534Connection
from connections import FakeConnection
import logging
import time

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)
f_handler = logging.StreamHandler()
logger.addHandler(f_handler)


conn = J2534Connection(windll='C:/Program Files (x86)/OpenECU/OpenPort 2.0/drivers/openport 2.0/op20pt32.dll', rxid=0x7E8, txid=0x7E0, sniff=True)
#conn = FakeConnection()
conn.open()

while True:
    response = conn.wait_frame()
    if response:
        logger.info(str(response.hex()))

conn.close()

