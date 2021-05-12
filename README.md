# SKEY-IdentityAuthentication
An Information System Security Experiment

基于S/Key协议的身份认证系统设计与实现  

## SKEY动态口令技术原理

### 定义

​	动态口令(One-Time Password , OTP)，又叫动态令牌、动态密码。

###  基本思想

​	依据用户身份信息，并引入不确定因子，产生随机变化的口令。

### 原理过程

#### 初始化

* 用户产生一个秘密的口令字：SecretPASS（长度大于八个字符）

* 服务器向用户发送一个种子：SEED（明传）

* 预处理：MD4(SecretPASS |SEED)，再把16字节的输出结果分为左右2部分，每部分8个字节，这两部分做异或运算，结果记为S。

####  生成口令序列

* 对S做N次S/KEY安全散列，得到第1个口令；

* 对S做N-1次S/KEY安全散列，得到第2个口令；

* 以此类推。。。
* 对S做1次S/KEY安全散列，得第N个口令

#### 口令的使用

* 第1个口令发送给服务器端保存
* 客户端顺序使用第2-N个口令

#### 口令的验证

服务器端将收到的一次性口令传给安全hash函数进行一次运算。若与上一次保存的口令匹配，则认证通过并将收到的口令保存供下次验证使用

## 流程图

### 服务器端流程图

![image](https://github.com/Jechin/SKEY-IdentityAuthentication/blob/main/src/Server.png)

### 客户端流程图

![image](https://github.com/Jechin/SKEY-IdentityAuthentication/blob/main/src/Client.png)

## 实现功能

- [x] 支持用户名/口令/验证码机制的身份认证；
- [x] 满足动态口令的技术要求；
- [x] 当前口令序列使用完毕后能够继续协商；
- [x] 记录用户登录日志，支持日志查看。

## 未实现功能

* 服务器端的循环连接或并发连接
* 日志文件的格式化对齐