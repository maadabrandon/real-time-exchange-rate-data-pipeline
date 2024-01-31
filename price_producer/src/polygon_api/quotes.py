import json
from pydantic import BaseModel
from typing import Optional, List, Dict

class Quote(BaseModel):
    
    event_type: str
    pair: List[str] 
    exchange_id: int
    ask_price: float
    bid_price: float
    timestamp: int
    
    def to_str(self):
        
        """ Returns a string representation of the Quotes object """
        
        return json.dumps(self.model_dump())
        
        
    def to_dict(self) -> Dict[str, any]:
        
        """ Turn the returned Quotes object to a dictionary """
        
        return {
            "event_type": self.event_type,
            "pair": self.pair, 
            "ask_price": self.ask_price,
            "bid_price": self.bid_price, 
            "timestamp": self.timestamp
        }
    