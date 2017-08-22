import json
import sys, os, re
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils, OffsetRange, TopicAndPartition

def main():
    try:
        sc and ssc
    except NameError as e:
        import findspark
        # Add the streaming package and initialize
        findspark.add_packages(["org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0"])
        findspark.init()
        import pyspark
        import pyspark.streaming

    PERIOD=10
    BROKERS='localhost:9092'
    TOPIC= 'twitterstream'
    duration=100
    conf = SparkConf().set("spark.default.paralleism", 1)
    sc = SparkContext(appName='Streamer', conf=conf)
    #create a streaming context with batch interval 10 sec
    ssc = StreamingContext(sc, PERIOD)
    #ssc.checkpoint("checkpoint")
    stream = KafkaUtils.createDirectStream(
      ssc,
      [TOPIC],
      {
        "metadata.broker.list": BROKERS,
        "group.id": "0",
      }
    )
    #stream = KafkaUtils.createStream(ssc, 'cdh57-01-node-01.moffatt.me:2181', 'spark-streaming', {TOPIC:1})

    # parsed = stream.map(lambda v: json.loads(v[1]))
    stream.count().map(lambda x:'Tweets in this batch: %s' % x).pprint()

    ssc.start()
    ssc.awaitTermination()

if __name__ == '__main__':
    main()