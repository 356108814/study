package com.dream.weather;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;

/**
 * 最高气温MR
 * @author Yurisues 16-12-22 下午4:48
 */
public class MaxMR {

    // map类和reduce没有加static修饰，因为Hadoop在调用map和reduce类时采用的反射调用
    public static class Map extends Mapper<LongWritable, Text, Text, FloatWritable> {

        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            // key为偏移量
//            System.out.println(key);
            String line = value.toString();
            if(!line.contains("STN")) {
                String year = line.substring(14, 18);
                float temp = Float.parseFloat(line.substring(26, 30)); //气温
//                System.out.println(temp);
                context.write(new Text(year), new FloatWritable(temp));
            }
        }
    }

    public static class Reduce extends Reducer<Text, FloatWritable, Text, FloatWritable> {

        public void reduce(Text key, Iterable<FloatWritable> values, Context context) throws IOException, InterruptedException {
            float max = 0;
            for (FloatWritable val : values) {
                max = Math.max(max, val.get());
            }
            context.write(key, new FloatWritable(max));
        }
    }

    public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
        if (args.length != 2) {
            System.err.println("Usage: MaxMR <input> <output>");
            System.exit(-1);
        }
        Path inputPath = new Path(args[0]);
        Path outPath = new Path(args[1]);
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "MaxMR");
        job.setJarByClass(MaxMR.class);
        job.setMapperClass(Map.class);
        job.setReducerClass(Reduce.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(FloatWritable.class);
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
