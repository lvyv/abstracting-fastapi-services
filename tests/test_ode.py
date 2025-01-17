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
unit test module
=========================

测试模型调度核心模块的入口主进程.
"""

# Author: Awen <26896225@qq.com>
# License: MIT

import logging
import unittest
from app import __version__

###############################################################################
#                          Libraries to use
###############################################################################
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import scipy.stats as stats
from scipy.integrate import odeint
from scipy.optimize import curve_fit


logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s %(filename)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S')


def test_version():
    assert __version__ == "0.1.0"


'''
###############################################################################
#                    General plot functions
###############################################################################

# Elimates the left and top lines and ticks in a matplotlib plot
def PlotStyle(Axes, Title):
    Axes.spines['top'].set_visible(False)
    Axes.spines['right'].set_visible(False)
    Axes.spines['bottom'].set_visible(True)
    Axes.spines['left'].set_visible(True)
    Axes.xaxis.set_tick_params(labelsize=14)
    Axes.yaxis.set_tick_params(labelsize=14)
    Axes.set_title(Title)


###############################################################################
#                    General Model Construction
###############################################################################

# Performs the dot produt to make the model
def MakeModel(MatrixCoeficients, InitialConditions):
    return np.dot(MatrixCoeficients, InitialConditions)


###############################################################################
#                              ODE system  solving
###############################################################################

SolverTime = np.linspace(0, 20, num=120)

# Model B Parameters
k1 = 0.3
k2 = 0.25
k3 = 0.1


# Coeficients matrix for model B
# Model B is refered as model02
def MakeModelMatrix02(K1, K2, K3):
    Matrix = np.zeros((3, 3))

    Matrix[0, 0] = -K1
    Matrix[0, 1] = K3

    Matrix[1, 0] = K1
    Matrix[1, 1] = -(K2 + K3)

    Matrix[2, 1] = K2

    return Matrix


Matrix02 = MakeModelMatrix02(k1, k2, k3)
InitialConditions = [0, 0, 0]


def KineticsSystem(InitialConditions, t, r, c):
    # res = MakeModel(Matrix02, InitialConditions)
    # return res
    r1, c1 = (2.4, 3)
    r2, c2 = (2.5, 3)
    r3, c3 = (3, 3)
    # if t < 3:
    #     i = t * 6
    # else:
    #     i = 18
    i = 18
    du1dt = (12 - InitialConditions[0] - i * r1) / (r1 * c1) + i / c1
    du2dt = (12 - InitialConditions[1] - i * r2) / (r2 * c2) + i / c2
    du3dt = (12 - InitialConditions[2] - i * r3) / (r3 * c3) + i / c3

    return [du1dt, du2dt, du3dt]


rr = 5
cc = 1
SystemSolution = odeint(KineticsSystem, InitialConditions, SolverTime, (rr, cc))

###############################################################################
#                    Visualization
###############################################################################

plt.figure(3, figsize=(9, 6))

plt.plot(SolverTime, SystemSolution[:, 0], 'b-', label='[A]',
         path_effects=[path_effects.SimpleLineShadow(alpha=0.2, rho=0.2),
                       path_effects.Normal()])
plt.plot(SolverTime, SystemSolution[:, 1], 'g-', label='[B]',
         path_effects=[path_effects.SimpleLineShadow(alpha=0.2, rho=0.2),
                       path_effects.Normal()])
plt.plot(SolverTime, SystemSolution[:, 2], 'm-', label='[C]',
         path_effects=[path_effects.SimpleLineShadow(alpha=0.2, rho=0.2),
                       path_effects.Normal()])

plt.xlabel('Time', fontsize=16, fontweight='bold')
plt.ylabel('Concentration', fontsize=16, fontweight='bold')
plt.legend(loc=0, fontsize=14)

ax = plt.gca()
PlotStyle(ax, '')
print('model created.')
pass


###############################################################################
#                            Data Generation
###############################################################################


def MakeNoisyData(Data, Noise):
    return [val + cal for val, cal in zip(Data, Noise)]


WhiteNoise = [np.random.uniform(low=-1, high=1) / 4 for val in SystemSolution[:, 2]]
WhiteSignal = MakeNoisyData(SystemSolution[:, 2], WhiteNoise)


###############################################################################
#                              ODE fitting
###############################################################################

def ModelSolver02(t, K1, K2, K3, InitialConditions):
    cK1 = K1
    cK2 = K2
    cK3 = K3

    cInit = InitialConditions

    cMatrix = MakeModelMatrix02(cK1, cK2, cK3)

    def LocalModel(cInit, t):
        return MakeModel(cMatrix, cInit)

    Solution = odeint(LocalModel, cInit, t)

    return Solution[:, 2]


def ModelSolution02(t, K1, K2, K3):
    return ModelSolver02(t, K1, K2, K3, InitialConditions)


Model02Params = curve_fit(ModelSolution02, SolverTime, WhiteSignal)

fK1 = Model02Params[0][0]
fK2 = Model02Params[0][1]
fK3 = Model02Params[0][2]

FitSolutionB = ModelSolution02(SolverTime, fK1, fK2, fK3)

###############################################################################
#                        Visualization
###############################################################################

plt.figure(4, figsize=(9, 6))

(markers, stemlines, baseline) = plt.stem(SolverTime, WhiteSignal, bottom=0, label='Data', basefmt=" ")
plt.setp(stemlines, linestyle="-", color="red", linewidth=0.5, alpha=0.5)
plt.setp(markers, color="red", alpha=0.75)

SolutionLabel = '[C]'
plt.plot(SolverTime, FitSolutionB, 'm-', label=SolutionLabel,
         path_effects=[path_effects.SimpleLineShadow(alpha=0.2, rho=0.2),
                       path_effects.Normal()])

plt.xlabel('Time', fontsize=16, fontweight='bold')
plt.ylabel('Concentration', fontsize=16, fontweight='bold')
plt.legend(loc=0, fontsize=14)

plt.ylim(0, 5.2)

ax = plt.gca()
PlotStyle(ax, '')

###############################################################################
#                    Residuals Statistical test
###############################################################################

ObRes = [signal - model for signal, model in zip(WhiteSignal, FitSolutionB)]

KS = stats.ks_2samp(ObRes, WhiteNoise)

print(KS)
'''


def model(y, t):
    dydt = -y + 1.0
    return dydt


def solve_ode():
    y0 = 0
    t = np.linspace(0, 5)
    y = odeint(model, y0, t)
    plt.plot(t, y)
    plt.xlabel('time')
    plt.ylabel('y(t)')
    plt.show()


# 需要拟合的函数
def f_1(x, A, B):
    return A * x + B


def fit_func():
    # 需要拟合的数据组
    x_group = np.array([3, 6.1, 9.1, 11.9, 14.9])
    y_group = np.array([0.0221, 0.0491, 0.0711, 0.0971, 0.1238])

    # 得到返回的A，B值
    A, B = curve_fit(f_1, x_group, y_group)[0]
    # 数据点与原先的进行画图比较
    plt.scatter(x_group, y_group, marker='o',label='real')
    x = np.arange(0, 15, 0.01)
    y = A * x + B
    plt.plot(x, y,color='red',label='curve_fit')
    plt.legend()
    plt.title('%.5fx%.5f=y' % (A, B))
    plt.show()


class TestMain(unittest.TestCase):
    """
    Tests for `健康模型构件` entrypoint.
    本测试案例启动整个健康模型构件（可以在数据资源集成分系统的算法开发软件中部署的模型协同工作）
    访问运行本案例的URL：
    https://IP:29081/docs，执行POST /subprocess，发送start/stop命令启停视频识别流水线。
    注意
    """
    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_Main(self):
        """Test app.main:app"""
        logging.info(f'********************  CASICLOUD AI METER services  ********************')
        logging.info(f'phmMD test started.')
        solve_ode()
        fit_func()


if __name__ == "__main__":
    unittest.main()
