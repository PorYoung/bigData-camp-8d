package com.poryoung.mapreduce;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

/**
 * Main
 */
public class Main {

    public static void main(String[] args) throws Exception {
        Configuration configuration = new Configuration();
        // 1.创建一个job和任务入口
        Job job = Job.getInstance(configuration);
        job.setJarByClass(Main.class); // main方法所在的class

        // 2.指定job的mapper和输出的类型<k2 v2>
        job.setMapperClass(CleanMapper.class);// 指定Mapper类
        job.setMapOutputKeyClass(NullWritable.class); // k2的类型
        job.setMapOutputValueClass(Text.class); // v2的类型

        // 3.指定job的reducer和输出的类型<k4 v4>
        job.setReducerClass(ReduceMapper.class);// 指定Reducer类
        job.setOutputKeyClass(NullWritable.class); // k4的类型
        job.setOutputValueClass(Text.class); // v4的类型

        // 4.指定job的输入和输出
        FileInputFormat.setInputPaths(job, new Path("hdfs://master:9000/input/zhilian.csv"));
        FileOutputFormat.setOutputPath(job, new Path("hdfs://master:9000/output/zhilian/"));
        // FileInputFormat.setInputPaths(job, new
        // Path("hdfs://master:9000/input/test2"));
        // FileOutputFormat.setOutputPath(job, new
        // Path("hdfs://master:9000/output/test2"));
        new Path("hdfs://master:9000/").getFileSystem(configuration)
                .delete(new Path("hdfs://master:9000/output/zhilian/"));
        // new Path("hdfs://master:9000/").getFileSystem(configuration)
        // .delete(new Path("hdfs://master:9000/output/test2/"));
        // 5.执行job
        job.waitForCompletion(true);
        System.out.print(job.waitForCompletion(true) ? '0' : '1');
    }
}