# douyu-album
python+selenium爬取斗鱼主播相册所有图片
运行环境：
1.python3及以上版本  这里是python3.8
2.pip install selenium 安装selenium库
3.谷歌浏览器+ webdriver

使用注意事项：
1.这里有两个spider 使用pic_parse_spider.py这个爬虫
2.pic_parse_spider 中init方法存放的webdriver路径要修改成自己webdriver存放目录
3.其他文件基本都没啥要改的
4.运行时会默认在当前文件夹建立image文件夹，图片会按照名字在image文件夹内创建子文件夹，根据名字分类别存储对应图片
5.不是第一次运行时最好将之前的image文件夹删除，不过不删除爬取到的图片也会写入到里面
5.如果想看看效果到这里就可以结束了，如果要爬取更多请看第6步
6.这里为了调试默认爬取第一页的5个主播相册，如果要修改请找到pic_parse_spider.py 修改函数修改说明如下：
      1）两个循环
          外循环控制页数
              如果要爬取所有--》就找到最后一个break然后注释掉
              
      
        2）  内循环控制主播人数
              找到里面for循环
              i是判断个数将i和下面的break注释
              可以按照需要修改
