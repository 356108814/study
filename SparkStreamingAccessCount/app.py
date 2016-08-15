# park Application - execute with spark-submit：
# spark-submit app.py
## Imports
import time
import re
from pyspark import SparkConf, SparkContext

## Module Constants
APP_NAME = "SparkStreamingAccessCount"

## Closure Functions

def parse(line):
    reg = re.compile('(?P<ip>.*) - - (?P<date>.*) "(?P<method>.*) (?P<uri>.*) (?P<version>.*)" (?P<status>.*) (?P<content_length>.*) "(?P<referer>.*)" "(?P<user_agent>.*)" (?P<request_time>.*)ms')
    match = reg.match(line)
    if not match:
        print(line)
    groupdict = match.groupdict()
    groupdict['uri'] = groupdict['uri'].split('?')[0]    # 去掉参数
    return groupdict


## Main functionality

def main(sc):
    start_time = time.time()
    textFile = sc.textFile('./data/access.log')
    rdd = textFile.map(parse)    # PyrhonRDD对象
    result = rdd.collect()    # 解析结果数组，每个元素为parse返回值
    with open('dictdata', 'w+') as f:
        f.writelines(str(result))
        print('处理完成:%s' % (time.time() - start_time))

if __name__ == "__main__":
    # Configure Spark
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)

    # Execute Main functionality
    main(sc)
