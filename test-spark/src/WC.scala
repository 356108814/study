/**
  * @author Yurisues 16-10-17 下午3:36
  */

import org.apache.spark.{SparkContext,SparkConf}

object WC {
  def main(args:Array[String]): Unit ={
    val conf = new SparkConf().setMaster("local[2]").setAppName("WC")
    val sc=new SparkContext(conf)
    val text=sc.textFile("hdfs://master:9000/data/machine_user_action.log")
    val result=text.flatMap(_.split(' ')).map((_,1)).reduceByKey(_+_).collect()
    result.foreach(println)
  }
}