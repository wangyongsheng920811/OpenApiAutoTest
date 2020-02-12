#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests


class Common(object):
    '''manage api 测试公共方法'''
    host = None
    headers = None

    @classmethod
    def init(cls, section):
        '''启动时初始化，根据conf.ini获取对应环境地址、用户名和密码并登录，获取token'''
        from configparser import ConfigParser
        if 'prod' in section:
            cls.section = 'prod'
        else:
            cls.section = 'qa'
        reader = ConfigParser()
        reader.read('conf/conf.ini')
        d = {key: value for key, value in reader.items(cls.section)}
        cls.host = d.get('host')
        headers = {'Origin': 'http://local.dding.cn'}
        payload = {
            'name': d.get('user_name'),
            'pass': d.get('password'),
            'from': '2'
        }
        res = requests.post(url=d.get('login_url'), json=payload, headers=headers)
        try:
            cls.headers = {'Cookie': res.headers.get('set-cookie')}
        except Exception as e:
            print('无法获取token')

    @classmethod
    def init_homes(cls, section):
        '''测试房源初始化，根据conf.ini获取对应openapi环境地址、用户信息，获取token，删除不必要的房源信息'''
        from configparser import ConfigParser
        if 'prod' in section:
            cls.section = 'prod'
        else:
            cls.section = 'qa'
        reader = ConfigParser()
        reader.read('conf/conf.ini')
        d = {key: value for key, value in reader.items(cls.section)}
        openapi_host = d.get('openapi_host')
        client_id = d.get('client_id')
        client_secret = d.get('client_secret')
        res_token = requests.post(url=openapi_host + '/v2/access_token', json={'client_id': client_id, 'client_secret': client_secret})
        try:
            token = res_token.json()['access_token']
        except Exception as e:
            print('获取openapi的token失败', e)
            return
        res_home_list = requests.get(url=openapi_host + '/v2/search_home_info', params={'access_token': token, 'offset': 0, 'count': 50})
        for home_tmp in res_home_list.json()['home_list']:
            if (not home_tmp['devices']) and (home_tmp['home_name'].find('OpenAPI') == -1):
                requests.post(url=openapi_host + '/v2/del_home', json={'access_token': token, 'home_id': home_tmp['home_id']})
        return

    @classmethod
    def request(cls, payload, host):
        '''请求方法，根据对应用例json数据里的method字段发起对应请求'''
        if host:
            url = host + payload.get('path')
        else:
            url = cls.host + payload.get('path')
        data = payload.get('params')
        print('\n')
        print('url:', url)
        print('method:', payload.get('method'))
        print('headers:', cls.headers)
        print('data:', data)
        return getattr(requests, payload.get('method'))(url=url, params=data, json=data, headers=cls.headers)

    @classmethod
    def check(cls, test_cls, datas, host=None):
        '''公用检测方法，检测请求结果响应码和响应数据是否和json一致
           检测用例json数据中是否有path、method、check_res_code和check_res_data字段'''
        test_cls.assertIn('path', datas)
        test_cls.assertIn('method', datas)
        test_cls.assertIn(datas.get('method'), ['get', 'post', 'put', 'delete'])
        test_cls.assertIn('check_res_code', datas)
        test_cls.assertIn('check_res_data', datas)
        res = cls.request(datas, host)
        check_res_code = datas.get('check_res_code')
        check_res_data = datas.get('check_res_data')
        try:
            print('response:', res.json())
        except Exception as e:
            print('exception: %s\nresponse响应码: %d' % (e, res.status_code))
        print('check_res_code:', check_res_code)
        print('check_res_data:', check_res_data)
        print('\n')
        if check_res_code is not None:
            test_cls.assertEqual(res.json().get('err_code'), check_res_code, msg=res.json())
        if check_res_data:
            test_cls.assertTrue(eval(check_res_data), msg=check_res_data)
        return res

    @staticmethod
    def random_list(l):
        '''返回列表中随机个元素'''
        import random
        return random.sample(l, random.randint(1, len(l)))

    @staticmethod
    def format_date():
        '''返回当前时间字符串，如20190723161620'''
        import time
        return str(time.strftime("%Y%m%d%H%M%S", time.localtime()))

    @staticmethod
    def format_timestamp(ms=1000, day=-0):
        '''返回毫秒级时间戳，如1574217971977'''
        import time
        return int(ms * (time.time() + day * 24 * 60 * 60))

    @staticmethod
    def check_list_dic(data, source):
        '''判断source中是否有data'''
        if isinstance(source, list):
            if data in source:
                return True
            else:
                for tmp_list in source:
                    if Common.check_list_dic(data, tmp_list):
                        return True
                    else:
                        continue
        elif isinstance(source, dict):
            if data in source.values():
                return True
            else:
                for tmp_dic in source:
                    if Common.check_list_dic(data, tmp_dic):
                        return True
                    else:
                        continue
        return False

    @staticmethod
    def dd_robot(success_count, failure_count, error_count):
        hook = r'https://oapi.dingtalk.com/robot/send?access_token=dc7c20ebd64bb47c4d9e70577f2b7e443b53fca7b7aa4235dfb6a1a78186f022'
        report_url = 'http://qa-ci.dding.net:8081/jenkins/view/5.0/job/hyperloop-auto-test-pipeline/Hyperloop_20Test_20Report'
        content = '''
            接口自动化:  成功: {},  失败: {},  错误: {}
            点击查看详情
            {}
            '''.format(success_count, failure_count, error_count, report_url)
        atMobiles = '18640573589'
        message = {
            'msgtype': 'text',
            'text': {'content': content},
            'at': {'atMobiles': [atMobiles], 'isAtAll': False}
        }
        requests.post(url=hook, json=message)

    @staticmethod
    def rerun_case(test_cls, case_name):
        '''
            用例内部调用，如用例test1包含两个场景case1和case2
            在test2中调用test1的case1则通过如下方式再次跑一次case1：
            Common.rerun_case(self, 'test1_case1')
            或者在test2中调用test1中所有case：
            Common.rerun_case(self, 'test1')
        '''
        test_cls.assertTrue(hasattr(test_cls, 'CASE_NAMES'), msg='class has no CASE_NAMES')
        flag = False
        for i in test_cls.CASE_NAMES:
            if case_name in i[:4] + i[9:]:
                flag = True
                print('rerun_case: ', i)
                getattr(test_cls, i)()
        test_cls.assertTrue(flag, msg=case_name + ' not exsit')
