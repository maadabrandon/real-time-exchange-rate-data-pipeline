import os
from dotenv import load_dotenv

from loguru import logger

from src.feed import polygon_client
from src.producer_wrapper import ProducerWrapper


load_dotenv()

USE_LOCAL_KAFKA = True if os.getenv("USE_LOCAL_KAFKA") is not None else False
KAFKA_OUTPUT_TOPIC = os.getenv("KAFKA_OUTPUT_TOPIC")


def run():
          
    with ProducerWrapper(kafka_topic=KAFKA_OUTPUT_TOPIC, use_local_kafka=USE_LOCAL_KAFKA) as producer:
    
        while True:

            prices = polygon_client.feed()

            if not prices:

                continue 

            logger.info("Got prices from the Polygon API")

            for price in prices:

                producer.produce(
                    key=prices
                )
