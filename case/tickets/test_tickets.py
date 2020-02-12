#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from common.common import Common
from common.my_ddt import *


@ddt
class Tickets(unittest.TestCase):
    '''工单'''

    @file_data(common_test=1)
    def test_common(self, payload):
        '''通用测试'''
        Common.check(self, payload)

    @file_data()
    def test_add_ticket_1(self, payload):
        '''增加新装工单'''
        payload['params']['subscribe']['expected_time'] = Common.format_timestamp()
        res = Common.check(self, payload)
        if payload['desc'] == '增加新装工单':
            Tickets.ticket1_id = res.json().get('result').get('id')
            Tickets.ticket1_sn = res.json().get('result').get('ticket_sn')
        elif payload['desc'] == '增加无网关门锁新装工单':
            Tickets.ticket1_lock_id = res.json().get('result').get('id')
            Tickets.ticket1_lock_sn = res.json().get('result').get('ticket_sn')
        else:
            pass

    @file_data()
    def test_add_ticket_2(self, payload):
        '''调用saasapi接口增加维修工单以便后面验证客服受理接口'''
        host = 'https://qa-saas.dding.net'
        payload['params']['faults'][0]['fault_time'] = Common.format_timestamp()
        res = Common.check(self, payload, host)
        Tickets.ticket2_id = res.json().get('result').get('id')
        Tickets.ticket2_sn = res.json().get('result').get('ticket_sn')

    @file_data()
    def test_reject_ticket(self, payload):
        '''打回工单'''
        payload['path'] = payload['path'].format(Tickets.ticket1_id)
        payload['params']['ticket_id'] = Tickets.ticket1_id
        Common.check(self, payload)

    @file_data()
    def test_service_ack(self, payload):
        '''客服受理工单'''
        payload['path'] = payload['path'].format(Tickets.ticket2_id)
        payload['params']['ticket_id'] = Tickets.ticket2_id
        Common.check(self, payload)

    @file_data()
    def test_add_ticket_3(self, payload):
        '''增加拆卸工单'''
        # payload['params']['faults'][0]['fault_time'] = Common.format_timestamp()
        res = Common.check(self, payload)
        Tickets.ticket3_id = res.json().get('result').get('id')
        Tickets.ticket3_sn = res.json().get('result').get('ticket_sn')

    @file_data()
    def test_add_ticket_4(self, payload):
        '''增加重装工单'''
        payload['params']['subscribe']['expected_time'] = Common.format_timestamp()
        res = Common.check(self, payload)
        Tickets.ticket4_id = res.json().get('result').get('id')
        Tickets.ticket4_sn = res.json().get('result').get('ticket_sn')

    def show_ticket(self, ticket_id, service_type, payload):
        '''工单详情'''
        tmp = payload.copy()
        tmp['path'] = tmp['path'].format(ticket_id)
        tmp['params']['service_type'] = service_type
        tmp['params']['ticket_id'] = ticket_id
        res = Common.check(self, tmp)
        return res

    @file_data()
    def test_show_tickets(self, payload):
        '''工单详情'''
        self.show_ticket(Tickets.ticket1_id, 1, payload)
        res = self.show_ticket(Tickets.ticket2_id, 2, payload)
        Tickets.ticket2_device_id = res.json().get('result').get('ticket_devices')[0].get('id')
        Tickets.ticket2_devices_device_id = res.json().get('result').get('ticket_devices')[0].get('device_id')
        Tickets.ticket2_room_id = res.json().get('result').get('ticket_devices')[0].get('room_id')
        res = self.show_ticket(Tickets.ticket3_id, 3, payload)
        Tickets.ticket3_device_id = res.json().get('result').get('ticket_devices')[0].get('id')
        self.show_ticket(Tickets.ticket4_id, 4, payload)

    def dispatch_ticket(self, ticket_id, device_id, payload):
        '''调度工单'''
        tmp = payload.copy()
        tmp['params']['ticket_list'][0]['ticket_id'] = ticket_id
        tmp['params']['ticket_list'][0]['ticket_devices'][0]['id'] = device_id
        Common.check(self, tmp)

    @file_data()
    def test_dispatch_ticket(self, payload):
        '''调度工单'''
        self.dispatch_ticket(Tickets.ticket2_id, Tickets.ticket2_device_id, payload)
        self.dispatch_ticket(Tickets.ticket3_id, Tickets.ticket3_device_id, payload)

    @file_data()
    def test_update_ticket_1(self, payload):
        '''编辑新装工单'''
        payload['path'] = payload['path'].format(Tickets.ticket1_id)
        payload['params']['subscribe']['expected_time'] = Common.format_timestamp() + 100000000
        Common.check(self, payload)

    @file_data()
    def test_update_ticket_2(self, payload):
        '''编辑维修工单'''
        payload['path'] = payload['path'].format(Tickets.ticket2_id)
        payload['params']['faults'][0]['id'] = Tickets.ticket2_device_id
        payload['params']['faults'][0]['ticket_id'] = Tickets.ticket2_id
        payload['params']['faults'][0]['fault_time'] = Common.format_timestamp() + 100000000
        Common.check(self, payload)

    @file_data()
    def test_update_ticket_3(self, payload):
        '''编辑拆卸工单'''
        payload['path'] = payload['path'].format(Tickets.ticket3_id)
        payload['params']['faults'][0]['id'] = Tickets.ticket3_device_id
        payload['params']['faults'][0]['ticket_id'] = Tickets.ticket3_id
        payload['params']['faults'][0]['fault_time'] = Common.format_timestamp() + 100000000
        Common.check(self, payload)

    @file_data()
    def test_update_ticket_4(self, payload):
        '''编辑重装工单'''
        payload['path'] = payload['path'].format(Tickets.ticket4_id)
        Common.check(self, payload)

    def ticket_history(self, ticket_id, payload):
        '''工单操作历史'''
        tmp = payload.copy()
        tmp['path'] = tmp['path'].format(ticket_id)
        Common.check(self, tmp)

    @file_data()
    def test_ticket_history(self, payload):
        '''工单操作历史'''
        self.ticket_history(Tickets.ticket1_id, payload)
        self.ticket_history(Tickets.ticket2_id, payload)
        self.ticket_history(Tickets.ticket3_id, payload)
        self.ticket_history(Tickets.ticket4_id, payload)

    def add_service_remark(self, ticket_id, payload):
        '''添加客服备注'''
        tmp = payload.copy()
        tmp['path'] = tmp['path'].format(ticket_id)
        tmp['params']['ticket_id'] = ticket_id
        Common.check(self, tmp)

    @file_data()
    def test_add_service_remark(self, payload):
        '''添加客服备注'''
        self.add_service_remark(Tickets.ticket1_id, payload)
        self.add_service_remark(Tickets.ticket2_id, payload)
        self.add_service_remark(Tickets.ticket3_id, payload)
        self.add_service_remark(Tickets.ticket4_id, payload)

    def get_service_remark(self, ticket_id, payload):
        '''查询客服备注'''
        tmp = payload.copy()
        tmp['path'] = tmp['path'].format(ticket_id)
        tmp['params']['ticket_id'] = ticket_id
        Common.check(self, tmp)

    @file_data()
    def test_get_service_remark(self, payload):
        '''查询客服备注'''
        self.get_service_remark(Tickets.ticket1_id, payload)
        self.get_service_remark(Tickets.ticket2_id, payload)
        self.get_service_remark(Tickets.ticket3_id, payload)
        self.get_service_remark(Tickets.ticket4_id, payload)

    def get_contract(self, ticket_id, payload):
        '''查询合同工单'''
        tmp = payload.copy()
        tmp['path'] = tmp['path'].format(ticket_id)
        tmp['params']['ticket_id'] = ticket_id
        Common.check(self, tmp)

    @file_data()
    def test_get_contract(self, payload):
        '''查询合同工单'''
        self.get_contract(Tickets.ticket1_id, payload)
        self.get_contract(Tickets.ticket2_id, payload)
        self.get_contract(Tickets.ticket3_id, payload)
        self.get_contract(Tickets.ticket4_id, payload)

    def match_contract(self, ticket_id, payload):
        '''工单匹配合同'''
        tmp = payload.copy()
        tmp['path'] = tmp['path'].format(ticket_id)
        tmp['params']['ticket_id'] = ticket_id
        Common.check(self, tmp)

    @file_data()
    def test_match_contract(self, payload):
        '''工单匹配合同'''
        self.match_contract(Tickets.ticket1_id, payload)
        self.match_contract(Tickets.ticket2_id, payload)
        self.match_contract(Tickets.ticket3_id, payload)
        self.match_contract(Tickets.ticket4_id, payload)

    @file_data()
    def test_check_state(self, payload):
        '''工单内绑定前查询要绑定的设备'''
        payload['path'] = payload['path'].format(Tickets.ticket1_id)
        Common.check(self, payload)

    def alloc_ticket(self, ticket_id, payload, device_id=0):
        '''指派工单'''
        tmp = payload.copy()
        tmp['params']['ticket_list'][0]['ticket_id'] = ticket_id
        tmp['params']['ticket_list'][0]['ticket_devices'][0]['id'] = device_id
        Common.check(self, tmp)

    @file_data()
    def test_alloc_ticket(self, payload):
        '''指派工单'''
        self.alloc_ticket(Tickets.ticket1_id, payload)
        self.alloc_ticket(Tickets.ticket1_lock_id, payload)
        self.alloc_ticket(Tickets.ticket2_id, payload, Tickets.ticket2_device_id)
        self.alloc_ticket(Tickets.ticket3_id, payload, Tickets.ticket3_device_id)
        self.alloc_ticket(Tickets.ticket4_id, payload)

    def home_position(self, ticket_id, payload):
        '''重标房源位置'''
        tmp = payload.copy()
        tmp['path'] = tmp['path'].format(ticket_id)
        tmp['params']['ticket_id'] = ticket_id
        Common.check(self, tmp)

    @file_data()
    def test_home_position(self, payload):
        '''重标房源位置'''
        self.home_position(Tickets.ticket1_id, payload)
        self.home_position(Tickets.ticket1_lock_id, payload)
        self.home_position(Tickets.ticket2_id, payload)
        self.home_position(Tickets.ticket3_id, payload)
        self.home_position(Tickets.ticket4_id, payload)

    def signin_position(self, ticket_id, payload):
        '''签到'''
        tmp = payload.copy()
        tmp['path'] = tmp['path'].format(ticket_id)
        tmp['params']['ticket_id'] = ticket_id
        Common.check(self, tmp)

    @file_data()
    def test_signin_position(self, payload):
        '''签到'''
        self.signin_position(Tickets.ticket1_id, payload)
        self.signin_position(Tickets.ticket1_lock_id, payload)
        self.signin_position(Tickets.ticket2_id, payload)
        self.signin_position(Tickets.ticket3_id, payload)
        self.signin_position(Tickets.ticket4_id, payload)

    def get_signin_position(self, ticket_id, payload):
        '''获取签到信息'''
        tmp = payload.copy()
        tmp['path'] = tmp['path'].format(ticket_id)
        tmp['params']['ticket_id'] = ticket_id
        Common.check(self, tmp)

    @file_data()
    def test_get_signin_position(self, payload):
        '''获取签到信息'''
        self.get_signin_position(Tickets.ticket1_id, payload)
        self.get_signin_position(Tickets.ticket2_id, payload)
        self.get_signin_position(Tickets.ticket3_id, payload)
        self.get_signin_position(Tickets.ticket4_id, payload)

    def accept_ticket(self, ticket_id, payload):
        '''确定预约时间'''
        tmp = payload.copy()
        tmp['path'] = tmp['path'].format(ticket_id)
        tmp['params']['appointment_time'] = Common.format_timestamp()
        tmp['params']['ticket_id'] = ticket_id
        Common.check(self, tmp)

    @file_data()
    def test_accept_ticket(self, payload):
        '''确定预约时间'''
        self.accept_ticket(Tickets.ticket1_id, payload)
        self.accept_ticket(Tickets.ticket2_id, payload)
        self.accept_ticket(Tickets.ticket3_id, payload)
        self.accept_ticket(Tickets.ticket4_id, payload)

    @file_data()
    def test_define_fault(self, payload):
        '''确定故障信息'''
        payload['path'] = payload['path'].format(Tickets.ticket2_id)
        payload['params']['faults'][0]['room_id'] = Tickets.ticket2_room_id
        payload['params']['faults'][0]['device_id'] = Tickets.ticket2_devices_device_id
        payload['params']['faults'][0]['id'] = Tickets.ticket2_device_id
        payload['params']['ticket_id'] = Tickets.ticket2_id
        Common.check(self, payload)

    @file_data()
    def test_get_define_fault(self, payload):
        '''获取最后一次工单错误解决方案'''
        payload['path'] = payload['path'].format(Tickets.ticket2_id)
        payload['params']['ticket_id'] = Tickets.ticket2_id
        payload['params']['room_id'] = Tickets.ticket2_room_id
        payload['params']['device_id'] = Tickets.ticket2_devices_device_id
        Common.check(self, payload)

    @file_data()
    def test_get_fault_id(self, payload):
        '''获取故障码列表'''
        faults = [1, 2, 3, 5, 6, 7]  # 1网关 2门锁 3电表 5水表网关 6/7水表
        # 二级故障id
        Tickets.second_faults = []
        for fault in faults:
            tmp = payload.copy()
            tmp['path'] = tmp['path'].format(fault)
            tmp['params']['device_type'] = str(fault)
            res = Common.check(self, tmp)
            for i in res.json().get('result'):
                for j in i.get('data'):
                    Tickets.second_faults.append(j.get('id'))
        print(Tickets.second_faults)

    @file_data()
    def test_get_solutions(self, payload):
        '''获取二级故障下的解决方案列表'''
        for fault in Tickets.second_faults:
            tmp = payload.copy()
            tmp['path'] = tmp['path'].format(fault)
            tmp['params']['fault_id'] = str(fault)
            Common.check(self, tmp)

    def submit_ticket(self, ticket_id, payload):
        '''提交工单'''
        tmp = payload.copy()
        tmp['path'] = tmp['path'].format(ticket_id)
        Common.check(self, tmp)

    @file_data()
    def test_submit_ticket(self, payload):
        '''提交工单'''
        self.submit_ticket(Tickets.ticket1_id, payload)
        self.submit_ticket(Tickets.ticket1_lock_id, payload)
        self.submit_ticket(Tickets.ticket2_id, payload)
        self.submit_ticket(Tickets.ticket3_id, payload)
        self.submit_ticket(Tickets.ticket4_id, payload)

    def turndown_ticket(self, ticket_id, payload):
        '''驳回工单'''
        tmp = payload.copy()
        tmp['path'] = tmp['path'].format(ticket_id)
        Common.check(self, tmp)

    @file_data()
    def test_turndown_ticket(self, payload):
        '''驳回工单'''
        self.turndown_ticket(Tickets.ticket1_id, payload)
        self.turndown_ticket(Tickets.ticket1_lock_id, payload)
        self.turndown_ticket(Tickets.ticket2_id, payload)
        self.turndown_ticket(Tickets.ticket3_id, payload)
        self.turndown_ticket(Tickets.ticket4_id, payload)

    def show_devices(self, ticket_id, payload):
        '''获取工单安装设备详细信息'''
        tmp = payload.copy()
        tmp['path'] = tmp['path'].format(ticket_id)
        Common.check(self, tmp)

    @file_data()
    def test_show_devices(self, payload):
        '''获取工单安装设备详细信息'''
        self.show_devices(Tickets.ticket1_id, payload)
        self.show_devices(Tickets.ticket2_id, payload)
        self.show_devices(Tickets.ticket3_id, payload)
        self.show_devices(Tickets.ticket4_id, payload)

    @file_data()
    def test_ensure_pays(self, payload):
        '''维修工单确定收费内容'''
        payload['path'] = payload['path'].format(Tickets.ticket2_id)
        Common.check(self, payload)

    @file_data()
    def test_unbind_gateways(self, payload):
        '''解绑网关'''
        payload['path'] = payload['path'].format(Tickets.ticket3_id)
        payload['params']['ticket_id'] = Tickets.ticket3_id
        Common.check(self, payload)

    @file_data()
    def test_bind_gateways(self, payload):
        '''绑定网关'''
        payload['path'] = payload['path'].format(Tickets.ticket1_id)
        payload['params']['ticket_id'] = Tickets.ticket1_id
        Common.check(self, payload)

    @file_data()
    def test_unbind_lock(self, payload):
        '''解绑无网关门锁'''
        payload['path'] = payload['path'].format(Tickets.ticket3_id)
        payload['params']['ticket_id'] = Tickets.ticket3_id
        Common.check(self, payload)

    @file_data()
    def test_bind_lock(self, payload):
        '''绑定无网关门锁'''
        payload['path'] = payload['path'].format(Tickets.ticket1_lock_id)
        payload['params']['ticket_id'] = Tickets.ticket1_lock_id
        Common.check(self, payload)

    def check_ticket(self, ticket_id, payload):
        '''验收工单'''
        tmp = payload.copy()
        tmp['path'] = tmp['path'].format(ticket_id)
        Common.check(self, tmp)

    @file_data()
    def test_check_ticket(self, payload):
        '''验收工单'''
        Common.rerun_case(self, 'test_submit_ticket_test_submit_ticket')
        self.check_ticket(Tickets.ticket1_id, payload)
        self.check_ticket(Tickets.ticket1_lock_id, payload)
        self.check_ticket(Tickets.ticket2_id, payload)
        self.check_ticket(Tickets.ticket3_id, payload)
        self.check_ticket(Tickets.ticket4_id, payload)

    def shut_ticket(self, ticket_id, payload):
        '''取消工单'''
        tmp = payload.copy()
        tmp['path'] = tmp['path'].format(ticket_id)
        Common.check(self, tmp)

    @file_data()
    def test_shut_ticket(self, payload):
        '''取消工单'''
        self.shut_ticket(Tickets.ticket1_id, payload)
        self.shut_ticket(Tickets.ticket1_lock_id, payload)
        self.shut_ticket(Tickets.ticket2_id, payload)
        self.shut_ticket(Tickets.ticket3_id, payload)
        self.shut_ticket(Tickets.ticket4_id, payload)

    @file_data()
    def test_duplicate_visit(self, payload):
        '''标记为二次上门'''
        payload['params']['ticket_ids'] = [Tickets.ticket1_id, Tickets.ticket2_id, Tickets.ticket3_id, Tickets.ticket4_id]
        Common.check(self, payload)
