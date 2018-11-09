# 批量爬取喜马拉雅专辑

## Base
Python3
requests, os
contextlib.closing

## Usage

输入对应专辑的url，自动爬去专辑内容到当前目录

## 原理

`https://www.ximalaya.com/revision/play/album` 该接口中存有相关音频的url的地址，遍历提取并下载即可，其参数有albumID(url中即可获取),pageSize,pageNum,order(0, 正序，-1，逆序)。

## 参考
没有系统的学过python，基本都通过google来完成的。

- [进度条](https://blog.csdn.net/supercooly/article/details/51046561)