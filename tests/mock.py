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
mock module
=========================

接口测试，用于健康模型构件的接口测试仿真。
同时也是phmMD中模型的参考实现（多线程）。
"""

# Author: Awen <26896225@qq.com>
# License: MIT

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from random import randint
from time import sleep
import uvicorn
import concurrent.futures

app = FastAPI()

# 支持跨越
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# IF11:REST MODEL 外部接口-phmMD与phmMS之间仿真接口


# time intensive tasks
@app.post("/api/v1/soh/{device_type}")
async def calculate_soh(device_type: str, dev_id: str):
    """模拟耗时的机器学习任务"""
    duration = randint(5, 10)
    # sleep(duration)   # will sleep 5 ~ 10 seconds
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))
    sleep(5)
    return {'public': True, 'id': 21, 'description': f'{duration}'}


if __name__ == '__main__':
    uvicorn.run('mock:app',                # noqa
                host="0.0.0.0",
                port=29082,
                workers=3
                )
