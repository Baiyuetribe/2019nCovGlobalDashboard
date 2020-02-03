# nCoV-Map: 新型肺炎疫情地图

在线体验地址： https://yiqing.baiyue.one

### 项目依赖
flask
requests
googletrans
pyecharts
此项目为第二版，所有数据为实时动态爬取，因闲置机器有8GB内存，可自由挥霍，所以暂未设置分离式的数据库，已完成Docker化，任何人都可以轻松部署。

1.动态效果图
### 全屏效果

![](https://img.baiyue.one/upload/2020/02/5e36571a32674.jpg)
2.局部效果- 世界地图

![](https://baiyue.one/wp-content/uploads/2020/02/2020020205411843.gif)

3.局部效果- 疫情曲线
![](https://baiyue.one/wp-content/uploads/2020/02/2020020205414135.gif)

4.局部效果- 每日确诊K线

![](https://baiyue.one/wp-content/uploads/2020/02/2020020205415820.gif)
### 可改进思路

- 尝试从数据中提取市县级统计、或市县级增长-时间的动态演示
- 尝试制作河流图，汇集负面的疑似案例，以及正面的确诊案例（内嵌治愈、死亡）
- 与SARS对比图
- 与SARS等对比拟合本次的疫情曲线，尝试预测疫情顶峰
- 尝试嵌入今日头条热榜
- 尝试嵌入热点舆情 云词图

### 部署方法：

STEP1: 安装Docker基础环境(适用于Centos、Ubuntu、Debian等等)

 ```
 echo y | bash <(curl -L -s https://raw.githubusercontent.com/Baiyuetribe/codes/master/docker.sh)  #安装docker环境
 ```

STEP2:部署程序

运行程序（目前为第二版：主要为全球疫情监测）：

```
docker run -d --name=yiqing -p 5000:5000 --log-opt max-size=50m --log-opt max-file=3 --restart=always baiyuetribe/code:yiqing2
```

然后访问http://ip:5000 就可以访问了。如需域名访问（请搜本站域名反代）。


- 2020.2.3

因谷歌翻译api限制调用，暂时移除翻译，启用本地字典

- 2020.2.2

上线预览地址

- 更多介绍：https://baiyue.one/archives/1553.html