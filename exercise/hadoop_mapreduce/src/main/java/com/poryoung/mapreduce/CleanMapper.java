package com.poryoung.mapreduce;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;
import java.util.ArrayList;

public class CleanMapper extends Mapper<LongWritable, Text, NullWritable, Text> {
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
    protected void map(LongWritable key, Text value, Mapper<LongWritable, Text, NullWritable, Text>.Context context)
            throws IOException, InterruptedException {
        if (!key.toString().equals("0")) {
            // System.out.println("原始数据" + value.toString());
            // String[] strList = value.toString().split("(?<!\\'),");
            String[] strList = value.toString().split(",(?=([^\"]*\"[^\"]*\")*[^\"]*$)");
            ArrayList<String> arrayList = new ArrayList<String>();
            // StringBuffer stringBuffer = new StringBuffer();
            for (int i = 0; i < strList.length; i++) {
                String str = strList[i].trim();
                // System.out.println(i + ": " + str);
                // if (str.isEmpty() || str.equals("['']") || str.equals("[]") ||
                // str.equals("[\"\"]")) {
                // // 空数据
                // return;
                // }
                if (str.isEmpty() || str.equals("[]") || str.equals("[\"\"]")) {
                    // 空数据
                    return;
                }
                arrayList.add(strList[i]);
                /*
                 * if (str.startsWith("\"") && !str.endsWith("\"")) {
                 * stringBuffer.append(strList[i]); } else if (!str.startsWith("\"") &&
                 * str.endsWith("")) { stringBuffer.append(strList[i]);
                 * arrayList.add(stringBuffer.toString()); stringBuffer.delete(0,
                 * stringBuffer.length()); } else { arrayList.add(stringBuffer.toString()); }
                 */
            }
            context.write(NullWritable.get(), new Text(String.join("|", arrayList)));
        } else {
            context.write(NullWritable.get(), value);
        }
    }
}
