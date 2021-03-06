from connections import J2534Connection
from connections import FakeConnection
import logging
import time

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)
f_handler = logging.StreamHandler()
logger.addHandler(f_handler)


conn = J2534Connection(
    windll="C:/Program Files (x86)/OpenECU/OpenPort 2.0/drivers/openport 2.0/op20pt32.dll",
    rxid=0x7E8,
    txid=0x7E0,
)
# conn = FakeConnection()
conn.open()

conn.txid = 0x700
conn.resetCable()

data = [b"\x22\xf1\x90\xf1\x89\xf1\x91\xf8\x06\xf1\xa3"]


for i in range(0, 1):
    for param in data:
        logger.debug("Requesting: " + str(param.hex()))
        conn.send(param)
        response = None
        # while response is None:
        response = conn.wait_frame()
        if response:
            print("Response: " + str(response.hex()))

conn.close()
