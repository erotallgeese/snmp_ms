from easysnmp import Session, EasySNMPError

from .baseClient import SnmpBaseClient

from .resp import SnmpResp
from .oid.oids import GeneralOids

oids = GeneralOids()

class SnmpCiscoCpuData():
    index = None
    cpmCPUTotal5sec = None
    cpmCPUTotal1min = None
    cpmCPUTotal5min = None

    def __str__(self):
        return 'type="cpu", index={}, cpmCPUTotal5sec={}, cpmCPUTotal1min={}, cpmCPUTotal5min={}'.format(self.index, self.cpmCPUTotal5sec, self.cpmCPUTotal1min, self.cpmCPUTotal5min)

class SnmpCiscoClient(SnmpBaseClient):
    TAG = 'SnmpCiscoClient'

    def __init__(self, base):
        self.session = base.session
        self.vendor = base.vendor
        self.uuid = base.uuid

    def getVendorCpu(self):
        try:
            cpuList = list()
            cpu5secList = self.session.walk(oids.ciscoprocess.cpmCPUTotal5sec)

            for i in range(len(cpu5secList)):
                if oids.ciscoprocess.cpmCPUTotal5sec == cpu5secList[i].oid:
                    s = SnmpCiscoCpuData()
                    s.index = cpu5secList[i].oid_index
                    s.cpmCPUTotal5sec = cpu5secList[i].value

                    s.cpmCPUTotal1min = self.session.get((oids.ciscoprocess.cpmCPUTotal1min, s.index)).value
                    s.cpmCPUTotal5min = self.session.get((oids.ciscoprocess.cpmCPUTotal5min, s.index)).value

                    cpuList.append(s)
            return cpuList
        except EasySNMPError, e:
            errMsg = '{}: getVendorCpu error: {}'.format(self.TAG, str(e))
            print(errMsg)
            return errMsg
        
        return []