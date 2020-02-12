## case

- 按模块创建目录，存放测试用例py文件
- 测试用例文件名必须为test_*.py

## common

- 存放公共方法等
- common.py 公共方法
- HTMLTestRunner_PY3.py html格式测试报告工具
- my_ddt.py 重写的ddt数据驱动

## conf

- 配置信息
- conf.ini 不同环境地址以及账号密码等

## data

- 测试用例数据，json格式

- 必须与case目录结构相同且文件名相同，如case里登陆用例路径为case/login/test_login.py，则该用例的测试数据为data/login/test_login.json

- 在json文件中:

  - 第一级key值必须和对应的测试用例方法同名且必须一一对应
  - 必填字段：
    - path 接口地址
    - method 请求方法
    - check_res_code 响应码
    - check_res_data 响应数据
  - 最里层json为实际case数据

  

  

- 通用用例场景及用法：以房源模块为例，当所有用例都是只检测响应码或响应字段时，则只写一个case，对应的case和data如下：

  ```python
  #!/usr/bin/env python
  # -*- coding: utf-8 -*-
  import unittest
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
      def test_add_part_house(self, payload):
          '''添加分散式房源'''
          Homes.home_name = Homes.home_number = 'AutoTest{}'.format(Common.format_date())
          payload['params']['home_name'], payload['params']['number'] = Homes.home_name, Homes.home_number
          res = Common.check(self, payload)
          Homes.home_id = res.json().get('result').get('home_id')
  
      @file_data()
      def test_add_part_house_room(self, payload):
          '''添加分散式房源房间'''
          payload['path'] = payload['path'].format(Homes.home_id)
          Common.check(self, payload)
          self.test_0001_common_test_homes_list_test_common()
  
  ```

  ```json
  {
      "test_provinces": {
          "path": "/v3/provinces",
          
          "test_common": {
              "desc": "获取省份列表",
              "method": "get",
              "check_res_code": 0,
              "check_res_data": "res.json().get('result') != None"
          }
      },
  
      "test_homes_list": {
          "path": "/v3/homes",
          
          "test_common": {
              "desc": "获取房源列表",
              "method": "get",
              "params": {
                  "offset": 0,
                  "limit": 10
              },
              "check_res_code": 0,
              "check_res_data": "res.json().get('result') != None"
          }
      },
      
      "test_add_part_house": {
          "path": "/v3/homes",
          
          "test_add_part_house": {
              "desc": "添加分散式房源",
              "method": "post",
              "params": {
                  "client_id": 92091,
                  "country": "中国",
                  "home_type": 1,
                  "home_name": "{}",
                  "province": "广东省",
                  "city": "深圳市",
                  "district": "南山区",
                  "block": "波顿科技园",
                  "street": "茶光路南150米",
                  "number": "{}",
                  "lease_type": 1,
                  "description": "01"
                  },
              "check_res_code": 0,
              "check_res_data": "res.json().get('result').get('home_id') != None"
          },
          
          "test_common_add_exist_house": {
              "desc": "添加已存在的分散式房源",
              "method": "post",
              "params": {
                  "client_id": 92091,
                  "country": "中国",
                  "home_type": 1,
                  "home_name": "01",
                  "province": "广东省",
                  "city": "深圳市",
                  "district": "南山区",
                  "block": "波顿科技园",
                  "street": "茶光路南150米",
                  "number": "02",
                  "lease_type": 1,
                  "description": "01"
                  },
              "check_res_code": 400044,
              "check_res_data": "res.json().get('err_msg') == '房源名称已存在'"
          }
      },
      
      "test_add_part_house_room": {
          "path": "/v3/homes/{}/rooms",
          
          "test_add_part_house": {
              "desc": "添加分散式房源房间",
              "method": "post",
              "params": {"rooms": [{"name": "0001"}, {"name": "0002"}, {"name": "0003"}, {"name": "0004"}, {"name": "0005"}, {"name": "0006"}, {"name": "0007"}, {"name": "0008"}, {"name": "0009"}, {"name":"0010"}]},
              "check_res_code": 0,
              "check_res_data": ""
          }
      }
  }
  ```

  

## run.py

- 启动入口
- python run.py 或python run.py test 代表线下环境
- python run.py prod 代表线上环境