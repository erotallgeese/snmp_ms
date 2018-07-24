
# there would not list all oids but only needed in my application
class GeneralOids():
    def __init__(self):
        self.system = self.system()
        self.hr = self.host_resource()
        self.ciscoprocess = self.cisco_process()
        self.ifs = self.interface()
    
    class system():
        sysObjectID = '.1.3.6.1.2.1.1.2'

    # how to calculate the i/o bandwidth: 
    # https://www.cisco.com/c/en/us/support/docs/ip/simple-network-management-protocol-snmp/8141-calculate-bandwidth-snmp.html
    class interface():
        ifDescr =       '.1.3.6.1.2.1.2.2.1.2'
        ifSpeed =       '.1.3.6.1.2.1.2.2.1.5'
        ifInOctets =    '.1.3.6.1.2.1.2.2.1.10'
        ifOutOctets =   '.1.3.6.1.2.1.2.2.1.16'

    class host_resource():
        hrStorageDescr =    '.1.3.6.1.2.1.25.2.3.1.3'
        hrStorageSize =     '.1.3.6.1.2.1.25.2.3.1.5'
        hrStorageUsed =     '.1.3.6.1.2.1.25.2.3.1.6'

        hrDeviceDescr =     '.1.3.6.1.2.1.25.3.2.1.3'
        hrProcessorLoad =   '.1.3.6.1.2.1.25.3.3.1.2'

    class cisco_process():
        cpmCPUTotal5sec = '.1.3.6.1.4.1.9.9.109.1.1.1.1.3'
        cpmCPUTotal1min = '.1.3.6.1.4.1.9.9.109.1.1.1.1.4'
        cpmCPUTotal5min = '.1.3.6.1.4.1.9.9.109.1.1.1.1.5'