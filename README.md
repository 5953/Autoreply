1024 自动回帖 本人小白刚学python 这个项目是复制 @0honus0 大神的 自己修改了一些东东 目前完美运行  里面还有好多文件和注释我都没删除 各位就将就点看哈 


1   去除了登录步骤改为cookie登录（cookie可以设为一年 还是很不错的）目前是单账号  后期可以考虑修改为多账号
2   运行只需两个参数即可 两个都是cookie ps:1024的cookie有点奇怪，回复用的cookie和获取自己发帖数量用的cookie是不同的 ，所以需要两个cookie
     就因为这个导致我修改了好多次 最后才找到原因的  
3   怎么获取两个cookie    
      第一个cookie是我们登陆后在主页https://t66y.com/index.php下抓包获取
      第二个cookie 在技术区随便进入一个帖子里面然后抓包获取
      获取cookie的方法网上大把自己去百度吧
4   需要的两个cookie  添加 Secrets（打开仓库「Settings」中的「Secrets」，点击「New secret」）
    第一个cookie  命名为COOKIE（从首页处获得的cookie）
    第二个cookie  命名为RCOOKIE(从技术讨论区获得的cookie)
    
    
    
    ----------------------------------------------如果运行有报错看一下两个cookie对不对，如果是对的但是还是报错欢迎提出来我来修改------------------    
