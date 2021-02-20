import ctypes
from ctypes import Structure, POINTER, cast, c_ulong, byref
from tactrix import Error_ID
import pprint

class J2534():
    hDLL = None
    isLibraryInitialized = False
    dllName = "op20pt32.dll"

class PASSTHRU_MSG(Structure):
    _fields_ = [("ProtocolID", ctypes.c_ulong),
        ("RxStatus", ctypes.c_ulong),
        ("TxFlags", ctypes.c_ulong),
        ("Timestamp", ctypes.c_ulong),
        ("DataSize", ctypes.c_ulong),
        ("ExtraDataindex", ctypes.c_ulong),
        ("Data", ctypes.c_char_p)]

hDLL = None
dllName = "op20pt32.dll"
 
dllPassThruOpen = None
dllPassThruClose = None
dllPassThruConnect = None
dllPassThruDisconnect = None
dllPassThruReadMsgs = None
dllPassThruWriteMsgs = None
dllPassThruStartPeriodicMsgMsgs = None
dllPassThruStopPeriodicMsgMsgs = None


def setUpFunctions():

    global dllPassThruOpen 
    global dllPassThruClose
    global dllPassThruConnect
    global dllPassThruDisconnect 
    global dllPassThruReadMsgs 
    global dllPassThruWriteMsgs
    global dllPassThruStartPeriodicMsgMsgs
    global dllPassThruStopPeriodicMsgMsgs
   
    dllPassThruOpenProto = ctypes.WINFUNCTYPE(
        ctypes.c_long,
        ctypes.c_void_p,
        POINTER(ctypes.c_ulong))
    
    dllPassThruOpenParams = (1, "pName", 0),(1, "pDeviceID", 0)
    dllPassThruOpen = dllPassThruOpenProto(("PassThruOpen", hDLL), dllPassThruOpenParams)
    
    
    dllPassThruCloseProto = ctypes.WINFUNCTYPE(
        ctypes.c_long,
        ctypes.c_ulong)
    
    dllPassThruCloseParams = (1, "DeviceID", 0),
    dllPassThruClose = dllPassThruCloseProto(("PassThruClose", hDLL), dllPassThruCloseParams) 
    
    dllPassThruConnectProto = ctypes.WINFUNCTYPE(
        ctypes.c_long,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_ulong,
        POINTER(ctypes.c_ulong))
    
    dllPassThruConnectParams = (1, "DeviceID", 0), (1, "ProtocolID", 0), (1, "Flags", 0), (1, "BaudRate", 500000), (1, "pChannelID", 0)
    dllPassThruConnect = dllPassThruConnectProto(("PassThruConnect", hDLL), dllPassThruConnectParams)
    
    dllPassThruDisconnectProto = ctypes.WINFUNCTYPE(
        ctypes.c_long,
        ctypes.c_ulong)
    
    dllPassThruDisconnectParams = (1, "ChannelID", 0),
    dllPassThruDisconnect = dllPassThruDisconnectProto(("PassThruDisconnect", hDLL), dllPassThruDisconnectParams) 

    dllPassThruReadMsgsProto = ctypes.WINFUNCTYPE(
        ctypes.c_long,
        ctypes.c_ulong,
        POINTER(PASSTHRU_MSG),
        POINTER(ctypes.c_ulong),
        ctypes.c_ulong)

    dllPassThruReadMsgsParams = (1, "ChannelID", 0), (1, "pMsg", 0), (1, "pNumMsgs", 0), (1, "Timeout", 0)
    dllPassThruReadMsgs = dllPassThruReadMsgsProto(("PassThruReadMsgs", hDLL), dllPassThruReadMsgsParams)

    dllPassThruWriteMsgsProto = ctypes.WINFUNCTYPE(
        ctypes.c_long,
        ctypes.c_ulong,
        POINTER(PASSTHRU_MSG),
        POINTER(ctypes.c_ulong),
        ctypes.c_ulong)

    dllPassThruWriteMsgsParams = (1, "ChannelID", 0), (1, "pMsg", 0), (1, "pNumMsgs", 0), (1, "Timeout", 0)
    dllPassThruWriteMsgs = dllPassThruWriteMsgsProto(("PassThruWriteMsgs", hDLL), dllPassThruWriteMsgsParams)

    dllPassThruStartPeriodicMsgProto = ctypes.WINFUNCTYPE(
        ctypes.c_long,
        ctypes.c_ulong,
        POINTER(PASSTHRU_MSG),
        POINTER(ctypes.c_ulong),
        ctypes.c_ulong)

    dllPassThruStartPeriodicMsgParams = (1, "ChannelID", 0), (1, "pMsg", 0), (1, "pMsgID", 0), (1, "TimeInterval", 0)
    dllPassThruStartPeriodicMsgMsgs = dllPassThruStartPeriodicMsgProto(("PassThruStartPeriodicMsg", hDLL), dllPassThruStartPeriodicMsgParams)

    dllPassThruStopPeriodicMsgProto = ctypes.WINFUNCTYPE(
        ctypes.c_long,
        ctypes.c_ulong,
        ctypes.c_ulong)

    dllPassThruStopPeriodicMsgParams = (1, "ChannelID", 0), (1, "MsgID", 0)
    dllPassThruStopPeriodicMsgMsgs = dllPassThruStopPeriodicMsgProto(("PassThruStopPeriodicMsg", hDLL), dllPassThruStopPeriodicMsgParams)


