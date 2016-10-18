/**
  * @author Yurisues 16-10-17 下午3:36
  */

import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.streaming.kafka._

object WC {
  def main(args:Array[String]): Unit ={
    val conf = new SparkConf().setMaster("local[2]").setAppName("WC")
//    val sc = new SparkContext(conf)
    val ssc = new StreamingContext(conf, Seconds(2))
    val textPath = "hdfs://master:9000/data/"
    val lines = ssc.textFileStream(textPath)
    val lines2 = lines.map(line => line.split("\n"))
    lines.foreachRDD(rdd =>
//      rdd.collect().foreach(test)
      // 保存多个副本到文件夹下，如何需要合并成一个文件，需要rdd.coalesce(1,true).saveAsTextFile()
      rdd.saveAsTextFile("hdfs://master:9000/data/result/")
    )
//    lines2.saveAsTextFile()
//    val text = sc.textFile(textPath)
//    val result = lines.flatMap(_.split("&"))
//    result.co
//    result.foreach(println)
//    val words = text.map(line => line.split("&"))
//    println(words.collect())
//    val wordCounts = words.map(x => (x, 1)).reduceByKey(_ + _)
//    words.print()
    ssc.start()
    ssc.awaitTermination()
//    val text=sc.textFile("hdfs://master:9000/data/machine_user_action.log")
//    val result=text.flatMap(_.split(' ')).map((_,1)).reduceByKey(_+_).collect()
//    result.foreach(println)
  }

  def test(line: String): Unit ={
    println(line)
  }
}