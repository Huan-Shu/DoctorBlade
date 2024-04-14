# Author:           Markus Kirchner
# Date:             2024-03-19
# Last modified:    2024-03-19

from socket import *


class TCPIP_TO_RS232_DEVICE_CLASS (socket):
    def __init__(self, host, port, buffer_size=1024, send_termination_character="\r\n", receive_termination_character="\r\n"):
        super().__init__(AF_INET, SOCK_STREAM, 0, None)
        self.connected = False
        super_connect = self.connect
        super_send = self.send
        super_close = self.close
        super_recv = self.recv
        def open_connection():
            super_connect((host,port))
            self.connected = True
        def close_connection():
            super_close()
            self.connected = False
        def send_msg(msg):
            msg = "".join([msg,send_termination_character])
            super_send(msg.encode())
        def recv_msg():
            tmp = super_recv(buffer_size).decode().replace(receive_termination_character,"")
            return tmp # remove "\r\n" from the end of string


        
        self.connect = open_connection #customize socket's connect function
        self.close = close_connection
        self.send = send_msg
        self.recv = recv_msg

    