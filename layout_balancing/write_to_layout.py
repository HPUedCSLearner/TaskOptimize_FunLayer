# -*- coding: UTF-8 -*-
import optimize_model
from scipy.optimize import minimize
import numpy as np

def sig(x,down,up):
    if x >= down and x < up :
        return 1
    else:
        return 0

def module_fit(xi, fitparameter):
    result = []
    for i in fitparameter:
        tmp_str = "sig({x},{down},{up})*({0}/({x}**2) + {1} / {x} +{2}*{x}**0.5 +  {3}*{x} + {4}*{x}**2 + {5}*{x}**3 + {6}*{x}**0.5*np.log({x}) + {7}*{x}*np.log({x}) + {8}*{x}**2*np.log({x}) + {9}*np.log({x}) + {10})".format(fitparameter[i]['parameter'][0], fitparameter[i]['parameter'][1],fitparameter[i]['parameter'][2], fitparameter[i]['parameter'][3], fitparameter[i]['parameter'][4], fitparameter[i]['parameter'][5], fitparameter[i]['parameter'][6], fitparameter[i]['parameter'][7], fitparameter[i]['parameter'][8], fitparameter[i]['parameter'][9], fitparameter[i]['parameter'][10], x = xi, down = fitparameter[i]['down'], up = fitparameter[i]['up'])
        result.append(tmp_str)
    return '+'.join(result)

def conduct_pattern(pattern):
    pattern_len = []
    for i in range(0,len(pattern)):
        pattern[i] = list(pattern[i])
        pattern[i].reverse()
        pattern_len.append(len(pattern[i]))
    tmp_len = pattern_len.copy()
    tmp_len.sort()
    while(tmp_len[0] != tmp_len[-1]):
        index = pattern_len.index(tmp_len[0]) #最小索引
        pattern_len[index] += 1
        pattern[index].insert(0, pattern[index][0])
        tmp_len = pattern_len.copy()
        tmp_len.sort()

def remove_same(pattern):
    if len(pattern) == 1:
        return False
    flag=True
    tmp1=pattern[0][0]
    for p in pattern:
        if p[0] != tmp1:
            flag = False
            break
    return flag

def max_prime(x):
    i = 1
    max_i = 1
    while i < x:
        i += 1
        if x % i == 0:
            x = x / i
            if max_i < i:
                max_i = i
            i  = 1
    return max_i

#机时最省容差
allowance = 0.00