from aiohttp import web
import json
import time

class Server():
    """

    Class containing all the custom log for the websocket server

    """

    @staticmethod
    def get_timestamp():
        """

        Returns the current unix timestamp of the server

        :return: current unix timestamp of the server
        :rtype: int

        """
        return int(time.time())


    def get_event(self, c):
        """

        Creates a JSON string containing the message count and the current timestamp

        :param c: The message count
        :type c: int
        :return: A JSON string containing the message count and the current timestamp
        :rtype: string

        """

        return json.dumps({"c": c, "ts": self.get_timestamp()})


    async def notify(self, ws, c):
        """

        Send a connected client an event JSON string

        :param ws: The connection to the websocket client
        :type ws: aiohttp.web.WebSocketResponse
        :param c: The message count
        :type c: int
        :return: void

        """
        message = self.get_event(c)
        await ws.send_str(message)

    async def wshandle(self, request):
        """

        Callback function triggered once per connected client.
        Sends initial timestamp and asynchronously awaits for incoming messages

        :param request: Information on the client trying to connect
        :return: ws
        :rtype: aiohttp.web.WebSocketResponse

        """
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        # send newly connected client initial timestamp
        await self.notify(ws, 0)

        # incoming message event
        async for msg in ws:
            if msg.type == web.WSMsgType.text:

                # decode incoming message into an associative array
                data = json.loads(msg.data)

                # notify client with event for message with count "c"
                await self.notify(ws, data['c'])
            elif msg.type == web.WSMsgType.close:
                break

        return ws

"""

Initializes the websocket server
Sets the callback function, host, and port,
as well as starts the loop the server runs in

"""
server = Server()
app = web.Application()
app.add_routes([web.get('/', server.wshandle)])

web.run_app(app)