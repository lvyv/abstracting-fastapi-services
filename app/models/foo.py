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
table data model module
=========================

数据库的表结构的映射模型。
"""

# Author: Awen <26896225@qq.com>
# License: MIT

from sqlalchemy import Boolean, Column, Integer, String

from config.database import Base


class FooItem(Base):
    __tablename__ = "foo_items"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    public = Column(Boolean, default=False)


class ReqItem(Base):
    """
    在phmMS收到REST调用时，创建一条记录，保存该异步请求，之后调用phmMD。
    在phmMD被调用启动的工作线程完成耗时计算后，反向回调phmMS，保存原来异步请求的执行结果。
    该表主要有三个字段：id记录请求号，每次调用都是唯一的；status是该请求的执行状态；result是请求执行的结果。
    Attributes
    ----------

    Methods
    -------

    """
    __tablename__ = "req_items"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    result = Column(String)
