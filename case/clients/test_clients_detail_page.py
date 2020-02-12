#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from common.common import Common
from common.my_ddt import *
import random


@ddt
class ClientsDetailPage(unittest.TestCase):
    """商户详情页"""

    client_id = "92302"

    @file_data(common_test=1)
    def test_common(self, payload):
        """通用测试"""
        Common.check(self, payload)

    @file_data()
    def test_branches(self, payload):
        """获取商户下门店信息"""
        payload['path'] = payload['path'].format(ClientsDetailPage.client_id)
        res = Common.check(self, payload)
        ClientsDetailPage.branch_id = res.json().get('result')[0].get('id')

    @file_data()
    def test_users_list(self, payload):
        """获取商户下员工信息"""
        payload['path'] = payload['path'].format(ClientsDetailPage.client_id)
        Common.check(self, payload)

    @file_data()
    def test_clients_log_types(self, payload):
        """获取商户操作日志分类"""
        Common.check(self, payload)

    @file_data()
    def test_search_clients_log(self, payload):
        """查询商户日志"""
        payload['params']['id'] = ClientsDetailPage.client_id
        Common.check(self, payload)

    @file_data()
    def test_developer_show(self, payload):
        """开发者选项"""
        payload['path'] = payload['path'].format(ClientsDetailPage.client_id)
        Common.check(self, payload)

    @file_data()
    def test_developer_setting(self, payload):
        """设置开发者选项"""
        payload['path'] = payload['path'].format(ClientsDetailPage.client_id)
        Common.check(self, payload)

    @file_data()
    def test_clients_finance(self, payload):
        """商户概览"""
        payload['path'] = payload['path'].format(ClientsDetailPage.client_id)
        Common.check(self, payload)

    @file_data()
    def test_clients_device_products(self, payload):
        """商户产品信息（设备型号）"""
        Common.check(self, payload)

    @file_data()
    def test_clients_device_statistics(self, payload):
        """商户设备统计（概览）"""
        payload['params']['client_id'] = ClientsDetailPage.client_id
        Common.check(self, payload)

    def clients_biz_orders(self, client_id, payload):
        """商户订单信息列表"""
        tmp = payload.copy()
        tmp['path'] = tmp['path'].format(client_id)
        res = Common.check(self, tmp)
        return res

    @file_data()
    def test_clients_biz_orders(self, payload):
        """商户订单信息列表"""
        res = self.clients_biz_orders(ClientsDetailPage.client_id, payload)
        ClientsDetailPage.order_id = res.json().get('result').get('data')[0].get('id')

    @file_data()
    def test_search_clients_biz_orders(self, payload):
        """搜索商户订单信息"""
        payload['params']['client_id'] = ClientsDetailPage.client_id
        Common.check(self, payload)

    @file_data()
    def test_biz_order_devices(self, payload):
        """查看商户某个订单的详情"""
        payload['path'] = payload['path'].format(ClientsDetailPage.order_id)
        res = Common.check(self, payload)
        ClientsDetailPage.biz_order_device_ids = res.json().get('result').get('rows')[0].get('id')

    # @file_data()
    # def test_return_order(self, payload):
    #     """退货"""
    #     payload['path'] = payload['path'].format(ClientsDetailPage.order_id)
    #     payload['params']['biz_order_device_ids'] = [ClientsDetailPage.biz_order_device_ids]
    #     Common.check(self, payload)

    @file_data()
    def test_client_logo(self, payload):
        """获取商户logo"""
        payload['path'] = payload['path'].format(ClientsDetailPage.client_id)
        Common.check(self, payload)

    def client_vr_homes(self, client_id, is_vr_home, payload):
        """VR房源"""
        tmp = payload.copy()
        tmp['path'] = tmp['path'].format(client_id)
        tmp['params']['is_vr_home'] = is_vr_home
        res = Common.check(self, tmp)
        return res

    @file_data()
    def test_client_vr_homes(self, payload):
        """VR房源"""
        res = self.client_vr_homes(ClientsDetailPage.client_id, 1, payload)
        ClientsDetailPage.vr_home_ids = res.json().get('result').get('rows')[0].get('id')

        res = self.client_vr_homes(ClientsDetailPage.client_id, 0, payload)
        ClientsDetailPage.not_vr_home_ids = res.json().get('result').get('rows')[0].get('id')

    @file_data()
    def test_add_delete_vr_home(self, payload):
        """新增/移除VR房源"""
        payload['path'] = payload['path'].format(ClientsDetailPage.client_id)
        payload['params']['home_ids'] = [ClientsDetailPage.not_vr_home_ids]
        Common.check(self, payload)

    @file_data()
    def test_clients_vr_home_info(self, payload):
        """查看VR房源信息"""
        payload['path'] = payload['path'].format(ClientsDetailPage.client_id, ClientsDetailPage.vr_home_ids)
        Common.check(self, payload)

    @file_data()
    def test_bind_vr_home(self, payload):
        """绑定VR资源"""
        payload['path'] = payload['path'].format(ClientsDetailPage.client_id, ClientsDetailPage.vr_home_ids)
        payload['params']['vr_resource_id'] = 'brenda'.join(str(random.randint(1, 10000)))
        Common.check(self, payload)

    @file_data()
    def test_dismantled_device(self, payload):
        """拆回设备"""
        payload['params']['client_id'] = ClientsDetailPage.client_id
        Common.check(self, payload)

    @file_data()
    def test_openapi_record_search_types(self, payload):
        """第三方接口调用记录筛选条件"""
        Common.check(self, payload)

    @file_data()
    def test_openapi_interface_record(self, payload):
        """第三方接口调用记录"""
        payload['params']['client_id'] = ClientsDetailPage.client_id
        Common.check(self, payload)

    @file_data()
    def test_contract(self, payload):
        """合同信息"""
        payload['params']['clientId'] = ClientsDetailPage.client_id
        Common.check(self, payload)

    @file_data()
    def test_manager_info(self, payload):
        """后台登录账号的信息"""
        Common.check(self, payload)

    @file_data()
    def test_contract_bill_info(self, payload):
        """账单信息"""
        payload['params']['clientId'] = ClientsDetailPage.client_id
        Common.check(self, payload)

    @file_data()
    def test_products(self, payload):
        """产品类型和型号"""
        Common.check(self, payload)

    @file_data()
    def test_extend_record(self, payload):
        """延保记录"""
        payload['params']['clientId'] = ClientsDetailPage.client_id
        Common.check(self, payload)






