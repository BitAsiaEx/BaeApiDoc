# API 文档

## 行情 API

### 获取首页行情
URL: https://www.bitasiabit.com/app/v1/getIndexMarketCus  
Type: **GET**  
请求参数: 无  
回应参数:
参数名称 | 数据类型 | 描述 | 备注
--- | --- | --- | ---
code | Integer | 回传状态代码 | 200: 成功<br> 300: 失败
msg | String | 获取首页行情 |
time | timestamp | 时间戳记 |

Data 说明
```JSON
{
    "pairname":币别缩写,
    "name":币别中文名称,
    "total":成交量,
    "high":最高价,
    "low":最低价,
    "price":上次成交价,
    "rose":涨跌幅 
}
```

### 获取交易对代码
URL: https://www.bitasiabit.com/app/v1/pairsCus  
Type: **GET**  
请求参数: 无  
回应参数:
参数名称 | 数据类型 | 描述 | 备注
--- | --- | --- | ---
code | Integer | 回传状态代码 | 200: 成功<br> 300: 失败
msg | String | 获取交易对代码 |
time | timestamp | 时间戳记 |

Data 说明
```JSON
{
    "tradeId":交易 ID 代号,
    "pairShortName":币别缩写
}
```

### 获取行情
URL: https://www.bitasiabit.com/app/v1/getMarketCus  
Type: **GET**  
请求参数:  
参数名称 | 数据类型 | 描述 | 是否必输入
--- | --- | --- | ---
pairname | String | 输入交易对代码 | 是

回应参数:
参数名称 | 数据类型 | 描述 | 备注
--- | --- | --- | ---
code | Integer | 回传状态代码 | 200: 成功<br> 300: 失败
msg | String | 获取行情 |
time | timestamp | 时间戳记 |

Data 说明
```JSON
{
    "pair":币别缩写,
    "total":成交量,
    "high":最高价,
    "low":最低价,
    "price":上次成交价,
    "rose":涨跌幅,
    "ask":卖1,
    "bid":买1
}
```

### 获取深度数据
URL: https://www.bitasiabit.com/app/v1/getFullDepthCus  
Type: **GET**  
请求参数: 
参数名称 | 数据类型 | 描述 | 是否必输入
--- | --- | --- | ---
pairname | String | 输入交易对代码 | 是

回应参数:
参数名称 | 数据类型 | 描述 | 备注
--- | --- | --- | ---
code | Integer | 回传状态代码 | 200: 成功<br> 300: 失败
msg | String | 获取深度数据 |
time | timestamp | 时间戳记 |

Data 说明
```JSON
{
    "ask":卖1 [[价格, 数量]],
    "bid":买1 [[价格, 数量]]
}
```

### 查询挖矿难度
URL: https://www.bitasiabit.com/app/v1/getDifficulty  
Type: **GET**  
请求参数: 无  
回应参数:
参数名称 | 数据类型 | 描述 | 备注
--- | --- | --- | ---
code | Integer | 回传状态代码 | 200: 成功<br> 300: 失败
msg | String | 前挖矿难度 |
time | timestamp | 时间戳记 |

Data 说明
```JSON
{
    "difficulty":挖矿难度
}
```

## RSA 加密 API

### RSA POST JSON 加密方式
1. 以买/卖委讬(限价)为例(/app/v1/entrustSubmitCus),除了apiKey,其他参数皆加入 JSON 字串,完成的 JSON 字串如下:
    ```JSON
    {
        "secretKey":"5DpP1Vgq5tUXwngHcJAYR1EnRamVuBBt",
        "type" :"1",
        "pairname":"BCHCNY",
        "price":"500",
        "count":"1"
    }
    ```
2. 以我方提供的 public key 做 RSA 加密后会产生一串乱数例如下方显示:
    ```
    0LTup+tDcIH4oyzgAj7FSENiTO8SeiMrooetvYkxyuKo9KrB2o+v3y7q1ZXATGo2b2w2cnWvpYnDUXaYTWjsvFLW7hEkDx63lHbt3IKIoFBEgNYtfEKPLmWjECO2joDDcUE6YI/vmqGXZHfgQAOTlbBC1f/WfuTcPrj9AnhhDyjLWmabTkACv0lsVWOLRSVrB9bELhhYBLhCrbuD46+Snzvx3gWp4SnxU4jg47XaWWcDM1qONREpCDY6hj6eXtqf 
    ```
