# coding: utf-8

import socketserver
import pickle
import struct
import logging
import threading


logging.basicConfig(
    format="%(name)-15s %(levelname)-8s %(message)s", level=logging.DEBUG
)



class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    def handle(self):
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break

            slen = struct.unpack(">L", chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk += self.connection.recv(slen - len(chunk))

            obj = pickle.loads(chunk)

            record = logging.makeLogRecord(obj)
            logger = logging.getLogger(record.name)

            if logger.isEnabledFor(record.levelno):
                logger.handle(record)


TCP_server = socketserver.ThreadingTCPServer(("0.0.0.0", 9020), LogRecordStreamHandler)

TCP_server.serve_forever()
