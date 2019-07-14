package com.poryoung.mapreduce;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCountDreiver {
    public static void main(String[] args) throws Exception {
        Configuration configuration = new Configuration();
        
        // 1.创建一个job和任务入口
        Job job = Job.getInstance(configuration);
        job.setJarByClass(WordCountDreiver.class); // main方法所在的class

        // 2.指定job的mapper和输出的类型<k2 v2>
        job.setMapperClass(WordCountMapper.class);// 指定Mapper类
        job.setMapOutputKeyClass(Text.class); // k2的类型
        job.setMapOutputValueClass(IntWritable.class); // v2的类型

        // 3.指定job的reducer和输出的类型<k4 v4>
        job.setReducerClass(WordCountReducer.class);// 指定Reducer类
        job.setOutputKeyClass(Text.class); // k4的类型
        job.setOutputValueClass(IntWritable.class); // v4的类型

        // 4.指定job的输入和输出
        FileInputFormat.setInputPaths(job, new Path("hdfs://master:9000/input/test"));
        FileOutputFormat.setOutputPath(job, new Path("hdfs://master:9000/output/"));

        // 5.执行job
        job.waitForCompletion(true);
        System.out.print(job.waitForCompletion(true) ? '0' : '1');
    }
}