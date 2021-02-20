import ctypes
from ctypes import Structure, WINFUNCTYPE, POINTER, cast, c_long, c_void_p, c_ulong, byref
from tactrix import Error_ID
import pprint


class PASSTHRU_MSG(Structure):
    _fields_ = [("ProtocolID", c_ulong),
        ("RxStatus", c_ulong),
        ("TxFlags", c_ulong),
        ("Timestamp", c_ulong),
        ("DataSize", c_ulong),
        ("ExtraDataindex", c_ulong),
        ("Data", ctypes.c_char_p)]

class J2534():
    dllPassThruOpen = None 
    dllPassThruClose = None
    dllPassThruConnect = None
    dllPassThruDisconnect  = None
    dllPassThruReadMsgs  = None
    dllPassThruWriteMsgs = None
    dllPassThruStartPeriodicMsgMsgs = None
    dllPassThruStopPeriodicMsgMsgs = None
    
    


    def __init__(self, dllName = "op20pt32.dll", location = "C:/Program Files (x86)/OpenECU/OpenPort 2.0/drivers/openport 2.0/"):

        global dllPassThruOpen 
        global dllPassThruClose
        global dllPassThruConnect
        global dllPassThruDisconnect 
        global dllPassThruReadMsgs 
        global dllPassThruWriteMsgs
        global dllPassThruStartPeriodicMsgMsgs
        global dllPassThruStopPeriodicMsgMsgs

        self.hDLL = ctypes.cdll.LoadLibrary(location + dllName)

        #if hDLL:
        #    return Error_ID.STATUS_NOERROR
        #else:
        #    return Error_ID.ERR_FAILED

        dllPassThruOpenProto = WINFUNCTYPE(
            c_long,
            c_void_p,
            POINTER(c_ulong))
        
        dllPassThruOpenParams = (1, "pName", 0),(1, "pDeviceID", 0)
        dllPassThruOpen = dllPassThruOpenProto(("PassThruOpen", self.hDLL), dllPassThruOpenParams)
        
        
        dllPassThruCloseProto = WINFUNCTYPE(
            c_long,
            c_ulong)
        
        dllPassThruCloseParams = (1, "DeviceID", 0),
        dllPassThruClose = dllPassThruCloseProto(("PassThruClose", self.hDLL), dllPassThruCloseParams) 
        
        dllPassThruConnectProto = WINFUNCTYPE(
            c_long,
            c_ulong,
            c_ulong,
            c_ulong,
            c_ulong,
            POINTER(c_ulong))
        
        dllPassThruConnectParams = (1, "DeviceID", 0), (1, "ProtocolID", 0), (1, "Flags", 0), (1, "BaudRate", 500000), (1, "pChannelID", 0)
        dllPassThruConnect = dllPassThruConnectProto(("PassThruConnect", self.hDLL), dllPassThruConnectParams)
        
        dllPassThruDisconnectProto = WINFUNCTYPE(
            c_long,
            c_ulong)
        
        dllPassThruDisconnectParams = (1, "ChannelID", 0),
        dllPassThruDisconnect = dllPassThruDisconnectProto(("PassThruDisconnect", self.hDLL), dllPassThruDisconnectParams) 
    
        dllPassThruReadMsgsProto = WINFUNCTYPE(
            c_long,
            c_ulong,
            POINTER(PASSTHRU_MSG),
            POINTER(c_ulong),
            c_ulong)
    
        dllPassThruReadMsgsParams = (1, "ChannelID", 0), (1, "pMsg", 0), (1, "pNumMsgs", 0), (1, "Timeout", 0)
        dllPassThruReadMsgs = dllPassThruReadMsgsProto(("PassThruReadMsgs", self.hDLL), dllPassThruReadMsgsParams)
    
        dllPassThruWriteMsgsProto = WINFUNCTYPE(
            c_long,
            c_ulong,
            POINTER(PASSTHRU_MSG),
            POINTER(c_ulong),
            c_ulong)
    
        dllPassThruWriteMsgsParams = (1, "ChannelID", 0), (1, "pMsg", 0), (1, "pNumMsgs", 0), (1, "Timeout", 0)
        dllPassThruWriteMsgs = dllPassThruWriteMsgsProto(("PassThruWriteMsgs", self.hDLL), dllPassThruWriteMsgsParams)
    
        dllPassThruStartPeriodicMsgProto = WINFUNCTYPE(
            c_long,
            c_ulong,
            POINTER(PASSTHRU_MSG),
            POINTER(c_ulong),
            c_ulong)
    
        dllPassThruStartPeriodicMsgParams = (1, "ChannelID", 0), (1, "pMsg", 0), (1, "pMsgID", 0), (1, "TimeInterval", 0)
        dllPassThruStartPeriodicMsgMsgs = dllPassThruStartPeriodicMsgProto(("PassThruStartPeriodicMsg", self.hDLL), dllPassThruStartPeriodicMsgParams)
    
        dllPassThruStopPeriodicMsgProto = WINFUNCTYPE(
            c_long,
            c_ulong,
            c_ulong)
    
        dllPassThruStopPeriodicMsgParams = (1, "ChannelID", 0), (1, "MsgID", 0)
        dllPassThruStopPeriodicMsgMsgs = dllPassThruStopPeriodicMsgProto(("PassThruStopPeriodicMsg", self.hDLL), dllPassThruStopPeriodicMsgParams)

    def PassThruOpen(self, pDeviceID = None):
        if not pDeviceID:
            pDeviceID = POINTER(c_ulong)()
    
        result = dllPassThruOpen(POINTER(ctypes.c_int)(), pDeviceID)
        return Error_ID(hex(result)), pDeviceID
    
    
    def PassThruConnect(self, deviceID, protocol, baudrate, pChannelID = None):
        if not pChannelID:
            pChannelID = POINTER(c_ulong)()
    
        result = dllPassThruConnect(deviceID, c_ulong(protocol), 0, baudrate, pChannelID)
        return Error_ID(hex(result)), pChannelID
    
    
    def PassThruClose(self, DeviceID):
        result = dllPassThruClose(DeviceID)
        return Error_ID(hex(result))
    
    
    def PassThruDisconnect(self, ChannelID):
        result = dllPassThruDisconnect(ChannelID)
        return Error_ID(hex(result))
    
    
    def PassThruReadMsgs(self, ChannelID, pNumMsgs = 1, Timeout = 0):
        pMsg = PASSTHRU_MSG()
        pNumMsgs = c_ulong(pNumMsgs)
    
        result = dllPassThruReadMsgs(ChannelID, byref(pMsg), byref(pNumMsgs), c_ulong(Timeout))
        return Error_ID(hex(result)), pMsg
    
    
    def PassThruWriteMsgs(self, ChannelID, Data, pNumMsgs = 1, Timeout = 100):
        Msg = PASSTHRU_MSG()
    
        Msg.Data = Data
        Msg.DataSize = len(Data)
    
        result = dllPassThruWriteMsgs(ChannelID, byref(Msg), byref(c_ulong(pNumMsgs)), c_ulong(Timeout))
        return Error_ID(hex(result))
    
    
    def PassThruStartPeriodicMsg(self, ChannelID, Data, MsgID = 0, TimeInterval = 100):
        pMsg = PASSTHRU_MSG()
    
        pMsg.Data = Data
        pMsg.DataSize = len(Data)
    
        result = dllPassThruStartPeriodicMsgMsgs(ChannelID, byref(pMsg), byref(c_ulong(MsgID)), c_ulong(TimeInterval))
    
        return Error_ID(hex(result))
    
    def PassThruStopPeriodicMsg(self, ChannelID, MsgID):
        result = dllPassThruStopPeriodicMsgMsgs(ChannelID, MsgID)
    
        return Error_ID(hex(result))



#
#
#    dllPassThruStartMsgFilterProto = WINFUNCTYPE(
#        c_long,
#((unsigned long ChannelID,
#                              unsigned long FilterType, const PASSTHRU_MSG *pMaskMsg, const PASSTHRU_MSG *pPatternMsg,
#                              const PASSTHRU_MSG *pFlowControlMsg, unsigned long *pMsgID);
#    dllPassThruStopMsgFilterProto = WINFUNCTYPE(
#        c_long,
#((unsigned long ChannelID, unsigned long MsgID);
#
#
#    dllPassThruSetProgrammingVoltageProto = WINFUNCTYPE(
#        c_long,
#((unsigned long DeviceID, unsigned long Pin, unsigned long Voltage);
#
#
#    dllPassThruReadVersionProto = WINFUNCTYPE(
#        c_long,
#((char *pApiVersion,char *pDllVersion,char *pFirmwareVersion,unsigned long DeviceID);
#
#
#    dllPassThruGetLastErrorProto = WINFUNCTYPE(
#        c_long,
#((char *pErrorDescription);
#
#
#    dllPassThruIoctlProto = WINFUNCTYPE(
#        c_long,
#((unsigned long ChannelID, unsigned long IoctlID, const void *pInput, void *pOutput);



