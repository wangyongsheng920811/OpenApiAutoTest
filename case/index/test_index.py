#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from common.common import Common
from common.my_ddt import *


@ddt
class Index(unittest.TestCase):
    '''首页'''

    @file_data(common_test=1)
    def test_common(self, payload):
        '''通用测试'''
        Common.check(self, payload)
