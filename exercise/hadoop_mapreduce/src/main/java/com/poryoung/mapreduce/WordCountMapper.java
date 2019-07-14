package com.poryoung.mapreduce;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class WordCountMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    @Override
    /**
     * @Author: Administrator
     * @Description: TODO
     * @Date: 11:49 2019/7/8
     * @param key
     * @param value
     * @param context
     * @return: void
     * @throw
     */
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString();
        String[] words = line.split(" ");
        for (int i = 0; i < words.length; i++) {
            context.write(new Text(words[i]), new IntWritable(1));
        }
    }
}
