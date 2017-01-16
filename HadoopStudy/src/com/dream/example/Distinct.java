package com.dream.example;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;
import java.util.StringTokenizer;

/**
 * 数据去重。根据输入文件，输出去重后的数据。
 * map：输出键值对
 * reduce:输入为键，值为map的对应键的值列表
 * @author Yurisues 16-12-19 下午2:50
 */
public class Distinct {
    public static class Map extends Mapper<Object, Text, Text, Text> {
        private static Text line = new Text();
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException{
            StringTokenizer itr = new StringTokenizer(value.toString(), " ");
            String id = itr.nextToken();
            String name = itr.nextToken();
            line = value;
            // 直接将值作为key
            context.write(new Text(id), line);
        }
    }

    public static class Reduce extends Reducer<Text, Text, Text, Text> {
        private static Text data = new Text("");
        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException{
            // reduce阶段， values值都为空，key就是原来的行数据
            for (Text value : values) {
                data = value;
                break;
            }
            // 最后写入文件的是key+value，此处即data
            context.write(data, new Text(""));
        }
    }

    public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
        if(args.length != 2){
            System.out.println("Usage: Distinct <input path> <out path>");
            System.exit(-1);
        }
        String inputPath = args[0];
        String outPath = args[1];
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Distinct");
        job.setJarByClass(Distinct.class);
        job.setMapperClass(Map.class);
        job.setReducerClass(Reduce.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        FileInputFormat.addInputPath(job, new Path(inputPath));
        FileOutputFormat.setOutputPath(job, new Path(outPath));
        System.exit(job.waitForCompletion(true) ? 0:1);
    }
}
