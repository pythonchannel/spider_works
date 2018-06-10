###
# 本项目使用py2.7环境 
 
### 分别用Xpath,bs4,正则三种方式获取51job关于Python的招聘信息



`Spider`是三种爬取方式的基类，这里有请求招聘数据列表与工作详情的请求信息.

另外里面创建了解析列表与详情数据的抽象类，然后在子类里面对抽象类进行实现 



`ExeclUtils`这是一个操作Execl的工具类，评分有创建Execl的sheet表格与对表格进行写入数据.



### 效果图

![效果图](https://github.com/pythonchannel/fetch_51job/blob/master/QQ%E6%88%AA%E5%9B%BE20180318220606.png)