3. 再把 apiKey 和产生的 RSA 字串包成下方 JSON 格式送出:
    ```JSON
    {
        "apiKey":"oJSchzfuyBaiggpllWCW9IV5lJqY7Al2",
        "data":"0LTup+tDcIH4oyzgAj7FSENiTO8SeiMrooetvYkxyuKo9KrB2o+v3y7q1ZXATGo2b2w2cnWvpYnDUXaYTWjsvFLW7hEkDx63lHbt3IKIoFBEgNYtfEKPLmWjECO2joDDcUE6YI/vmqGXZHfgQAOTlbBC1f/WfuTcPrj9AnhhDyjLWmabTkACv0lsVWOLRSVrB9bELhhYBLhCrbuD46+Snzvx3gWp4SnxU4jg47XaWWcDM1qONREpCDY6hj6eXtqf"
    } 
    ```
备注:
* 封装方式: base64
* RSA 的公钥导出格式: PKCS8
* PKI: X.509

### 买卖委讬(限价)
URL: https://www.bitasiabit.com/app/v1/entrustSubmitCus  
Type: **POST**  
请求参数: 
参数名称 | 数据类型 | 描述 | 是否必输入
--- | --- | --- | ---
apiKey | String | | 是
secretKey | String | | 是
type | String | 0: 买<br> 1: 卖 | 是
pairname | String | 输入交易对代码 | 是
price | BigDecimal | 金额 | 是
count | BigDecimal | 数量 | 是

回应参数:
参数名称 | 数据类型 | 描述 | 备注
--- | --- | --- | ---
code | Integer | 回传状态代码 | 200: 成功<br> 300: 失败
msg | String | 下单成功 |
time | timestamp | 时间戳记 |

Data 说明
```JSON
{
    "entrustId":委单 ID,
    "entrustType":Sell or Buy,
    "tradeId":交易 ID
}
```

### 买卖委讬IOC（非成即撤） 
URL: https://www.bitasiabit.com/app/v1/entrustSubmitIocCus  
Type: **POST**  
请求参数: 
参数名称 | 数据类型 | 描述 | 是否必输入
--- | --- | --- | ---
apiKey | String | | 是
secretKey | String | | 是
type | String | 0: 买<br> 1: 卖 | 是
pairname | String | 输入交易对代码 | 是
price | BigDecimal | 金额 | 是
count | BigDecimal | 数量 | 是

回应参数:
参数名称 | 数据类型 | 描述 | 备注
--- | --- | --- | ---
code | Integer | 回传状态代码 | 200: 成功<br> 300: 失败
msg | String | 下单成功 |
time | timestamp | 时间戳记 |

Data 说明
```JSON
{
    "entrustId":委单 ID,
    "entrustType":Sell or Buy,
    "tradeId":交易 ID
}
```

### 买卖委讬(市价)
URL: https://www.bitasiabit.com/app/v1/entrustMarketCus  
Type: **POST**  
请求参数: 
参数名称 | 数据类型 | 描述 | 是否必输入
--- | --- | --- | ---
apiKey | String | | 是
secretKey | String | | 是
type | String | 0: 买<br> 1: 卖 | 是
pairname | String | 输入交易对代码 | 是
price | BigDecimal | 金额 | 买方为必填栏位
count | BigDecimal | 数量 | 卖方为必填栏位

回应参数:
参数名称 | 数据类型 | 描述 | 备注
--- | --- | --- | ---
code | Integer | 回传状态代码 | 200: 成功<br> 300: 失败
msg | String | 下单成功 |
time | timestamp | 时间戳记 |

Data 说明
```JSON
{
    "entrustId":委单 ID,
    "entrustType":Sell or Buy,
    "tradeId":交易 ID
}
```

### 撤单
URL: https://www.bitasiabit.com/app/v1/entrustBatchCancelCus  
Type: **POST**  
请求参数: 
参数名称 | 数据类型 | 描述 | 是否必输入
--- | --- | --- | ---
apiKey | String | | 是
secretKey | String | | 是
entrustIdList | String |委单ID ex:1,2,3 | 是

回应参数:
参数名称 | 数据类型 | 描述 | 备注
--- | --- | --- | ---
code | Integer | 回传状态代码 | 200: 成功<br> 300: 失败
msg | String | 撤单成功 |
time | timestamp | 时间戳记 |

### 当前委单
URL: https://www.bitasiabit.com/app/v1/userEntrustCus  
Type: **POST**  
请求参数: 
参数名称 | 数据类型 | 描述 | 是否必输入
--- | --- | --- | ---
apiKey | String | | 是
secretKey | String | | 是
entrustId | String | 委单 ID | 否
pairname | String | 输入交易对代码 | 否

