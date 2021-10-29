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
controller layer
=========================

controller层，负责电池模型调用路由分发.
"""

# Author: Awen <26896225@qq.com>
# License: MIT

from fastapi import APIRouter, Depends
# from services.foo import FooService
from services.battery import BatteryService
# from schemas.foo import FooItem, FooItemCreate
from utils.service_result import handle_result
from config.database import get_db

router = APIRouter(
    prefix="/api/v1/phm/battery",
    tags=["电池模型"],
    responses={404: {"description": "Not found"}},
)


# 电池健康模型的前端接口，该层接口可以实现模型与调用方解耦，并添加负载均衡等扩展功能。
@router.post("/soh/{device_id}")
async def call_soh(device_id: str, db: get_db = Depends()):
    """
    健康评估模型

    :param device_id: 设备标识。
    :type: string。
    :param db: 数据库连接。
    :type: sqlalchemy.orm.sessionmaker。
    :return:
    :rtype:
    """
    bs = BatteryService(db)
    res = await bs.soh(device_id)
    # res2 = {'id': 3, 'success': True}
    return handle_result(res)


@router.post("/opmode/{device_id}")
async def call_opmode(device_id: str, sts: int, dts: int, taglist: str, db: get_db = Depends()):
    """
    工况判别模型

    :param device_id:
    :type: string
    :param sts:
    :type: int
    :param dts:
    :type: int
    :param taglist:
    :type: string
    :param db:
    :type:
    :return:
    :rtype:  ServiceResult
    """
    bs = BatteryService(db)
    res = await bs.soh(device_id)
    return handle_result(res)


# @router.post("/item/", response_model=FooItem)
# async def create_item(item: FooItemCreate, db: get_db = Depends()):
#     foos = FooService(db)
#     result = foos.create_item(item)
#     return handle_result(result)


# @router.put("/item/")
# async def update_item(reqid: str, res: str, db: get_db = Depends()):
#     foos = FooService(db)
#     result = foos.update_item(reqid, res)
#     return handle_result(result)
#
#
# @router.get("/item/{item_id}", response_model=FooItem)
# async def get_item(item_id: int, db: get_db = Depends()):
#     result = FooService(db).get_item(item_id)
#     return handle_result(result)
