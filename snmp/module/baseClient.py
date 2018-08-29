import uuid

from easysnmp import Session, EasySNMPError
from .resp import SnmpResp
from .vendor.mapping import vendor_map
from .oid.oids import GeneralOids

oids = GeneralOids()

class SnmpHrStorageData():
    index = None
    hrStorageDescr = None
    hrStorageSize = None
    hrStorageUsed = None

    def __str__(self):
        return 'type="storage" index="{}" descr="{}" size={} used={}'.format(self.index, self.hrStorageDescr, self.hrStorageSize, self.hrStorageUsed)

class SnmpInterfaceData():
    index = None
    ifDescr = None
    ifSpeed = None
    ifInOctets = None
    ifOutOctets = None

    def __str__(self):
        return 'type="interface" index="{}" descr="{}" speed={} in={} out={}'.format(self.index, self.ifDescr, self.ifSpeed, self.ifInOctets, self.ifOutOctets)

class SnmpProcessLoadData():
    index = None
    hrDeviceDescr = None
    hrProcessorLoad = None

    def __str__(self):
        return 'type="process" index="{}" descr="{}" load={}'.format(self.index, self.hrDeviceDescr, self.hrProcessorLoad)

# Base worker class to get data through snmp. Other vendor should inherit this class and overwrite their functions.
class SnmpBaseClient(object):
    TAG = 'SnmpBaseClient'
    UNKNOWN_VENDOR = 'unknown'

    def __init__(self, **kwargs):
        self.vendor = None
        self.enterpriseId = None
        self.session = None
        
        try:
            self.uuid = uuid.uuid4().hex
            self.session = Session(**kwargs)
            
        except Exception, e:
            print('{}: __init__ error: {}'.format(self.TAG, str(e)))

    # check remote server valid or not
    def test(self):
        try:
            objectId = self.session.get((oids.system.sysObjectID, '0'))
            return True
        except Exception, e:
            print('{}: test error: {}'.format(self.TAG, str(e)))

        return False

    # according to its sysObjectID to distinguish its vendor
    def getVender(self):
        try:
            #objectId = self.session.get('sysObjectID.0')
            objectId = self.session.get((oids.system.sysObjectID, '0'))
            self.enterpriseId = objectId.value.split('.')[7]
            self.vendor = vendor_map[self.enterpriseId]
        
        except EasySNMPError, e:
            self.vendor = None
            print('{}: getVender error: {}'.format(self.TAG, str(e)))

        except Exception, e:
            self.vendor = self.UNKNOWN_VENDOR
            print('{}: unsupport vendor: {}'.format(self.TAG, str(e)))

    # retrieve for hrStorageDescr, hrStorageSize, hrStorageUsed
    def getHostStorage(self):
        try:
            storageList = list()
            descrList = self.session.walk(oids.hr.hrStorageDescr)

            for i in range(len(descrList)):
                if oids.hr.hrStorageDescr == descrList[i].oid:  # only check subset
                    s = SnmpHrStorageData()
                    s.index = descrList[i].oid_index
                    s.hrStorageDescr = descrList[i].value

                    s.hrStorageSize = self.session.get((oids.hr.hrStorageSize, s.index)).value
                    s.hrStorageUsed = self.session.get((oids.hr.hrStorageUsed, s.index)).value

                    storageList.append(s)
            return storageList

        except EasySNMPError, e:
            errMsg = '{}: getHostStorage error: {}'.format(self.TAG, str(e))
            print(errMsg)
            return errMsg
        
        return []

    def getHostProcessLoad(self):
        try:
            processList = list()
            plList = self.session.walk(oids.hr.hrProcessorLoad)

            for i in range(len(plList)):
                if oids.hr.hrProcessorLoad == plList[i].oid:  # only check subset
                    s = SnmpProcessLoadData()
                    s.index = plList[i].oid_index
                    s.hrProcessorLoad = plList[i].value

                    s.hrDeviceDescr = self.session.get((oids.hr.hrDeviceDescr, s.index)).value

                    processList.append(s)
            return processList

        except EasySNMPError, e:
            errMsg = '{}: getHostProcessLoad error: {}'.format(self.TAG, str(e))
            print(errMsg)
            return errMsg
        
        return []

    def getInterface(self):
        try:
            ifList = list()
            descrList = self.session.walk(oids.ifs.ifDescr)

            for i in range(len(descrList)):
                if oids.ifs.ifDescr == descrList[i].oid:  # only check subset
                    s = SnmpInterfaceData()
                    s.index = descrList[i].oid_index
                    s.ifDescr = descrList[i].value

                    s.ifSpeed = self.session.get((oids.ifs.ifSpeed, s.index)).value
                    s.ifInOctets = self.session.get((oids.ifs.ifInOctets, s.index)).value
                    s.ifOutOctets = self.session.get((oids.ifs.ifOutOctets, s.index)).value

                    ifList.append(s)
            return ifList

        except EasySNMPError, e:
            errMsg = '{}: getInterface error: {}'.format(self.TAG, str(e))
            print(errMsg)
            return errMsg
        
        return []

    def getVendorCpu(self, maxCount=64):
        return []