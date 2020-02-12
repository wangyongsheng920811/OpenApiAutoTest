#!usr/bin/env python
# coding:utf-8
"""
@author: xuyanhui
@file: test_tags.py
@time: 2019-11-11
"""

import unittest
from common.common import Common
from common.my_ddt import *


@ddt
class Tags(unittest.TestCase):
    """商户标签"""

    @file_data(common_test=1)
    def test_common(self, payload):
        """通用测试"""
        Common.check(self, payload)

    @file_data()
    def test_add_tags(self, payload):
        """添加标签"""
        res = Common.check(self, payload)
        if res.json().get('err_msg') == 'ok':
            Tags.tag_id = res.json().get('result').get('id')

    @file_data()
    def test_update_clients_tags(self, payload):
        """更新标签"""
        payload['path'] = payload['path'].format(Tags.tag_id)
        Common.check(self, payload)

    @file_data()
    def test_delete_tags(self, payload):
        """删除标签"""
        payload['path'] = payload['path'].format(Tags.tag_id)
        Common.check(self, payload)

