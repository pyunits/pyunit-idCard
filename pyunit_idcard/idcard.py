# !/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/6/22 上午10:07
# @Author: Jtyoui@qq.com
# @Notes : 身份证实体抽取，身份证补全，身份证检测等功能
import json
import os
import re
from datetime import datetime


class NumberNotShortError(Exception):
    ...


class IDCardNotStingError(Exception):
    ...


class IDCardFormatError(Exception):
    ...


class VerificationLegalError(Exception):
    ...


chinese = {
    ord('一'): '1',
    ord('二'): '2',
    ord('三'): '3',
    ord('四'): '4',
    ord('五'): '5',
    ord('六'): '6',
    ord('七'): '7',
    ord('八'): '8',
    ord('九'): '9',
    ord('幺'): '1',
    ord('拐'): '7',
    ord('洞'): '0',
    ord('两'): '2',
    ord('勾'): '9',
    ord('x'): 'X'
}


class IdCard:
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'idCard.json')) as fp:
            regions = json.load(fp)
            self.region = {region['code']: region['name'] for region in regions}
        self.card = []

    @staticmethod
    def correct_card(card: str):
        """纠正数字数字

        比如：方言，中文数据等
        """
        translate = card.translate(chinese)
        return translate

    def check_up(self, id_card: str):
        """检验身份证信息的合法性"""
        assert isinstance(id_card, str), IDCardNotStingError('身份证号码必须是字符串类型')
        assert len(id_card) == 18, NumberNotShortError(F'身份证号码必须是18位，不支持{len(id_card)}位身份证')
        if not (id_card[:-1].isdigit() and re.match('[0-9X]', id_card[-1])):
            raise IDCardFormatError('身份证格式错误')
        assert self._verification_legal(id_card) == id_card[-1], VerificationLegalError('合法性验证失败')
        return True

    @staticmethod
    def _verification_legal(id_card: str):
        """检验最后一位"""
        coefficient = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        last = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]
        s = sum([int(x) * y for x, y in zip(id_card[:-1], coefficient)])
        remainder = last[s % 11]
        return str(remainder)

    def find_card(self, id_card: str):
        """查询身份证"""
        id_card = self.correct_card(id_card)
        self.check_up(id_card)
        province = id_card[:6]
        year = id_card[6:10]
        month = id_card[10:12]
        day = id_card[12:14]
        sex = '女' if int(id_card[16]) % 2 == 0 else '男'
        return {'发证地': self.region[province], '出生日期': f'{year}年{month}月{day}日', '性别': sex}

    def _completion(self, id_card: str):
        """补全身份证缺失位

        缺失位用*来填充： 比如： ***121199505307*51
        """
        assert len(id_card) == 18, NumberNotShortError(F'身份证号码必须是18位，不支持{len(id_card)}位身份证')
        province = id_card[:6]
        year = id_card[6:10]
        month = id_card[10:12]
        day = id_card[12:14]
        sort = id_card[14:17]
        last = id_card[17]
        if '*' in province:
            province_re = province.replace('*', '.')
            for k in self.region:
                if re.match(province_re, k):
                    self._completion(k + id_card[6:])
        elif '*' in year:
            current_year = str(datetime.now().year)
            if '*' in year[0]:
                for y_1 in ['1', '2']:
                    id_card = id_card[:6] + y_1 + id_card[7:]
                    self._completion(id_card)
            if '*' in year[1:]:
                year_re = year.replace('*', '.')
                for y_2 in range(1984, int(current_year) + 1):
                    if re.match(year_re, str(y_2)):
                        id_card = id_card[:6] + str(y_2) + id_card[10:]
                        self._completion(id_card)
        elif '*' in month:
            month_re = month.replace('*', '.')
            for mon in range(1, 13):
                m = f'{mon:0>2}'
                if re.match(month_re, m):
                    id_card = id_card[:10] + m + id_card[12:]
                    self._completion(id_card)
        elif '*' in day:
            day_re = day.replace('*', '.')
            for d in range(1, 32):
                ds = f'{d:0>2}'
                try:
                    datetime(int(year), int(month), d)
                    if re.match(day_re, ds):
                        id_card = id_card[:12] + ds + id_card[14:]
                        self._completion(id_card)
                except ValueError:
                    pass
        elif '*' in sort:
            sort_re = sort.replace('*', '.')
            for st in range(1, 1000):
                s = f'{st:0>3}'
                if re.match(sort_re, s):
                    id_card = id_card[:14] + s + id_card[-1]
                    self._completion(id_card)
        elif '*' in last:
            new_last = self._verification_legal(id_card)
            id_card = id_card[:-1] + new_last
            self._completion(id_card)
        else:
            self.card.append(id_card)

    def complete_information(self, id_card: str):
        """补全身份证缺失位

        缺失位用*来填充： 比如： ***121199505307*51
        """
        id_card = self.correct_card(id_card)
        self.card.clear()
        self._completion(id_card)
        comps = []
        for comp in self.card:
            try:
                if self.check_up(comp):
                    comps.append(comp)
            except AssertionError:
                pass
        return comps

    def match_card(self, card):
        """包含一句身份证信息的话

        包含18位身份证信息，可以自动补全信息
        eg: 我的身份证信息是5**121199*05*07051你能猜出来吗？
        :param card: 包含一句身份证信息的语句
        :return: 身份证信息
        """
        messages = []
        for message in re.finditer('[0-9*]{17}[0-9*xX]', card):
            cards = self.complete_information(message.group())
            for card in cards:
                data = self.find_card(card)
                data['身份证号码'] = card
                messages.append(data)
        return messages
