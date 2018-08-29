import datetime

class SnmpResp():
    data = []
    error = None
    target = None

    def __init__(self, target=None, data=[]):
        self.time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.target = target
        self.data = data

    def resp(self):
        if self.target != None:
            if isinstance(self.data, list) and len(self.data) > 0:
                ret = []
                prefix = 'logtime="{}" host="{}" port="{}"'.format(self.time, self.target.hostname, self.target.remote_port)
                if self.target.community:
                    prefix += ' community="{}"'.format(self.target.community)
                if self.target.security_username:
                    prefix += ' security_username="{}"'.format(self.target.security_username)
                if self.target.context:
                    prefix += ' context="{}"'.format(self.target.context)
                
                for d in self.data:
                    ret.append('{} {}'.format(prefix, str(d)))

                return ret

        return []