回应参数:
参数名称 | 数据类型 | 描述 | 备注
--- | --- | --- | ---
code | Integer | 回传状态代码 | 200: 成功<br> 300: 失败
msg | String | 个人当前委单列表 |
time | timestamp | 时间戳记 |

Data 说明
```JSON
{
    "createTime":建立时间,
    "price":价格,
    "count":数量,
    "amount":总金额,
    "entrustId":委单 ID,
    "updateTime":最后更新时间,
    "type":SELL or BUY (String),
    "leftCount":剩余数量,
    "buyShortName":买方币名称,
    "sellShortName":卖方币名称,
    "status":(部分成交、完全成交、已撤销),
    "statusType":1(未成交)、2(部分成交),
    "ordertype":0(限价)、1(市价),
    "tradeId":交易 ID,
    "tradeType":交易名称
}
```

### 历史委单
URL: https://www.bitasiabit.com/app/v1/userEntrustHistoryCus  
Type: **POST**  
请求参数: 
参数名称 | 数据类型 | 描述 | 是否必输入
--- | --- | --- | ---
apiKey | String | | 是
secretKey | String | | 是
entrustId | String | 委单 ID | 否
pairname | String | 输入交易对代码 | 否
currentPage | Integer | 指定跳页 | 否

回应参数:
参数名称 | 数据类型 | 描述 | 备注
--- | --- | --- | ---
code | Integer | 回传状态代码 | 200: 成功<br> 300: 失败
msg | String | 个人历史委单列表 |
time | timestamp | 时间戳记 |

Data 说明
```JSON
{
    "createTime":建立时间,
    "price":价格,
    "count":数量,
    "entrustId":委单 ID,
    "updateTime":最后更新时间,
    "type":SELL or BUY (String),
    "avgPrice":平均成交价,
    "buyShortName":买方币名称,
    "sellShortName":卖方币名称,
    "status":(部分成交、完全成交、已撤销),
    "statusType":2(部分成交)、3(完全成交)、5(已撤销),
    "ordertype":0(限价)、1(市价),
    "fees":手续费(以交易币种为计价单位),
    "tradeId":交易 ID,
    "tradeType":交易名称,
    "dealAmount":总成交金额,
    "dealCount":剩余数量,
    "pages":总页数,
    "hittorySize":总笔数
}
```

### 委单查询
URL: https://www.bitasiabit.com/app/v1/userEntrustSearchCus  
Type: **POST**  
请求参数: 
参数名称 | 数据类型 | 描述 | 是否必输入
--- | --- | --- | ---
apiKey | String | | 是
secretKey | String | | 是
entrustId | String | 委单 ID | 是

回应参数:
参数名称 | 数据类型 | 描述 | 备注
--- | --- | --- | ---
code | Integer | 回传状态代码 | 200: 成功<br> 300: 失败
msg | String | 委单查询 |
time | timestamp | 时间戳记 |

Data 说明
```JSON
{
    "createTime":建立时间,
    "price":价格,
    "count":数量,
    "amount":总金额,
    "entrustId":委单 ID,
    "updateTime":最后更新时间,
    "type":SELL or BUY (String),
    "leftCount":剩余数量,
    "buyShortName":买方币名称,
    "sellShortName":卖方币名称,
    "status":(部分成交、完全成交、已撤销),
    "statusType":1(未成成交)、2(部分成交)、3(完全成交)、5(已撤销),
    "ordertype":0(限价)、1(市价),
    "fees":手续费(以交易币种为计价单位),
    "tradeId":交易 ID,
    "tradeType":交易名称
}
```

### 获取用户资产
URL: https://www.bitasiabit.com/app/v1/userCapitalCus  
Type: **POST**  
请求参数: 
参数名称 | 数据类型 | 描述 | 是否必输入
--- | --- | --- | ---
apiKey | String | | 是
secretKey | String | | 是

回应参数:
参数名称 | 数据类型 | 描述 | 备注
--- | --- | --- | ---
code | Integer | 回传状态代码 | 200: 成功<br> 300: 失败
msg | String | 获取用户资产 |
time | timestamp | 时间戳记 |

Data 说明
```JSON
{
    "totalAsset":总资产,
    "total":可用金额,
    "forzen":冻结金额,
    "updateTime":最后更新时间,
    "coinName":币别名称,
    "shortname":币别缩写
}
```
