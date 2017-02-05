from logger import *
from io import StringIO

class Attacker:
    def __init__(self, sock, payload, chunk_size):
        self.socket = sock
        self.payload = StringIO(payload)
        self.chunk_size = chunk_size
        self.is_done = False
        self.killed_prematurely = False

    def execute_step(self):
            chunk = self.get_chunk()
            encoded_chunk = chunk.encode()
            try:
                self.socket.send(encoded_chunk)
                if len(chunk) < self.chunk_size:
                    self.is_done = True
                    Logger.debug(self.socket.recv(1024))
                    self.socket.close();
            except:
                self.is_done = True
                self.socket.close()
                if len(self.payload.getvalue()) != 0:
                    self.killed_prematurely = True

    def get_chunk(self):
        return self.payload.read(self.chunk_size)















#
