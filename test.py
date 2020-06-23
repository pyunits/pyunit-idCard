#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/2/18 15:23
# @Author: Jtyoui@qq.com
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
