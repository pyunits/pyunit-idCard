# **PyUnit-IDCard** [![](https://gitee.com/tyoui/logo/raw/master/logo/photolog.png)][1]

## 身份证实体抽取，身份证补全，身份证检测等功能。
[![](https://img.shields.io/badge/Python-3.7-green.svg)](https://pypi.org/project/pyunit-address/)

## 安装
    pip install pyunit-idcard


## 使用
```python
from pyunit_idcard import IdCard

card = IdCard()


def check_up():
    """检验身份证正确性"""
    assert card.check_up('522121199505307051') is True


def find_card():
    """查询身份证信息测试"""
    assert card.find_card('522121199505307051') == {'发证地': '贵州省遵义地区遵义县', '出生日期': '1995年05月30日', '性别': '男'}


def complete_information():
    """补全身份证测试"""
    assert card.complete_information('522121*99505307051') == ['522121199505307051']

def match_card():
    """寻找身份证测试"""
    assert card.match_card('我的身份证信息是5**121199505*07051你能猜出来吗') == [
        {'发证地': '贵州省遵义地区遵义县', '出生日期': '1995年05月30日', '性别': '男', '身份证号码': '522121199505307051'},
        {'发证地': '云南省昆明市呈贡县', '出生日期': '1995年05月30日', '性别': '男', '身份证号码': '530121199505307051'},
        {'发证地': '西藏自治区拉萨市林周县', '出生日期': '1995年05月10日', '性别': '男', '身份证号码': '540121199505107051'}]


if __name__ == '__main__':
    check_up()
    find_card()
    match_card()
    complete_information()
```

## Docker部署
    docker pull jtyoui/pyunit-idcard
    docker run -d -P jtyoui/pyunit-idcard

### 车牌号规则提取
|**参数名**|**类型**|**是否可以为空**|**说明**|
|------|------|-------|--------|
|data|string|YES|输入话带有身份证，未知数可以用*来替代|

### 请求示例
> #### Python3 Requests测试
```python
import requests

url = "http://IP:端口/pyunit/idCard"
data = {
    'data': '我的身份证信息是5**121199505*07051你能猜出来吗',
}
headers = {'Content-Type': "application/x-www-form-urlencoded"}
response = requests.post(url, data=data, headers=headers).json()
print(response)
``` 

> #### 返回结果
```json
{
    "code":200,
    "result":[
        {
            "出生日期":"1995年05月30日",
            "发证地":"贵州省遵义地区遵义县",
            "性别":"男",
            "身份证号码":"522121199505307051"
        },
        {
            "出生日期":"1995年05月30日",
            "发证地":"云南省昆明市呈贡县",
            "性别":"男",
            "身份证号码":"530121199505307051"
        },
        {
            "出生日期":"1995年05月10日",
            "发证地":"西藏自治区拉萨市林周县",
            "性别":"男",
            "身份证号码":"540121199505107051"
        }
    ]
}
```

***
[1]: https://blog.jtyoui.com