package com.dream.weather;

import com.dream.example.WordCount;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;

/**
 * 天气数据MR
 * @author Yurisues 16-12-22 下午4:48
 */
public class FirstMR {

    // map类和reduce没有加static修饰，因为Hadoop在调用map和reduce类时采用的反射调用
    public static class Map extends Mapper<LongWritable, Text, Text, IntWritable> {

        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            // key为偏移量
            System.out.println(key);
            context.write(new Text("2016"), new IntWritable(1));
        }
    }

    public static class Reduce extends Reducer<Text, IntWritable, Text, IntWritable> {

        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            for (IntWritable val : values) {
                context.write(new Text("2016"), new IntWritable(1));
            }
        }
    }

    public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
        if (args.length != 2) {
            System.err.println("Usage: FirstMR <input> <output>");
            System.exit(-1);
        }
        Path inputPath = new Path(args[0]);
        Path outPath = new Path(args[1]);
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "FirstMR");
        job.setJarByClass(FirstMR.class);
        job.setMapperClass(Map.class);
        job.setReducerClass(Reduce.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, inputPath);
        FileOutputFormat.setOutputPath(job, outPath);
        // 判断outPath是否存在，如存在则先删除，否则报错
        FileSystem fs = FileSystem.getLocal(conf);
        if (fs.exists(outPath)) {
            fs.delete(outPath, true);
        }
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
