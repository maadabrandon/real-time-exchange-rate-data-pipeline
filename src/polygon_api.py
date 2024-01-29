import os
import socket
from typing import List
from dotenv import load_dotenv
from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage
from polygon.websocket.models.common import Feed, Market

load_dotenv()

client = WebSocketClient(
    api_key=os.environ["POLYGON_API_KEY"],
    feed=Feed.RealTime,
    market=Market.Forex,
    subscriptions=["C.GBP/USD"]
)


def handle_msg(msgs: List[WebSocketMessage]):
    
    for line in msgs:
        print(line)


try:
    client.run(handle_msg=handle_msg)

except socket.error as error:
    print(f"Websocket connection error: {error}")