#
#
#    dllPassThruStartMsgFilterProto = ctypes.WINFUNCTYPE(
#        ctypes.c_long,
#((unsigned long ChannelID,
#                              unsigned long FilterType, const PASSTHRU_MSG *pMaskMsg, const PASSTHRU_MSG *pPatternMsg,
#                              const PASSTHRU_MSG *pFlowControlMsg, unsigned long *pMsgID);
#    dllPassThruStopMsgFilterProto = ctypes.WINFUNCTYPE(
#        ctypes.c_long,
#((unsigned long ChannelID, unsigned long MsgID);
#
#
#    dllPassThruSetProgrammingVoltageProto = ctypes.WINFUNCTYPE(
#        ctypes.c_long,
#((unsigned long DeviceID, unsigned long Pin, unsigned long Voltage);
#
#
#    dllPassThruReadVersionProto = ctypes.WINFUNCTYPE(
#        ctypes.c_long,
#((char *pApiVersion,char *pDllVersion,char *pFirmwareVersion,unsigned long DeviceID);
#
#
#    dllPassThruGetLastErrorProto = ctypes.WINFUNCTYPE(
#        ctypes.c_long,
#((char *pErrorDescription);
#
#
#    dllPassThruIoctlProto = ctypes.WINFUNCTYPE(
#        ctypes.c_long,
#((unsigned long ChannelID, unsigned long IoctlID, const void *pInput, void *pOutput);



def LoadJ2534DLL(dllName, location = None):
    global hDLL

    if not location:
        location = "C:/Program Files (x86)/OpenECU/OpenPort 2.0/drivers/openport 2.0/"
    hDLL = ctypes.cdll.LoadLibrary(location + dllName)
    if hDLL:
        setUpFunctions()
        return Error_ID.STATUS_NOERROR
    else:
        return Error_ID.ERR_FAILED


def checkDLL():
    if not hDLL:
        LoadJ2534DLL(dllName = dllName)
    return hDLL is not None


def getLastError():
    return lastError

def valid():
    return hDLL is not None


def PassThruOpen(pDeviceID = None):
    if not pDeviceID:
        pDeviceID = POINTER(ctypes.c_ulong)()

    result = dllPassThruOpen(POINTER(ctypes.c_int)(), pDeviceID)
    return Error_ID(hex(result)), pDeviceID


def PassThruConnect(deviceID, protocol, baudrate, pChannelID = None):
    if not pChannelID:
        pChannelID = POINTER(ctypes.c_ulong)()

    result = dllPassThruConnect(deviceID, protocol, 0, baudrate, pChannelID)
    return Error_ID(hex(result)), pChannelID


def PassThruClose(DeviceID):
    result = dllPassThruClose(DeviceID)
    return Error_ID(hex(result))


def PassThruDisconnect(ChannelID):
    result = dllPassThruDisconnect(ChannelID)
    return Error_ID(hex(result))


def PassThruReadMsgs(ChannelID, pNumMsgs = 1, Timeout = 0):
    pMsg = PASSTHRU_MSG()
    pNumMsgs = c_ulong(pNumMsgs)

    result = dllPassThruReadMsgs(ChannelID, byref(pMsg), byref(pNumMsgs), c_ulong(Timeout))
    return Error_ID(hex(result)), pMsg


def PassThruWriteMsgs(ChannelID, Data, pNumMsgs = 1, Timeout = 100):
    Msg = PASSTHRU_MSG()

    Msg.Data = Data
    Msg.DataSize = len(Data)

    result = dllPassThruWriteMsgs(ChannelID, byref(Msg), byref(c_ulong(pNumMsgs)), c_ulong(Timeout))
    return Error_ID(hex(result))


def PassThruStartPeriodicMsg(ChannelID, Data, MsgID = 0, TimeInterval = 100):
    pMsg = PASSTHRU_MSG()

    pMsg.Data = Data
    pMsg.DataSize = len(Data)

    result = dllPassThruStartPeriodicMsgMsgs(ChannelID, byref(pMsg), byref(c_ulong(MsgID)), c_ulong(TimeInterval))

    return Error_ID(hex(result))

def PassThruStopPeriodicMsg(ChannelID, MsgID):
    result = dllPassThruStopPeriodicMsgMsgs(ChannelID, MsgID)

    return Error_ID(hex(result))

