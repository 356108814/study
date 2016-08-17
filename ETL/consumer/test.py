# encoding: utf-8

import re
from kafka import SimpleClient,SimpleConsumer,KafkaConsumer


def testpythonkafka():
    """
    python-kafka
    :return:
    """
    consumer = KafkaConsumer('aimeipay', group_id='python-consumer-group', bootstrap_servers=['172.16.2.102:9092'])
    for message in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        topic = message.topic
        partition = message.partition
        offset = message.offset
        key = message.value.decode('utf-8')
        value = message.value.decode('utf-8')
        # print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value.decode('utf-8')))
        # 开始清洗
        # aimei_rsp_time=20160324114509&mid=255&sequeid=255_1458791086&rsp_code=0&rsp_msg=msg ok&aimei_pay_no=P20160324114446_1_0_255&pay_type=1&amount=1500&expense_time=6&product=1
        value_dict = {}
        list1 = value.split('&')
        for _, v in enumerate(list1):
            list2 = v.split('=')
            key = list2[0]
            value = list2[1]
            value_dict[key] = value



def testpykafka():
    """
    pykafka
    :return:
    """
    from pykafka import KafkaClient

    client = KafkaClient(hosts="172.16.2.102:9092")
    topic_list = client.topics
    print client.topics
    topic = topic_list['aimeipay']
    print topic
    # 持续监听消费。不维护offset，消费完以后，不会再监听到。只会监听到新的消息
    consumer = topic.get_simple_consumer('python-consumer-group')
    for message in consumer:
        if message is not None:
            print message.offset, message.value


if __name__ == '__main__':
    # testpythonkafka()
    testpykafka()