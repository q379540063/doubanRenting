# doubanRenting

文件说明
1、cookies.txt 登录用户的cookies信息，用工具Charles可以直接抓包获取，然后把cookies信息直接复制到文件中 格式如 x1:xxx;x2:xxx;x3:xxx......
2、setting.json 要爬的关键字  lasttime 不需要改动（记录上一次爬虫时间），keywords 为数组，自己写入要抓包的关键字
3、result.json 为爬虫的结果  其中一些参数，如最多爬取3天数据，每次爬虫的时间间隔，都可以在代码中修改，有备注
