#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
 Counts words in UTF8 encoded, '\n' delimited text received from the network every second.
 Usage: kafka_wordcount.py <zk> <topic>

 To run this on your local machine, you need to setup Kafka and create a producer first, see
 http://kafka.apache.org/documentation.html#quickstart

 and then run the example
    `$ bin/spark-submit --jars \
      external/kafka-assembly/target/scala-*/spark-streaming-kafka-assembly-*.jar \
      examples/src/main/python/streaming/kafka_wordcount.py \
      localhost:2181 test`

      bin/spark-submit --jars external/kafka-assembly/spark-streaming-kafka-0-10-assembly_2.10-2.0.0.jar /RTCS/minik_weixin_user_action.py 172.16.2.101:2181 minik_weixin_user_action
"""
from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


def parse_line(line):
    print(line)
    # index = line.find(']')
    # line = (line[index+1:]).strip()
    # data = self.parser.split_k_v(line)
    # column_value = {
    #     'uid': data['uid'],
    #     'p_type': Product.MINIK.value,
    #     't_type': Terminal.Mobile.value,
    #     'a_type': -1,
    #     'action_time': -1,
    #     'location': -1,
    #     'aimei_object': '',
    #     'update_time': -1
    # }
    # action = data['action']
    # if action == 'click_listen_song':
    #     column_value['a_type'] = Action.REQUEST_SONG.value
    #     column_value['aimei_object'] = data['songid']
    # else:
    #     column_value['a_type'] = Action.CLICK_BUTTON.value
    #     aimei_object = ''
    #     if action == 'click_tab':
    #         aimei_object = data['tab']
    #     elif action == 'visit_url':
    #         aimei_object = data['url']
    #     elif action == 'click_play_album':
    #         aimei_object = data['albumid']
    #     column_value['aimei_object'] = aimei_object
    # column_value['action_time'] = DateUtil.date2timestamp(data['timestamp'], fmt='%Y-%m-%d_%H:%M:%S')


def insert(column_value):
    print(column_value)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: kafka_wordcount.py <zk> <topic>", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="minik_weixin_user_action")
    ssc = StreamingContext(sc, 1)

    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "python-etl-group", {topic: 1})
    lines = kvs.map(lambda x: x[1])
    counts = lines.flatMap(parse_line) \
        .map(insert)
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()
