import threading

from .module.baseClient import SnmpBaseClient
from .module.ciscoClient import SnmpCiscoClient 
from .module.resp import SnmpResp


# Serve as an session to an snmp agent to retreive data
class SnmpSession(object):
    TAG = 'SnmpClient'
    
    def __init__(self, hostname='',
                       remote_port=161,
                       version=2,
                       community='public',
                       security_level='auth_with_privacy',     # (no_auth_or_privacy, auth_without_privacy or auth_with_privacy)
                       security_username='',
                       auth_protocol='DEFAULT',      # (MD5 or SHA)
                       auth_password='',
                       privacy_protocol='DEFAULT',   # (DES, AES, AES192, AES256)
                       privacy_password='',
                       context=''):
        # because it can't get those infos from easysnmp.session directlly, preseve an copy here.
        self.hostname = hostname
        self.remote_port = remote_port
        self.version = version
        self.community = community
        self.security_level = security_level
        self.security_username = security_username
        self.auth_protocol = auth_protocol
        self.auth_password = auth_password
        self.privacy_protocol = privacy_protocol
        self.privacy_password = privacy_password
        self.context = context

        self.snmpClient = None
        self.lock = threading.Lock()  # this lock is used for locking same host.
        
        try:
            self.snmpClient = SnmpBaseClient(use_long_names=True,
                                            use_numeric=True,
                                            hostname=hostname,
                                            remote_port=remote_port,
                                            version=version,
                                            community=community,
                                            security_level=security_level,
                                            security_username=security_username,
                                            auth_protocol=auth_protocol,
                                            auth_password=auth_password,
                                            privacy_protocol=privacy_protocol,
                                            privacy_password=privacy_password,
                                            context=context)

        except Exception, e:
            print('{}: __init__ error: {}'.format(self.TAG, str(e)))

    # @return true if remote host is valid and vice versa
    def checkVendor(self):
        self.snmpClient.getVender()

        if self.snmpClient.vendor != None:
            # switch the worker by vendor if support, or use default one. 
            print('<< vendor: ' + self.snmpClient.vendor)
            if self.snmpClient.vendor == 'cisco':
                self.snmpClient = SnmpCiscoClient(self.snmpClient)
            return True
        return False

    # check remote server valid or not
    # @return true if remote host is valid and vice versa
    def test(self):
        return self.snmpClient.test()

    def getHostStorage(self):
        return SnmpResp(self, self.snmpClient.getHostStorage()).resp()

    def getHostProcessLoad(self):
        return SnmpResp(self, self.snmpClient.getHostProcessLoad()).resp()

    def getInterface(self):
        return SnmpResp(self, self.snmpClient.getInterface()).resp()

    def getVendorCpu(self):
        return SnmpResp(self, self.snmpClient.getVendorCpu()).resp()

    def getAllData(self):
        if self.test() == True: # reduce retry time for invalid remote server
            r = SnmpResp(self)
            l = []

            # get cpu
            lt = self.snmpClient.getHostProcessLoad()
            if isinstance(lt, list):
                l.extend(lt)

            # get storage
            lt = self.snmpClient.getHostStorage()
            if isinstance(lt, list):
                l.extend(lt)

            # get interface
            lt = self.snmpClient.getInterface()
            if isinstance(lt, list):
                l.extend(lt)

            # get vendor cup
            lt = self.snmpClient.getVendorCpu()
            if isinstance(lt, list):
                l.extend(lt)

            r.data = l
            return r.resp()

        return []
        