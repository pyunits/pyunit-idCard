# !/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time  : 2020/5/7 上午11:27
# @Author: Jtyoui@qq.com
# @Notes :  flask 启动
from flask import Flask, jsonify, request

from pyunit_idcard import IdCard

app = Flask(__name__)

card = IdCard()


def flask_content_type(requests):
    """根据不同的content_type来解析数据"""
    if requests.method == 'POST':
        if 'application/x-www-form-urlencoded' == requests.content_type:
            data = requests.form
        else:  # 无法被解析出来的数据
            raise Exception('POST的Content-Type必须是:application/x-www-form-urlencoded')
    elif requests.method == 'GET':
        data = requests.args
    else:
        raise Exception('只支持GET和POST请求')
    return data


@app.route('/')
def hello():
    return jsonify(code=200, result='welcome to pyunit-idCard')


@app.route('/pyunit/idCard', methods=['POST', 'GET'])
def supplement():
    try:
        data = flask_content_type(request)
        word = data['data']
        find = card.match_card(word)
        return jsonify(code=200, result=find)
    except Exception as e:
        return jsonify(code=500, error=str(e))


if __name__ == '__main__':
    app.run(port=2312)
