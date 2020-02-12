#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import time
from common.common import Common
from common.my_ddt import *


@ddt
class Homes(unittest.TestCase):
    '''房源'''
    @file_data(common_test=1)
    def test_common(self, payload):
        '''通用测试'''
        Common.check(self, payload)

    @file_data()
    def test_add_home(self, payload):
        '''添加房源'''
        Homes.home_name = Homes.home_number = 'AutoTest{}'.format(Common.format_date())
        payload['params']['home_name'] = payload['params']['number'] = Homes.home_number
        res = Common.check(self, payload)
        # 分散式
        if payload['params']['home_type'] == 1 and payload['check_res_code'] == 0:
            Homes.home_id = res.json().get('result').get('home_id')
        # 集中式
        elif payload['params']['home_type'] == 2 and payload['check_res_code'] == 0:
            Homes.home_id_2 = res.json().get('result').get('home_id')
        time.sleep(1)

    @file_data()
    def test_get_home_info(self, payload):
        '''获取房源详情'''
        payload['path'] = payload['path'].format(Homes.home_id)
        payload['check_res_data'] = payload['check_res_data'].format(Homes.home_id)
        Common.check(self, payload)

    @file_data()
    def test_get_home_list(self, payload):
        '''获取房源列表'''
        payload['check_res_data'] = payload['check_res_data'].format(Homes.home_id)
        Common.check(self, payload)

    @file_data()
    def test_add_room(self, payload):
        '''添加房源房间'''
        if payload['desc'] == '添加分散式房源房间':
            payload['path'] = payload['path'].format(Homes.home_id)
        elif payload['desc'] == '添加集中式房源房间':
            payload['path'] = payload['path'].format(Homes.home_id_2)
        else:
            payload['path'] = payload['path'].format(Homes.home_id)
        Common.check(self, payload)

    @file_data()
    def test_get_room_list(self, payload):
        '''获取房间列表'''
        if payload['desc'] == '获取分散式房源下房间列表':
            payload['path'] = payload['path'].format(Homes.home_id)
            payload['check_res_data'] = payload['check_res_data'].format(Homes.home_id)
            res = Common.check(self, payload)
            Homes.room_id = res.json().get('result')[1].get('id')
        elif payload['desc'] == '获取集中式房源下房间列表':
            payload['path'] = payload['path'].format(Homes.home_id_2)
            payload['check_res_data'] = payload['check_res_data'].format(Homes.home_id_2)
            res = Common.check(self, payload)
            Homes.room_id_2 = res.json().get('result')[1].get('id')
        else:
            payload['path'] = payload['path'].format(Homes.home_id)
            payload['check_res_data'] = payload['check_res_data'].format(Homes.home_id)
            Common.check(self, payload)

    @file_data()
    def test_get_room_info(self, payload):
        '''获取房间详情'''
        payload['path'] = payload['path'].format(Homes.room_id)
        payload['check_res_data'] = payload['check_res_data'].format(Homes.room_id)
        Common.check(self, payload)

    @file_data()
    def test_update_room_1(self, payload):
        '''更新单个房间'''
        payload['path'] = payload['path'].format(Homes.room_id)
        payload['check_res_data'] = payload['check_res_data'].format(Homes.room_id)
        Common.check(self, payload)

    @file_data()
    def test_update_room_2(self, payload):
        '''更新多个房间'''
        payload['path'] = payload['path'].format(Homes.home_id_2)
        payload['params']['rooms'][0].update({'id': Homes.room_id_2})
        Common.check(self, payload)

    @file_data()
    def test_update_home(self, payload):
        '''更新房源'''
        payload['path'] = payload['path'].format(Homes.home_id)
        payload['params']['number'] = payload['params']['number'].format(Homes.home_number)
        Common.check(self, payload)

    @file_data()
    def test_get_room_elemeter_setting(self, payload):
        '''获取房间用电配置'''
        payload['path'] = payload['path'].format(Homes.room_id)
        Common.check(self, payload)

    @file_data()
    def test_get_room_charge_list(self, payload):
        '''获取房间充值记录列表'''
        payload['path'] = payload['path'].format(Homes.room_id)
        payload['params']['startTime'] = Common.format_timestamp(1000, -5)
        payload['params']['endTime'] = Common.format_timestamp()
        res = Common.check(self, payload)
        self.assertEqual(res.status_code, 200)

    @file_data()
    def test_export_room_charge_list(self, payload):
        '''导出房间充值记录列表'''
        payload['path'] = payload['path'].format(Homes.room_id)
        payload['params']['startTime'] = Common.format_timestamp(1000, -5)
        payload['params']['endTime'] = Common.format_timestamp()
        Common.check(self, payload)

    @file_data()
    def test_get_room_watermeter_setting(self, payload):
        '''获取房间用水配置'''
        payload['path'] = payload['path'].format(Homes.room_id)
        Common.check(self, payload)

    @file_data()
    def test_get_lock_setting(self, payload):
        '''获取安全配置'''
        # 房间
        if payload['params']['type'] == 'room':
            payload['params']['value'] = payload['params']['value'].format(Homes.room_id)
        # 房源
        elif payload['params']['type'] == 'home':
            payload['params']['value'] = payload['params']['value'].format(Homes.home_id)
        Common.check(self, payload)

    @file_data()
    def test_get_room_electric_record(self, payload):
        '''获取房间用电记录'''
        payload['path'] = payload['path'].format(Homes.room_id)
        payload['params']['start_time'] = Common.format_timestamp(1000, -5)
        payload['params']['end_time'] = Common.format_timestamp()
        Common.check(self, payload)

    @file_data()
    def test_delete_room(self, payload):
        '''删除房间'''
        payload['path'] = payload['path'].format(Homes.room_id_2)
        payload['check_res_data'] = payload['check_res_data'].format(Homes.room_id_2)
        Common.check(self, payload)

    @file_data()
    def test_get_home_list_info(self, payload):
        '''获取房源下拉列表'''
        payload['check_res_data'] = payload['check_res_data'].format(Homes.home_id)
        Common.check(self, payload)

    @file_data()
    def test_get_home_devices(self, payload):
        '''获取房源下所有设备信息'''
        payload['path'] = payload['path'].format(Homes.home_id)
        Common.check(self, payload)

    @file_data()
    def test_get_home_elemeter_setting(self, payload):
        '''获取房源用电配置'''
        payload['path'] = payload['path'].format(Homes.home_id)
        Common.check(self, payload)

    @file_data()
    def test_get_home_pool_setting(self, payload):
        '''获取房源公摊配置'''
        payload['path'] = payload['path'].format(Homes.home_id)
        Common.check(self, payload)

    @file_data()
    def test_get_lock_setting_sub_list(self, payload):
        '''获取子层级的门锁提醒设置列表'''
        payload['params']['value'] = str(Homes.home_id)
        Common.check(self, payload)

    @file_data()
    def test_get_home_watermeter_setting(self, payload):
        '''获取房源用水配置'''
        payload['path'] = payload['path'].format(Homes.home_id)
        Common.check(self, payload)
