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

from typing import (
    Dict,
    Optional
)

from aiohttp import web, web_request

from .security import verify_request


class RESTServer:
    def __init__(
        self,
        public_key: str
    ):
        self.app = web.Application()
        self.public_key: str = public_key
        
        self._guild_cache: Dict[str, Optional[str]] = {}

        self.register_routes()


    async def handle_interaction_receive(self, request: web_request.Request):
        body = await request.text()
        secure = verify_request(self.public_key, request, body)
        if not secure:
            return web.Response(text = "invalid request signature", status = 401)

        # handle request
        json = await request.json()
        print(json)
        pong = {
            "type": 1
        }
        response = web.json_response(pong, status = 200)
        return response

    def register_routes(self) -> list:
        routes = [
            web.post("/api/interactions", self.handle_interaction_receive)
        ]
        self.app.add_routes(routes)
        return routes
