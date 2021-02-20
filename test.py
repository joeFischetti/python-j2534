import j2534
import tactrix
import ctypes

devID = None
channelID = None

protocol = ctypes.c_ulong(tactrix.Protocol_ID.ISO15765.value)
baudrate = 500000;

print("Checking/Loading DLL\n")
j2534.checkDLL()

print("Opening Pass through device")
result, devID = j2534.PassThruOpen()
print("    " + result.name + "\n")


if result.value != 0:
    devID = 1

print("Connecting to pass through device")
result, channelID = j2534.PassThruConnect(devID, protocol, baudrate)
print("    " + result.name + "\n")

if result.value != 0:
    channelID = 1


data = b'\x23\x14\xd0\x01\xb3\xaa\x01'
print("Sending arbitrary bytes: " + str(data.hex()))
result = j2534.PassThruWriteMsgs(channelID, data)
print("    " + result.name + "\n")

print("Reading data back")
result, response = j2534.PassThruReadMsgs(channelID)
print("    " + result.name + "\n")

print("Disconnecting from pass through device")
result = j2534.PassThruDisconnect(channelID)
print("    " + result.name + "\n")


print("Closing Pass through device")
result = j2534.PassThruClose(devID)
print("    " + result.name + "\n")

