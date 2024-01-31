import os
import logging
from src.utils import initialise_logger, load_env_variables
from src.polygon_api.api import PolygonQuotesAPI
from src.polygon_api.quotes import Quotes
from src.producer_wrapper import ProducerWrapper

logger = logging.getLogger()
load_env_variables()

USE_LOCAL_KAFKA = True if os.environ.get("use_local_kafka") is not None else False
#KAFKA_OUTPUT_TOPIC = os.environ["output"]


def run():
    
    polygon_client = PolygonQuotesAPI(
        api_key=os.environ["POLYGON_API_KEY"],
        feed=Feed.RealTime,
        market=Market.Forex,
        subscriptions=["C.GBP/USD"]
    )
    
    #with ProducerWrapper(kafka_topic=KAFKA_OUTPUT_TOPIC, use_local_kafka=USE_LOCAL_KAFKA) as producer:
        
        
            
    
    