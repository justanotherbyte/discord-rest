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

from typing import (
    Union, 
    Any,
    Dict
)

from .http import HTTPClient, Route
from .asset import Asset

class User:
    
    _http: HTTPClient

    def __init__(self, data: Dict[str, Any]):
        self.__avatar_hash = data["avatar"]
        self.__avatar_format = "gif" if self.__avatar_hash.startswith("a") else "png"
        self.__avatar_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.__avatar_hash}.{0.__avatar_format}".format(self)

        self.id = int(data["id"])
        self.name = data["username"]
        self.discriminator = int(data["discriminator"])
        self.avatar = Asset(self.__avatar_url)

    async def create_dm(self) -> dict:
        route = Route("POST", "/users/@me/channels")
        payload = {
            "recipient_id": self.id
        }
        data = await self._http.request(route, json = payload)
        return data



    
