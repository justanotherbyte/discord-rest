from __future__ import annotations

import asyncio
import json
from typing import (
    Optional,
    Any, 
    Union,
    TYPE_CHECKING
)

import aiohttp


class Route:
    BASE = "https://discord.com/api/v9"
    def __init__(self, method: str, endpoint: str, **params):
        self.method = method
        self.endpoint = endpoint
        self.url = self.BASE + endpoint.format(**params)


async def parse_response(response: aiohttp.ClientResponse) -> Union[str, dict]:
    headers = response.headers()
    try:
        if headers["Content-Type"] == "application/json":
            return await response.json()
    except KeyError:
        # Thanks Cloudflare
        pass

    text = await response.text(encoding='utf-8')
    return text


class HTTPClient:
    def __init__(
        self,
        *,
        loop: Optional[asyncio.AbstractEventLoop] = None
    ):  
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.__session: Optional[aiohttp.ClientSession] = None # filled in later
        self.token: Optional[str] = None


    async def http_connect(self) -> Optional[aiohttp.ClientSession]:
        if self.__session is None or self.__session.closed is True:
            session = aiohttp.ClientSession()
            self.__session = session
            return session

        return None

    async def request(self, route: Route, **kwargs) -> Any:
        method = route.method
        url = route.url
        token = self.token

        if token is None:
            raise ValueError("Token in HTTPClient is None")

        headers = {} # headers creation

        headers["Authorization"] = "Bot {}".format(token)

        kwargs["headers"] = headers

        async with self.__session.request(method, url **kwargs) as resp:
            data = await parse_response(resp)

        if 300 > resp.status >= 200:
            return data

        raise OSError("hey something messed up http wise, this is a temp error will be replaced with http exception later :)")