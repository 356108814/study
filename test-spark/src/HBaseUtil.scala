import org.apache.hadoop.hbase.HBaseConfiguration
import org.apache.hadoop.hbase.client.Put
import org.apache.hadoop.hbase.io.ImmutableBytesWritable
import org.apache.hadoop.hbase.mapred.TableOutputFormat
import org.apache.hadoop.hbase.util.Bytes
import org.apache.hadoop.mapred.JobConf
import org.apache.spark.{SparkConf, SparkContext}

/**
 * Created by dream on 16-10-18.
 */
class HBaseUtil {
    def main(args: Array[String]): Unit = {
        //创建jobConf
        val conf = HBaseConfiguration.create()
        val jobConf = new JobConf(conf)
        jobConf.setOutputFormat(classOf[TableOutputFormat])
        jobConf.set(TableOutputFormat.OUTPUT_TABLE,"test")

        //创建hiveContext
        val sparkConf = new SparkConf().setAppName("test")
        val sc = new SparkContext(sparkConf)
        @transient  val sqlContext = new org.apache.spark.sql.hive.HiveContext(sc)
        sqlContext.setConf("spark.sql.shuffle.partitions","3")

        //保存到hbase
        val rdd = sqlContext.sql("select C1,C2,C3 from test")
        .map(row => {
            val c1 = row(0).asInstanceOf[String]
            val c2 = row(1).asInstanceOf[String]
            val c3 = row(2).asInstanceOf[String]
            val p = new Put(Bytes.toBytes(c1))
            p.add(Bytes.toBytes("f"), Bytes.toBytes("c2"), Bytes.toBytes(c2))
            p.add(Bytes.toBytes("f"), Bytes.toBytes("c3"), Bytes.toBytes(c3))
            (new ImmutableBytesWritable,p)
        }).saveAsHadoopDataset(jobConf)
    }
}
