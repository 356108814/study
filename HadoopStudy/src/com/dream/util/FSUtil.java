package com.dream.util;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.*;

import java.io.IOException;
import java.net.URI;
import java.util.ArrayList;
import java.util.List;

/**
 * FileSystem工具类
 * @author Yurisues 16-12-23 上午10:53
 */
public class FSUtil {

    /**
     * 挑选出符合正则表达式的文件
     */
    public static class RegexPathFilter implements PathFilter {
        private final String regex;
        public RegexPathFilter(String regex) {
            this.regex = regex;
        }

        @Override
        public boolean accept(Path path) {
            String localPath = path.toString();
            boolean isMatch = localPath.matches(regex);
//            System.out.println(localPath + ":" + isMatch);
            return isMatch;
        }
    }

    private Configuration conf = null;

    public FSUtil() throws IOException {
        this.conf = new Configuration();
    }

    public List<LocatedFileStatus> lsLocal(String path) throws IOException {
        FileSystem fs = FileSystem.get(this.conf);
        List<LocatedFileStatus> fileList = new ArrayList<>();
        RemoteIterator<LocatedFileStatus> locatedFileStatusRemoteIterator = fs.listFiles(new Path(path), false);
        while(locatedFileStatusRemoteIterator.hasNext()) {
            LocatedFileStatus status = locatedFileStatusRemoteIterator.next();
            System.out.println(status.getPath());
            System.out.println(status.getModificationTime());
            fileList.add(status);
        }
        return fileList;
    }

    /**
     * 列出文件信息
     * @param uri
     * @return FileStatus[]
     * @throws IOException
     */
    public FileStatus[] ls(String uri) throws IOException {
        // hdfs只能使用URI创建，而本地路径可以使用FileSystem fs = FileSystem.get(conf);
        FileSystem fs = FileSystem.get(URI.create(uri), conf);
        return fs.listStatus(new Path(uri));
    }

    /**
     * 返回符合正则表达式的文件信息
     * @param uri
     * @param regex 正则通配符
     * @return FileStatus[]
     * @throws IOException
     */
    public FileStatus[] ls(String uri, String regex) throws IOException {
        // hdfs只能使用URI创建，而本地路径可以使用FileSystem fs = FileSystem.get(conf);
        FileSystem fs = FileSystem.get(URI.create(uri), conf);
        return fs.globStatus(new Path(uri), new RegexPathFilter(regex));
    }

    public static void main(String[] args) throws IOException {
        String hdfsUri = "hdfs://master/";
        FSUtil fsUtil = new FSUtil();
//        fsUtil.lsLocal("/home/dream/");
//        FileStatus[] status = fsUtil.ls("/home/dream");
        FileStatus[] status = fsUtil.ls("/home/dream/*", "file:/home/dream/.*");
        if(status != null) {
            for(FileStatus stat: status) {
                System.out.println(stat.getPath());
//                System.out.println(stat.getOwner());
            }
        }
    }
}
