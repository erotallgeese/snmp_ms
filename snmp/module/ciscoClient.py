from easysnmp import Session, EasySNMPError

from .baseClient import SnmpBaseClient, SnmpInterfaceData

from .resp import SnmpResp
from .oid.oids import GeneralOids

oids = GeneralOids()

class SnmpCiscoCpuData():
    index = None
    cpmCPUTotal5secRev = None
    cpmCPUTotal1minRev = None
    cpmCPUTotal5minRev = None

    def __str__(self):
        return 'type="cpu" index={} cpmCPUTotal5secRev={} cpmCPUTotal1minRev={} cpmCPUTotal5minRev={}'.format(self.index, self.cpmCPUTotal5secRev, self.cpmCPUTotal1minRev, self.cpmCPUTotal5minRev)

class SnmpCiscoClient(SnmpBaseClient):
    TAG = 'SnmpCiscoClient'

    def __init__(self, base):
        self.session = base.session
        self.vendor = base.vendor
        self.uuid = base.uuid
        self.version = self.session.version
        #print('version: {}'.format(self.version))

    # https://www.cisco.com/c/en/us/support/docs/ip/simple-network-management-protocol-snmp/26007-faq-snmpcounter.html
    def getInterface(self):
        if self.version == 1:
            try:
                ifList = list()
                descrList = self.session.walk(oids.ciscointerface.ifName)

                for i in range(len(descrList)):
                    if oids.ciscointerface.ifName == descrList[i].oid:  # only check subset
                        s = SnmpInterfaceData()
                        s.index = descrList[i].oid_index
                        s.ifDescr = descrList[i].value

                        s.ifSpeed = self.session.get((oids.ciscointerface.ifHighSpeed, s.index)).value
                        s.ifInOctets = self.session.get((oids.ifs.ifInOctets, s.index)).value
                        s.ifOutOctets = self.session.get((oids.ifs.ifOutOctets, s.index)).value

                        ifList.append(s)
                return ifList
            except EasySNMPError, e:
                errMsg = '{}: getInterface error: {}'.format(self.TAG, str(e))
                print(errMsg)
                return errMsg
            return []
        else:
            try:
                ifList = list()
                descrList = self.session.walk(oids.ciscointerface.ifName)

                for i in range(len(descrList)):
                    if oids.ciscointerface.ifName == descrList[i].oid:  # only check subset
                        s = SnmpInterfaceData()
                        s.index = descrList[i].oid_index
                        s.ifDescr = descrList[i].value

                        s.ifSpeed = self.session.get((oids.ciscointerface.ifHighSpeed, s.index)).value
                        s.ifInOctets = self.session.get((oids.ciscointerface.ifHCInOctets, s.index)).value
                        s.ifOutOctets = self.session.get((oids.ciscointerface.ifHCOutOctets, s.index)).value

                        ifList.append(s)
                return ifList
            except EasySNMPError, e:
                errMsg = '{}: getInterface error: {}'.format(self.TAG, str(e))
                print(errMsg)
                return errMsg
            return []
        return ''

    def getVendorCpu(self):
        try:
            cpuList = list()
            cpu5secList = self.session.walk(oids.ciscoprocess.cpmCPUTotal5secRev)

            for i in range(len(cpu5secList)):
                if oids.ciscoprocess.cpmCPUTotal5secRev == cpu5secList[i].oid:
                    s = SnmpCiscoCpuData()
                    s.index = cpu5secList[i].oid_index
                    s.cpmCPUTotal5secRev = cpu5secList[i].value

                    s.cpmCPUTotal1minRev = self.session.get((oids.ciscoprocess.cpmCPUTotal1minRev, s.index)).value
                    s.cpmCPUTotal5minRev = self.session.get((oids.ciscoprocess.cpmCPUTotal5minRev, s.index)).value

                    cpuList.append(s)
            return cpuList
        except EasySNMPError, e:
            errMsg = '{}: getVendorCpu error: {}'.format(self.TAG, str(e))
            print(errMsg)
            return errMsg
        
        return []