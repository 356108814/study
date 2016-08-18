# encoding: utf-8

from kafka import KafkaConsumer


class Consumer(object):
    """
    消费者基类，只针对kafka
    """

    def __init__(self, topics, group_id, bootstrap_servers):
        """
        初始化。默认消费最近的数据，offset自动提交
        :param topics: 消息类别
        :param group_id: 消费组
        :param bootstrap_servers: 服务器列表
        :return:
        """
        # auto_offset_reset='earliest'
        # enable_auto_commit=False，默认为True，自动保存offset
        self.kafka_consumer = KafkaConsumer(topics, group_id=group_id, bootstrap_servers=bootstrap_servers,
                                            auto_offset_reset='earliest', enable_auto_commit=False)

    def handle(self):
        topics = self.kafka_consumer.topics()
        print('topics:%s' % topics)
        for message in self.kafka_consumer:
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            topic = message.topic
            partition = message.partition
            offset = message.offset
            key = message.value.decode('utf-8')
            value = message.value.decode('utf-8')
            # print("%s:%d:%d: key=%s value=%s" % (topic, partition, offset, key, value))
            if value:
                self.consume(value)

    def consume(self, line_data):
        print("value:%s" % line_data)

    def close(self):
        self.kafka_consumer.close()


if __name__ == '__main__':
    consumer = Consumer('minik_weixin_user_action', 'python-etl-group', ['172.16.3.222:9092'])
    consumer.handle()
