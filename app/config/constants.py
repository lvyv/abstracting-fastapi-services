#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2021 The CASICloud Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
# pylint: disable=invalid-name
# pylint: disable=missing-docstring

"""
=========================
constants module
=========================

定义所有常量。
"""

# Author: Awen <26896225@qq.com>
# License: MIT

# 所有后端的科学计算模型，phmMD类型
DEV_BATTERY = 'battery'
DEV_CELLPACK = 'cellpack'
DEV_CANNED_MOTOR_PUMP = 'canned motor pump'
DEV_CENTRIFUGAL_PUMP = 'centrifugal pump'
DEV_AC_FAN = 'air conditioner fan'
DEV_CHILLER = 'chiller'

# 各种状态常量
REQ_STATUS_PENDING = 'pending'
REQ_STATUS_SETTLED = 'settled'

# 后台ai模型的地址
REST_REQUEST_TIMEOUT = 1

# 后台ai模型的地址
AIURL_SOH = 'https://127.0.0.1:29082/api/v1/soh'

# phmMS启动的地址、端口、证书等
PHMMS_HOST = '0.0.0.0'
PHMMS_PORT = 29081
PHMMS_KEY = 'cert.key'
PHMMS_CER = 'cert.cer'
