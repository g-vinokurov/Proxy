# -*- coding: utf-8 -*-

import sys
import socket
import select


class ProxyServer:
    def __init__(self, host: str, port: int):
        self.__host = host
        self.__port = port

        self.__runnable = False

    def __enter__(self):
        self.__main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__main_socket.bind((self.__host, self.__port))
        self.__main_socket.listen()
        self.__main_socket.setblocking(False)

        self.__all_sockets = [self.__main_socket]

        self.__runnable = True

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for __socket in self.__all_sockets:
            __socket.close()
        self.__runnable = False

    def run(self):
        if not self.__runnable:
            raise RuntimeError('You have to create server using with-statement')

        while True:
            readable_sockets = select.select(self.__all_sockets, [], [])[0]

            for __socket in readable_sockets:
                if __socket == self.__main_socket:
                    client_socket, addr = self.__main_socket.accept()
                    client_socket.setblocking(False)
                    self.__all_sockets.append(client_socket)
                else:
                    pass


if __name__ == '__main__':

    with ProxyServer('127.0.0.1', int(sys.argv[1])) as server:
        server.run()
