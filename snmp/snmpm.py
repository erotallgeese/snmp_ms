import os
import threading
from multiprocessing.pool import ThreadPool
import time
import pprint

from easysnmp import Session, EasySNMPError

from .module.baseClient import SnmpBaseClient

# Serve as an manager to maintain an snmp agent list and polling for data
class SnmpManager(object):
    TAG = 'SnmpManager'
    
    # suppose there would start an thread to polling for data
    def __init__(self, enablePool=True, callback=None, pollingInterval=240):
        self.enablePool = enablePool    # enable threadpool or not
        self.poolSize = 10              # threadpool size
        self.callback = callback        # callback function after getting data. this function's definition should be def func(data), where data is an 2d list.
        self.p = None                   # thread pointer for polling
        self.p_add = None               # thread pointer for polling once, used at addList
        self.lock = threading.Lock()    # used to protect sessionList
        self.sessionList = []           # the snmp agent list (list of SnmpSession)
        self.polling_interval = pollingInterval    # polling interval
        
    #def __del__(self):
    #    pass
    
    # add sessions to be monitored
    # there should be an key: (hostname, remote_port, community, security_username, context),
    # tits, it should not exist duplicated session with same key
    def add(self, session):
        # check remote host valid or not
        if session.checkVendor():
            with self.lock:
                # check duplicate
                isDuplicate = False
                dupHost = None
                for s in self.sessionList:
                    if s.hostname == session.hostname:
                        dupHost = s
                    if (s.hostname == session.hostname and 
                        s.remote_port == session.remote_port and
                        s.community == session.community and
                        s.security_username == session.security_username and
                        s.context == session.context):
                        isDuplicate = True
                        print('<< skip duplicated session')
                        break
                if isDuplicate == False:
                    # ideally it should let same host exist with same lock, but threading in python would also be locked by gil.
                    # the truth here is that it doesnot need to let same host with same lock but it still not a bad thing...
                    if dupHost != None:
                        session.lock = dupHost.lock
                    self.sessionList.append(session)
                    return True
        
        return False

    # add an list of sessions to be monitored
    # the behavior is as same as add plus it would do polling immediatelly
    def addList(self, sessionList):
        addList = list()
        for session in sessionList:
            if session.checkVendor():
                with self.lock:
                    # check duplicate
                    isDuplicate = False
                    dupHost = None
                    for s in self.sessionList:
                        if s.hostname == session.hostname:
                            dupHost = s
                        if (s.hostname == session.hostname and 
                            s.remote_port == session.remote_port and
                            s.community == session.community and
                            s.security_username == session.security_username and
                            s.context == session.context):
                            isDuplicate = True
                            print('<< skip duplicated session')
                            break
                    if isDuplicate == False:
                        # ideally it should let same host exist with same lock, but threading in python would also be locked by gil.
                        # the truth here is that it doesnot need to let same host with same lock but it still not a bad thing...
                        if dupHost != None:
                            session.lock = dupHost.lock
                        self.sessionList.append(session)
                        addList.append(session)
            
        # get data
        if self.p_add != None:
            self.p_add.join()
        self.p_add = threading.Thread(target=self._polling_once, args=(addList, ))
        self.p_add.start()

    # tbd...
    def update(self, session, **kwargs):
        pass

    # remove all for monitored list
    def clean(self):
        with self.lock:
            self.sessionList.clear()

    @staticmethod
    def _doJobInPool(session):
        # the session in easysnmp is not thread-safe, here need the lock to prevent from snmpget on same host,
        # or it would cause segment fault
        with session.lock:
            return session.getAllData()

    def _polling_once(self, sessionList):
        print('<< enter polling once')
        sessionData = []
        with self.lock:     # still need lock because the content in sessionList may be deleted at other thread
            if self.enablePool:
                pool = ThreadPool(self.poolSize)
                sessionData = pool.map(SnmpManager._doJobInPool, sessionList)
                pool.close()
                pool.join()
            else:
                for s in sessionList:
                    sessionData.append(s.getAllData())

        #pprint.pprint(sessionData)
        if sessionData and self.callback != None:
            self.callback(sessionData)

        print('<< leave polling once')

    def _polling(self):
        print('<< enter polling')
        starttime = time.time()

        while self.p_stop == False:
            print('<< polling...{}'.format(time.time()))
            sessionData = []
            with self.lock:
                if self.enablePool:
                    # i have try to use multiprocessing.pool instead of ThreadPool, but it would fall into pickle error.
                    # (self.sessionList can't be pickled to process)
                    pool = ThreadPool(self.poolSize)
                    sessionData = pool.map(SnmpManager._doJobInPool, self.sessionList)
                    pool.close()
                    pool.join()
                else:
                    for s in self.sessionList:
                        sessionData.append(s.getAllData())
                        
            # sessionData would be 2d list where is first dimension is session
            #pprint.pprint(sessionData)
            if sessionData and self.callback != None:
                self.callback(sessionData)
                        
            time.sleep(self.polling_interval - ((time.time() - starttime) % self.polling_interval))
            
        print('<< leave polling')

    # start polling
    def start(self):
        self.p_stop = False
        self.p = threading.Thread(target=self._polling, args=())
        self.p.start()

    # stop polling
    def stop(self):
        if self.p:
            self.p_stop = True
            self.p.join()
            self.p = None