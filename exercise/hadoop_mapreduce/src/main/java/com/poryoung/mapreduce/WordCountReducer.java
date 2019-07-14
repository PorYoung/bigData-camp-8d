package com.poryoung.mapreduce;

import java.io.IOException;

import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Reducer;

/**
 * WordCountReducer
 */
public class WordCountReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    @Override
    protected void reduce(Text key, Iterable<IntWritable> ite, Context context)
            throws IOException, InterruptedException {
        int sum = 0;
        for (IntWritable i : ite) {
            sum += i.get();
        }
        context.write(key, new IntWritable(sum));
    }
}