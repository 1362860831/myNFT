# 基于非同质化代币的知识产权防侵权系统-说明文档
# ZWM-NFT-Readme
 

## 作品概要

在本作品中搭建了一个基于非同质化代币的知识产权防侵权系统。该作品底层由truffle进行区块链开发平台的合约部署，默认部署在ganache的区块链仿真平台上；该作品通过flask作为网站引擎对外提供web服务，接受用户请求，与底层区块链交互，并将结果反馈给用户；最后通过html+js提供网页前端与用户进行交互。

## 环境配置

为了使作品能够正常工作，请按照以下顺序进行环境配置：

1. 安装python3.7环境；
2. 下载代码，并安装`requirement.txt`中的依赖；

3. 安装[truffle](https://trufflesuite.com/truffle/)；

4. 安装[mysql](https://www.mysql.com/cn/)；

5. (可选项)安装[ganache](https://trufflesuite.com/ganache/)；

本作品使用linux操作系统进行部署和测试，并推荐使用[docker](https://www.docker.com/)进行测试工作。另外推荐安装ganache桌面端作为可视化的区块链仿真平台，当然您也可以选择其他的区块链平台部署合约！

## 代码安装与运行

为了使作品能够正常工作，请按照以下顺序进行代码安装：

1. 下载并解压代码；
2. 运行ganache或者其他区块链开发平台；
3. 根据启动的区块链开发平台的实际运行位置和端口，修改`truffle-config.js`文档中关于网络的设置，默认设置为ganache的默认配置；

``` javascript
  networks: {
    development: {
     host: "127.0.0.1", 
     port: 7545, 
     network_id: "*", 
    },
  },
```

4. 通过`truffle migrate`命令将`./contracts/`文件夹中的合约部署在区块链中
5. 将合约在区块链中的地址记录下来，并修改`app.py`中，合约实际部署的地址；

``` python
contract_address = "0xE32913159aE0F8772794E7D0A53247B2721b2912"		# 合约MyNFT地址
Faucet_address = "0x18E48C14515ee4A7Fa7C336d4F6d1E8f3b6118b1"		# 合约Faucet地址
RingSig_address = '0xD287959491e8Fc0D688E140fdAE2d8F91981922f'		# 合约RingSig地址
```

6. 修改`app.py`中实际的数据库位置；

``` python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:7b5b2e4afcb3e1ff30de9780ee3f05ac28cc12fa@127.0.0.1:3307/webUsers'
# 协议://用户名:密码@ip:port/数据库名
```

7. 通过`flask create`进行初始化，该操作会在系统中初始化30个用户，命名为test1~test30，密码为test123；
8. 通过`python3 app.py`运行系统；

## 网站页面和相关功能

1. 注册与登录。新用户在访问网站后可以注册新用户并登录网站。

![image-20221124175309730](https://raw.githubusercontent.com/1362860831/my_notePic/main/images/image-20221124175309730.png)

2. 用户账户信息模块。登录网站后，首先可以看到用户账户信息模块，这里显示了用户的相关账户信息，如用户名、账户地址、余额、持有版权代币情况等等。

![image-20221124180307133](https://raw.githubusercontent.com/1362860831/my_notePic/main/images/image-20221124180307133.png)

3. 测试币申请模块：为了仿真真实区块链上的交易情况，通过部署水管合约，为用户提供测试币进行后续测试；

![image-20221124175738869](https://raw.githubusercontent.com/1362860831/my_notePic/main/images/image-20221124175738869.png)

4. 版权注册模块：在这里用户可以通过花费测试币，为自己的数字图像作品注册版权，并生成零水印；

![image-20221124180518850](https://raw.githubusercontent.com/1362860831/my_notePic/main/images/image-20221124180518850.png)

5. 版权查询模块：在这里用户可以查询已经被注册的版权的归属情况；![image-20221124180541088](https://raw.githubusercontent.com/1362860831/my_notePic/main/images/image-20221124180541088.png)

6. 版权交易模块：用户可以通过该模块将自己所述的版权铸币交易给其他用户，交易完成后可以通过版权查询模块验证交易有效；
![image-20221124180753818](/home/wutianqi/.config/Typora/typora-user-images/image-20221124180753818.png)

![image-20221124180837008](https://raw.githubusercontent.com/1362860831/my_notePic/main/images/image-20221124180837008.png)

7. 版权仲裁模块：在这里可以进行版权仲裁，快速发现已注册版权的相似作品和他的注册水印信息。

![image-20221124181017305](https://raw.githubusercontent.com/1362860831/my_notePic/main/images/image-20221124181017305.png)

