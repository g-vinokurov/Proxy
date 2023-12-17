# -*- coding: utf-8 -*-

import sys
import socket
import select


class ProxyServer:
    def __init__(self, host: str, port: int):

        self.__main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__main_socket.bind((host, port))
        self.__main_socket.listen()
        self.__main_socket.setblocking(False)

        self.__dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # ... dns-settings

        self.__all_sockets = [self.__main_socket]

    def run(self):
        while True:
            readable_sockets = select.select(self.__all_sockets, [], [])[0]

            for __socket in readable_sockets:
                if __socket == self.__main_socket:
                    client_socket, addr = self.__main_socket.accept()
                    client_socket.setblocking(False)
                    self.__all_sockets.append(client_socket)
                elif __socket == self.__dns_socket:
                    self.__handle_dns_socket()
                else:
                    self.__handle_client_socket(__socket)

    def __handle_client_socket(self, __socket):
        pass

    def __handle_dns_socket(self):
        pass


if __name__ == '__main__':
    ProxyServer('127.0.0.1', int(sys.argv[1])).run()
