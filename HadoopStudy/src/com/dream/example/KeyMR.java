package com.dream.example;

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
import java.util.StringTokenizer;

/**
 * 测试Mapper KEY_IN
 * @author Yurisues 16-12-15 下午2:24
 */


public class KeyMR {

    public static class Map extends Mapper<LongWritable, Text, Text, Text> {

        public void map(LongWritable key, Text value, Context context ) throws IOException, InterruptedException {
            // 文件偏移亮，对文本文件，一个英文字符占1位，一个中文占4位
            long offset = key.get();
            System.out.println(offset);
            context.write(new Text(offset + ""), value);
        }
    }

    public static class Reduce extends Reducer<Text, Text, Text, Text> {

        public void reduce(Text key, Iterable<Text> values, Context context ) throws IOException, InterruptedException {
            for (Text val : values) {
                context.write(key, val);
            }
        }
    }

    public static void main(String[] args) throws Exception {
        // 默认路径为hdfs路径，input对应的为hdfs://master:9000/data/input
        // 提交执行：hadoop jar HadoopStudy.jar com.dream.test.WordCount /data/input /data/out

        if(args.length != 2) {
            System.err.println("Usage: KeyMR <input> <output>");
            System.exit(-1);
        }
        Path inputPath = new Path(args[0]);
        Path outPath = new Path(args[1]);

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "KeyMR");
        job.setJarByClass(KeyMR.class);
        job.setMapperClass(Map.class);
        job.setReducerClass(Reduce.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        FileInputFormat.addInputPath(job, inputPath);
        FileOutputFormat.setOutputPath(job, outPath);
        // 判断outPath是否存在，如存在则先删除，否则报错
        FileSystem fs = FileSystem.getLocal(conf);
        if(fs.exists(outPath)) {
            fs.delete(outPath, true);
        }
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}