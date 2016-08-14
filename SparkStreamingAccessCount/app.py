# park Application - execute with spark-submit：
# spark-submit app.py
## Imports
from pyspark import SparkConf, SparkContext

## Module Constants
APP_NAME = "SparkStreamingAccessCount"

## Closure Functions

## Main functionality

def main(sc):
    pass

if __name__ == "__main__":
    # Configure Spark
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)

    # Execute Main functionality
    main(sc)
