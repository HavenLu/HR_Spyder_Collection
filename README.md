# Offershow: Charles抓包微信小程序

微信小程序和网页的区别在于，我们没法直接右键/F12进入开发者模式观测结构，所以需要专门的抓包工具。我们这里使用Charles，以下是安装链接

[https://www.charlesproxy.com/download/](https://www.charlesproxy.com/download/)

## 安装完成之后需要对Charles进行一定的设置：

### 安装charles SSL根证书

- 帮助->SSL代理->安装charles root证书->常规->安装证书->本地计算机->将所有证书放到下列存储->受信任的证书颁发机构

### SSL代理设置PC本机为代理

- 代理->SSL代理设置->SSL代理->添加
- 主机: .
- 端口: 443

接着打开微信小程序的时候就能用Charles捕捉到相应的包。
![image](https://github.com/HavenLu/HR_Spyder_Collection/assets/117450296/5a6d3d9c-3b88-48e1-aef4-d2f2875fbcf9)

在Filter里输入`offershow`关键词，然后在V4包里的search salary里，可以看到工资数据是以JSON的格式存储在一个一个Object里。

那么难点就是如何用python实现登录的效果，然后获取数据。那么实际上，登录的信息都已经被Charles捕获显示在headers里了（token和referer可能涉及个人信息，打码是习惯）
![image](https://github.com/HavenLu/HR_Spyder_Collection/assets/117450296/03efdf5c-7b30-4c80-8f30-bbae9fa7ee5d)

将你的token和referer填充到代码里即可，需要注意的是token不是一劳永逸的，下一次爬取的时候需要粘贴新的token。






# 实习僧：requests库，字体反爬（md正在撰写中）

# Boss直聘：selenium库（md正在撰写中）

