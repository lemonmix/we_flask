# wechat_flask
1、根据https://github.com/songluyi/crawl_wechat上的方法从机器学习微信公众号中批量爬取文章，并提取文章中所有的github的url，保存github地址及文章地址于Mysql数据库中。
2、getGithub.py:
根据github地址爬取github中的相关信息（如url, title,description,stars,collect_time,source_url），保存于数据库中。
3、main.py:
使用flask框架建微信公众号，并将github相关信息显示在网页上。