**根据搜索关键词随机爬取快手视频**
- - -
**开发环境** 
|Package|version| 
| ------------- |:-------------:| 
| python|3.6.13| 
| requests|2.27.1 |
|fake-useragent	 | 	1.1.3  | 
|pandas| 	1.1.5  | 
- - -
**文件介绍**

kuaishou.py:  爬虫主体文件

ks_index.txt : 一个包含搜索关键词的文本文档（可以根据需要自己填写或者用chatgpt随机生成关键词）

- - - 
**参数介绍**

page :  爬取每一个关键词搜索结果视频的页数，越大即对应关键词的视频越多

max :   视频时长最大值，毫秒为单位

min :    视频时长最小值，毫秒为单位

index_txt : ks_index.txt 路径

dirpath : 视频保存路径

- - -

**功能介绍**

1.可以自动根据当日日期生成以当日为命名的文件夹

2.利用ks_index.txt里关键词进行搜索，得到搜索结果，爬取相应关键词的视频，以唯一标识命名视频保存。

![](https://joplin-1307529570.cos.ap-shanghai.myqcloud.com/joplin/20230711152540.png)

3.生成一个对应csv文档，用来存储视频id及标题

![](https://joplin-1307529570.cos.ap-shanghai.myqcloud.com/joplin/20230711152136.png)



