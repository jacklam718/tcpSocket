#!/usr/bin/env python
# --*--coding: utf-8 --*--

from socket import * 
from threading import Thread

class basicTCP: 
    running     = True 
    has_connect = False 
    def __init__(self, server_address=address, buffersize=8192): 
        self.server_address = server_address
        self.buffersize     = buffersize

    def createSocket(self): 
        self.socket = socket(AF_INET, SOCK_STREAM) 
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind( self.server_address )  
        self.socket.listen( 5 )

    def receiver(self): 
        data = "" 
        try: 
            while True:
                buffer = self.socket.recv( self.buffersize )
                data += buffer 
                if '\e' in buffer:  
                    break      
            return data 

        except error as err:  
            self.close_( )

    def sender(self, data): 
        try: 
            self.socket.send(data)
        except error as err:
            return err  

    def close_(self): 
        self.has_connect = False 
        self.socket.close( )


class TCPSocketServer(basicTCP): 
    """ 
    the TCPServerConnection as a TCP server provide basic function.  
    """ 
    def __init__(self, server_address=address, buffersize=8192): 
        basicTCP.__init__(self, server_address, buffersize)
        self.server_address = server_address 
        self.buffersize     = buffersize
        
    def __listen__(self):
        try: 
            self.createSocket( ) 
            self.socket, self.address = self.socket.accept( )
            self.has_connect = True 
            print(self.socket.getpeername( ))
        except error as err:
            return err

    def __listener__(self, handler): 
        """ 
        this is a listener, when have connection request would be 
        accept and then use the handler method to handle the connection, 
        you needed to write your own "handler" function.  
        """
        self.createSocket( ) 
        while self.running: 
            sockObj, address = self.socket.accept( ) 
            self.has_connect = True 
            t = Thread(target=handler, args=( sockObj, ))
        self.close_( ) 

    def listen(self): 
        """ 
        This mothod  implement multithread listen, make it does not 
        block other operats 
        """   
        self.t = Thread(target=self.__listen__)
        self.t.setDaemon(True) 
        self.t.start( )
        self.t.join( 0.5 ) 

    def listener(self, handler):
        """ 
        This mothod multithreaded implement multithread listener, 
        make it does not block other operats 
        """   
        self.t = Thread(target=self.__listener__, args=( handler, )) 
        self.t.setDaemon(True) 
        self.t.start( )
        self.t.join( 0.5 )


class TCPClientConnection(basicTCP): 
    """ 
    the TCPClientConnection as a client side for connect to TCP Server.
    """
    def __init__(self, server_address, buffersize=8192): 
        basicTCP.__init__(self, server_address, buffersize) 
        self.server_address = server_address

    def connectTo(self): 
        try: 
            self.createSocket( )
            self.socket.connect( self.server_address )
            self.has_connect = True 
            return True
        except error as err: 
            self.close_( )

    def createSocket(self): 
        self.socket = socket( AF_INET, SOCK_STREAM )
        self.socket.setsockopt( SOL_SOCKET, SO_REUSEADDR, 1 )

if __name__ == '__main__': 
    import sys 
    if len(sys.argv) > 1: 
        port = sys.argv[1] 
        address = (getIP( ), int(port))
    print('[*] Listening....', s.server_address) 
    s = TCPSocketServer(address)
    s.listen( )
