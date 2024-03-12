import os
import json
from typing import Optional

from loguru import logger
from quixstreams.kafka import Producer
from quixstreams.platforms.quix import QuixKafkaConfigsBuilder, TopicCreationConfigs


class ProducerWrapper:

    """ 
    This is just a wrapper around the quixstreams.kafka.Producer class which provides 
    logic for two scenarios:

    - a local Kafka cluster
    - a Quix Kafka cluster.
    """
    
    def __init__(
            self,
            kafka_topic: str,
            use_local_kafka: Optional[bool] = False
    ):

        """
        After initialising the Kafka topic, we go on to initialise the Producer 
        object depending on which of the above scenarios we're going with.
        """

        self._kafka_topic = kafka_topic
        self._producer = None

        if use_local_kafka:

            logger.info("Connecting to the Local Kafka cluster")

            # Connect to a local Kafka cluster
            self._producer = Producer(
                broker_address=os.getenv("KAFKA_BROKER"),
                extra_config={"allow.auto.create.topics": "true"}
                )
        
        else:

            logger.info("Connecting to Quix Kafka cluster")

            # Connect to a Quix Kafka cluster
            topic = kafka_topic
            cfg_builder = QuixKafkaConfigsBuilder()
            cfgs, topics, _ = cfg_builder.get_confluent_client_configs([topic])
            topic = topics[0]

            self._kafka_topic = topic

            cfg_builder.create_topics(
                [TopicCreationConfigs(name=topic)]
            )

            self._producer = Producer(
                broker_address=cfgs.pop("bootstrap.servers"),
                extra_config=cfgs
            )

    def produce(
            self,
            key,
            value: dict[str, any],
            headers=None,
            partition=None,
            timestamp=None
    ):
        self._producer.produce(
            topic=self._kafka_topic,
            headers=headers,
            key=key,
            value=json.dumps(value)
        )

    def __enter__(self):
        return self 

    def __exit__(self, exc_type, exc_value, traceback):

        self._producer.__exit__(exc_type, exc_value, traceback)
