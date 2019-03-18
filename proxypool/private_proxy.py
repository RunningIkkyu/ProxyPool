
class PrivateProxy(object):
    """ Get your private proxy """
    def __init__(self, filename='myproxies.txt'):
        self.proxies_list = []
        self.filename = filename

    def get_proxies(self):
        with open(self.filename, 'r') as f:
            for line in f.readlines():
                self.proxies_list.append(line.strip())
        print('[INFO] Resolve private proxy success!')
        return self.proxies_list
