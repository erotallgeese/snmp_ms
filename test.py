import pprint
import time

from snmp.snmps import SnmpSession
from snmp.snmpm import SnmpManager

def cb(data):
    pprint.pprint(data)

s2 = SnmpSession(hostname='172.17.0.2', version=3, security_level='auth_with_privacy', security_username='loker3', auth_protocol='MD5', auth_password='12345678', privacy_protocol="DES", privacy_password='87654321')
s3 = SnmpSession(hostname='172.17.0.2', version=3, security_level='no_auth_or_privacy', security_username='loker1')
s4 = SnmpSession(hostname='172.17.0.2', community='lokertest', version=1)

m = SnmpManager(callback=cb)
m.start()
time.sleep(1)   # wait for thread start

#m.add(s2)
#m.add(s3)
#m.add(s4)
m.addList([s2, s3, s4])

time.sleep(4)   # wait for thread start
m.stop()