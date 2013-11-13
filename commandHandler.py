import os
import socket

class CommandHandler(object):

    def __init__(self, connection):
        self.CRLF = "\r\n"
        self.connection = connection
        self.pwd = os.getcwd()

    def handler(self, data):
        cmd = data[0:4].strip().upper()
        print data
        options = data[4:-1].strip()

        response = ""
        if cmd == "USER":
            response = "230 Logged in anonymously"
        elif cmd == "PWD":
            response = "247 \"%s\" is the current directory" % self.pwd
        elif cmd == "SYST":
            response = "215 UNIX Working With FTP"
        elif cmd == "CWD":
            if os.path.exists(options):
                self.pwd = options
                response = "250 direcotry changed to %s" % self.pwd
            else:
                response = "550 direcotry not found"
        elif cmd == "PORT":
            parts = options.split(",")
            ip_addr = ".".join(parts[0:4])
            port = int(parts[4]) * 256 + int(parts[5])

            self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.data_socket.connect((ip_addr,port))
            response = "200 Active connection established %s" % port

        elif cmd == "RETR":
            f = open(os.path.join(self.pwd, options), 'r')
            self.connection.respond("125 Data transfer starting %s bytes" % os.fstat(f.fileno()).st_size)

            file_content = f.read()
            self.data_socket.send(file_content)
            self.data_socket.close()
            
        elif cmd == "LIST":
            self.connection.respond("125 Opening data connection for file list")

            result = "\r\n".join(os.listdir(self.pwd))
            self.data_socket.send(result)
            self.data_socket.close()
        else:
            response = "502 Don't know how to respond to %s" % cmd

        return response