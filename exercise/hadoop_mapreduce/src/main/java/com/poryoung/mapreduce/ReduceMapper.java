package com.poryoung.mapreduce;

import java.io.IOException;

import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

/**
 * ReduceMapper
 */
public class ReduceMapper extends Reducer<NullWritable, Text, NullWritable, Text> {

    @Override
    protected void reduce(NullWritable arg0, Iterable<Text> values,
            Reducer<NullWritable, Text, NullWritable, Text>.Context context) throws IOException, InterruptedException {
        int count = 0;
        for (Text text : values) {
            String[] dataList = text.toString().split("\\|");
            if (count == 0) {
                count = dataList.length;
            } else if (dataList.length == count) {
                context.write(NullWritable.get(), new Text(String.join("|", dataList)));
            }
        }
    }
}