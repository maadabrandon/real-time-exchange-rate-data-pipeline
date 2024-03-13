import os
import socket 
from typing import List, Any 

from dotenv import load_dotenv

from src.prices import Prices

from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage
from polygon.websocket.models.common import Feed, Market


load_dotenv()       
        
polygon_client = WebSocketClient(
        api_key=os.getenv("POLYGON_API_KEY"),
        feed=Feed.RealTime,
        market=Market.Forex,
        subscriptions=["C.GBP/USD"]
)


@staticmethod
def _parse_prices(msg: List[Any]) -> List[Prices]:
    
    raw_prices = msg[1]        
    
    prices = [
        Prices(
            event_type=rate[0],
            pair=rate[1],
            exchange_id=int(rate[2]),
            ask_price=float(rate[3]),
            bid_price=float(rate[4]),
            timestamp=int(rate[5])*1000
        )
        for rate in raw_prices
    ]
    
    return prices
    

def handle_msg(msgs: List[WebSocketMessage]):
    
    for line in msgs:
        
        print(line)
   

try:

    polygon_client.run(handle_msg=handle_msg)
    

except socket.error as error:
    print(f"Websocket connection error: {error}")
