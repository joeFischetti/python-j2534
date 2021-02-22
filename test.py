from j2534 import J2534
from j2534 import Protocol_ID
from j2534 import Ioctl_ID
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


#if result.value != 0:
#    devID = 12345678

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

print("Setting up a flow contorl filter for ISO15765")
result = interface.PassThruStartMsgFilter(channelID, protocol.value)
print("    " + result.name)
print()

print("Clearing the rxBuffer")
result = interface.PassThruIoctl(channelID, Ioctl_ID.CLEAR_RX_BUFFER)
print("    " + result.name)
print()

print("Reading buffer (since it should be empty)")
result, response, numMessages = interface.PassThruReadMsgs(channelID, protocol.value, 1, 10)
print("    " + result.name)
print("    " + str(response))
print()

data = b'\x10\x03'
print("Sending bytes to switch to extended diag: " + str(data.hex()))
result = interface.PassThruWriteMsgs(channelID, data, protocol.value)
result = interface.PassThruIoctl(channelID, Ioctl_ID.CLEAR_RX_BUFFER)
print("    Transmit: " + result.name)
result, response, numMessages = interface.PassThruReadMsgs(channelID, protocol.value, 1, 10)
print("    Receive: " + result.name + ", Num Messages: " + str(numMessages.value))
print("    Response: " + str(response.hex()))
print()


data = b'\x22\xf1\x90'
print("Sending bytes to read vin (0x22 f1 90): " + str(data.hex()))
result = interface.PassThruWriteMsgs(channelID, data, protocol.value)
result = interface.PassThruIoctl(channelID, Ioctl_ID.CLEAR_RX_BUFFER)
print("    Transmit: " + result.name)
result, response, numMessages = interface.PassThruReadMsgs(channelID, protocol.value, 1, 10)
print("    Receive: " + result.name + ", Num Messages: " + str(numMessages.value))
print("    Response: " + str(response.hex()))
print()

data = b'\x22\xf1\x91'
print("Sending bytes to read ECU Hardware Number (0x22 f1 91): " + str(data.hex()))
result = interface.PassThruWriteMsgs(channelID, data, protocol.value)
result = interface.PassThruIoctl(channelID, Ioctl_ID.CLEAR_RX_BUFFER)
print("    Transmit: " + result.name)
result, response, numMessages = interface.PassThruReadMsgs(channelID, protocol.value, 1, 10)
print("    Receive: " + result.name + ", Num Messages: " + str(numMessages.value))
print("    Response: " + str(response.hex()))
print()

data = b'\x22\xf1\x89'
print("Sending bytes to read ASW Version number (0x22 f1 89): " + str(data.hex()))
result = interface.PassThruWriteMsgs(channelID, data, protocol.value)
print("    Transmit: " + result.name)
result, response, numMessages = interface.PassThruReadMsgs(channelID, protocol.value, 1, 10)
print("    Receive: " + result.name + ", Num Messages: " + str(numMessages.value))
print("    Response: " + str(response.hex()))
print()



print("Disconnecting from pass through device")
result = interface.PassThruDisconnect(channelID)
print("    " + result.name)
print()


print("Closing Pass through device")
result = interface.PassThruClose(devID)
print("    " + result.name)
print()

