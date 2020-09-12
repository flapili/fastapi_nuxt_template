# coding: utf-8
import logging
import time
import typing

from starlette.types import ASGIApp, Receive, Scope, Send


class LogAccessMiddleware:
    def __init__(self, app: ASGIApp, logger_name: str = "uvicorn.access") -> None:
        self.app = app
        self.access_logger = logging.getLogger(logger_name)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] in ["http", "websocket"]:
            from pprint import pprint
            pprint(scope)

            headers: typing.Dict[bytes, bytes] = dict(scope["headers"])

            try:
                real_ip: str = headers[b"x-real-ip"].decode("ascii")
                print(real_ip)
            except KeyError:
                logging.getLogger(__name__).warning("x-real-ip header is missing")
            
            
        return await self.app(scope, receive, send)