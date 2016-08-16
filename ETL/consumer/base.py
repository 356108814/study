# encoding: utf-8

from kafka import KafkaConsumer


class Consumer(object):
    """
    消费者基类，只针对kafka
    """
    def __init__(self, topics, group_id, bootstrap_servers):
        """
        初始化
        :param topics: 消息类别
        :param group_id: 消费组
        :param bootstrap_servers: 服务器列表
        :return:
        """
        self.kafka_consumer = KafkaConsumer(topics, group_id=group_id, bootstrap_servers=bootstrap_servers)

    def handle(self):
        """
        处理
        :return:
        """
        for message in self.kafka_consumer:
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            topic = message.topic
            partition = message.partition
            offset = message.offset
            key = message.value.decode('utf-8')
            value = message.value.decode('utf-8')

    def close(self):
        """
        关闭消费连接
        :return:
        """
        self.kafka_consumer.close()


if __name__ == '__main__':
    pass
