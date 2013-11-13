import socket
import signal
import time

from commandHandler import CommandHandler

class Serial(object):
    def __init__(self,port=21):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.bind(('0.0.0.0',port))
        s.listen(5)

        self.control_socket = s
        self.CLRF = "\r\n"

        signal.signal(signal.SIGINT,self.signal_handler)

    def signal_handler(self, sig, id):
        exit()

    def gets(self):
        return self.fd.readline()

    def respond(self,message):
        self.client.send(message)
        self.client.send(self.CLRF)

    def run(self):
        while 1:
            self.client, _ = self.control_socket.accept()
            self.fd = self.client.makefile('rw', 0)

            self.respond("220 OHAI")

            handler = CommandHandler(self)
            while 1:
                request = self.gets()
                if request:
                    self.respond(handler.handler(request))
                else:
                    self.client.close()
                    break


if __name__ == "__main__":            
    s = Serial(4413)
    s.run()