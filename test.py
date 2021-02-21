from j2534 import J2534
from j2534 import Protocol_ID
import ctypes

devID = None
channelID = None

protocol = Protocol_ID.ISO15765
baudrate = 500000;

interface = J2534()

print("Opening Pass through device")
result, devID = interface.PassThruOpen()
print("    " + result.name)
print()


if result.value != 0:
    devID = 12345678

print("Getting device information")
result, firmwareVersion, dllVersion, apiVersion = interface.PassThruReadVersion(devID)
print("    " + result.name)
print("    firmware: " + str(firmwareVersion.value))
print("    dllVersion: " + str(dllVersion.value))
print("    apiVersion: " + str(apiVersion.value))
print()

print("Connecting to pass through device")
result, channelID = interface.PassThruConnect(devID, protocol.value, baudrate)
print("    " + result.name)
print()

if result.value != 0:
    channelID = 1

print("Setting up a flow contorl filter for ISO15765")
result = interface.PassThruStartMsgFilter(channelID, protocol.value)
print("    " + result.name)
print()


data = b'\x22\xf1\x90'
print("Sending bytes to read vin (0x22 f1 90): " + str(data.hex()))
result = interface.PassThruWriteMsgs(channelID, data)
print("    " + result.name)
print()

print("Reading data back")
result, response, numResponse = interface.PassThruReadMsgs(channelID)
print("    result: " + result.name)
if numResponse:
    print("    response: " + str(response))
    print()


print("Disconnecting from pass through device")
result = interface.PassThruDisconnect(channelID)
print("    " + result.name)
print()


print("Closing Pass through device")
result = interface.PassThruClose(devID)
print("    " + result.name)
print()

