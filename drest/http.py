"""
MIT License

Copyright (c) 2021 Vish M

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

import asyncio
import json
from typing import (
    Optional,
    Any, 
    Union,
    Dict,
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
    headers = response.headers
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
        self.application_id: Optional[int] = None


    def recreate(self) -> Optional[aiohttp.ClientSession]:
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
        print(kwargs)
        print(type(kwargs))

        self.recreate()

        async with self.__session.request(method, url, **kwargs) as resp:
            data = await parse_response(resp)

            if 300 > resp.status >= 200:
                return data

        raise OSError(f"hey something messed up http wise, this is a temp error will be replaced with http exception later :) {data}")


    def register_slash_command(self, name: str, description: str, type: int, *, guild_id: Optional[int] = None) -> asyncio.Future:
        if guild_id:
            endpoint = "/applications/{application_id}/guilds/{guild_id}/commands"
            route = Route("POST", endpoint, application_id = self.application_id, guild_id = guild_id)
        else:
            endpoint = "/applications/{application_id}/commands"
            route = Route("POST", endpoint, application_id = self.application_id)

        payload: Dict[str, Any] = {
            "name": name,
            "description": description,
            "type": type
        }

        return self.request(route, json = payload)


    async def read_url(self, url: str) -> bytes:
        async with self.__session.get(url) as resp:
            return await resp.read()

        