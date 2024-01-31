import os
import socket
from dotenv import load_dotenv
from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage
from typing import Optional, List, Dict, Union, Any 
from polygon.websocket.models.common import Feed, Market

from src.polygon_api.quotes import Quote


load_dotenv()

class PolygonQuotesAPI(WebSocketClient):
    
    def __init__(self, api_key, feed, market, subscriptions, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.api_key = api_key
        self.feed = feed
        self.market = market
        self.subscriptions = subscriptions
        
        
    @staticmethod
    def _parse_quotes(msg: List[Any]) -> List[Quote]:
        
        raw_quotes = msg[1]
        quotes = [
            Quote(
                event_type=quote[0],
                pair=quote[1],
                exchange_id=int(quote[2]),
                ask_price=float(quote[3]),
                bid_price=float(quote[4]),
                timestamp=int(quote[5])*1000
            )
            for quote in raw_quotes
        ]
        
        return quotes
    

def handle_msg(msgs: List[WebSocketMessage]):
    
    for line in msgs:
        print(line)
   
   
try:
    client.run(handle_msg=handle_msg)

except socket.error as error:
    print(f"Websocket connection error: {error}")
