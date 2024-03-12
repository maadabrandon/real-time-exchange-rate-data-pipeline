import os
import socket 
from dotenv import load_dotenv
from typing import List, Any 

from src.rates import Rates

from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage
from polygon.websocket.models.common import Feed, Market


load_dotenv()

class PolygonStream(WebSocketClient):
    
    def __init__(self, api_key, feed, market, subscriptions, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.api_key = api_key
        self.feed = feed
        self.market = market
        self.subscriptions = subscriptions
        
        
    @staticmethod
    def _parse_rates(msg: List[Any]) -> List[Rates]:
        
        raw_rates = msg[1]
        
        rates = [
            Rates(
                event_type=rate[0],
                pair=rate[1],
                exchange_id=int(rate[2]),
                ask_price=float(rate[3]),
                bid_price=float(rate[4]),
                timestamp=int(rate[5])*1000
            )
            for rate in raw_rates
        ]
        
        return rates
    

def handle_msg(msgs: List[WebSocketMessage]):
    
    for line in msgs:
        
        print(line)
   
   
load_dotenv()
try:
    
    polygon_client = PolygonStream(
        api_key=os.getenv("POLYGON_API_KEY"),
        feed=Feed.RealTime,
        market=Market.Forex,
        subscriptions=["C.GBP/USD"]
    )

    polygon_client.run(handle_msg=handle_msg)
    

except socket.error as error:
    print(f"Websocket connection error: {error}")
