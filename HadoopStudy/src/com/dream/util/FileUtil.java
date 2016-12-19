package com.dream.util;

import java.io.File;

/**
 * @author Yurisues 16-12-15 下午3:04
 */
public class FileUtil {
    public static Boolean isDirectoryExist(String path){
        File file = new File(path);
        if(file.isDirectory() && file.exists()){
            return true;
        }
        return false;
    }

    /**
     * 删除文件夹以及下面的文件
     * @param path
     * @return
     */
    public static Boolean deleteDirectory(String path){
        File dir = new File(path);
        if (dir.isDirectory()) {
            String[] children = dir.list();
            //递归删除目录中的子目录下
            if(children != null){
                for (int i = 0; i < children.length; i++) {
                    boolean success = deleteDirectory(children[i]);
                    if (!success) {
                        return false;
                    }
                }
            }
        }
        // 目录此时为空，可以删除
        return dir.delete();
    }

    public static void main(String[] args){
        deleteDirectory("output");
    }
}
