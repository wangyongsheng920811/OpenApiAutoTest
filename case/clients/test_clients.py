#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from common.common import Common
from common.my_ddt import *


@ddt
class Clients(unittest.TestCase):
    """商户"""

    client_id = 92302
    client_phone = '11099990047'

    @file_data(common_test=1)
    def test_common(self, payload):
        """通用测试"""
        Common.check(self, payload)

    @file_data()
    def test_clients_optional_permissions(self, payload):
        """商户可选权限列表"""
        Common.check(self, payload)

    @file_data()
    def test_clients_business(self, payload):
        """获取商户对接人列表"""
        Common.check(self, payload)

    @file_data()
    def test_search_client_keyword(self, payload):
        """根据商户手机号／名称搜索商户"""
        payload['params']['keyword'] = Clients.client_phone
        res = Common.check(self, payload)
        assert res.json().get('result').get('count') != 0

    @file_data()
    def test_search_client_id(self, payload):
        """根据客户ID搜索商户"""
        payload['params']['id'] = Clients.client_id
        Common.check(self, payload)

    @file_data()
    def test_search_client_by_id_keyword(self, payload):
        """根据客户ID和手机号／名称搜索商户"""
        Common.check(self, payload)

    @file_data()
    def test_add_client(self, payload):
        """添加商户"""
        Common.rerun_case(self, 'test_common_test_clients_optional_permissions_test_common')
        Common.rerun_case(self, 'test_common_test_clients_business_test_common')
        res = Common.check(self, payload)
        if res.json().get('err_msg') == 'ok':
            Clients.new_client_id = res.json().get('result').get('client_id')

    @file_data()
    def test_freeze_client(self, payload):
        """冻结／解冻商户"""
        payload['path'] = payload['path'].format(Clients.client_id)
        Common.check(self, payload)

        Common.rerun_case(self, 'test_common_test_clients_list_test_common')

    @file_data()
    def test_delete_client(self, payload):
        """删除商户"""
        payload['path'] = payload['path'].format(Clients.new_client_id)
        res = Common.check(self, payload)
        assert res.json().get('result') == Clients.new_client_id



