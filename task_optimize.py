# -*- coding: utf-8 -*-
import configparser
import csv
import sys
from xml.dom.minidom import parse
import time
import re
import numpy as np
import os
import math

curpath = os.path.split(os.path.realpath(__file__))[0]
load_balancing_path = curpath + '/layout_balancing'
sys.path.append(load_balancing_path)
import load_balancing_solve_jpl as lb
import sample_run

uq_path    = os.environ['UQ_PATH']
db_path    = uq_path+'/DataBase/'
sys.path.append(db_path)
script_path = uq_path + '/model_scripts/CAS-ESM/'
sys.path.append(script_path)

import casesm_run
from fit_db_inter import *

logfile=curpath + "/logs/TaskOptimize.log"
taskllog= open(logfile, "w")
sys.stdout = taskllog
def module_fit(x, a,b,c,d,e,f,g,h,i,j,k):
    return a/(x**2) + b / x +c*x**0.5 +  d*x + e*x**2 + f*x**3 + g*x**0.5*np.log(x) + h*x*np.log(x) + i*x**2*np.log(x) + j*np.log(x) + k

def fit_pre(module_data, preproc):
    module_parameter = []
    min_down = 9999
    max_up = 0
    min_key = "a"
    max_key = "b"
    for key in module_data:
        if module_data[key]["down"] < min_down:
            min_down = module_data[key]["down"]
            min_key = key
        if  module_data[key]["up"] > max_up:
            max_up =  module_data[key]["up"] 
            max_key = key
        if module_data[key]["down"] <= preproc and  module_data[key]["up"] > preproc:
            module_parameter=module_data[key]["parameter"]
    if not module_parameter:
        if preproc < min_down:
            module_parameter = module_data[min_key]["parameter"]
        elif preproc > max_up:
            module_parameter = module_data[max_key]["parameter"]
        else:
            print("error parameter!")
            return
    preresult = module_fit(preproc, module_parameter[0],module_parameter[1],module_parameter[2],module_parameter[3],module_parameter[4],module_parameter[5],module_parameter[6],module_parameter[7],module_parameter[8],module_parameter[9],module_parameter[10])
    return preresult
    
def layout_write_mintime(layout_dir, case_config_name, best_mintime):
    file_mintime = layout_dir + "/mintime.ini"
    case_config =  configparser.ConfigParser()
    case_config.read(case_config_name)
    
    ids = ['NTASKS_ATM', 'NTASKS_WRF','NTASKS_GEA','NTASKS_SRD','NTASKS_LND','NTASKS_ICE','NTASKS_OCN','NTASKS_CPL','NTASKS_GLC']
    
    
    #mintime
    ntasks1 = best_mintime['ntasks']
    roots1 = best_mintime['roots']
    maxproc1 = 1
    unuseid = ids.copy()
    
    for key in ntasks1:
        ntasks1[key] = int(ntasks1[key])
        if ntasks1[key] > maxproc1:
            maxproc1 = ntasks1[key]
    for key in ntasks1:
        id1 = 'NTASKS_' + key.upper()
        case_config.set('env_mach_pes', id1, str(ntasks1[key]))
        unuseid.remove(id1)
        id2 = 'ROOTPE_' + key.upper()
        case_config.set('env_mach_pes', id2, str(roots1[key]))
    for id in unuseid:
        case_config.set('env_mach_pes', id, str(maxproc1))
        case_config.set('env_mach_pes', 'ROOTPE_' + id[7:], '0')
    with open(file_mintime, 'w+') as f1:
        case_config.write(f1)
        
        
    return file_mintime

def layout_write_mincost(layout_dir, case_config_name,best_mincost):
    file_mincost = layout_dir + "/mincost.ini"
    case_config =  configparser.ConfigParser()
    case_config.read(case_config_name)
    
    ids = ['NTASKS_ATM', 'NTASKS_WRF','NTASKS_GEA','NTASKS_SRD','NTASKS_LND','NTASKS_ICE','NTASKS_OCN','NTASKS_CPL','NTASKS_GLC']
    
        
    #mincost
    ntasks2 = best_mincost['ntasks']
    roots2 = best_mincost['roots']
    maxproc2 = 1
    unuseid = ids.copy()
    
    for key in ntasks2:
        ntasks2[key] = int(ntasks2[key])
        if ntasks2[key] > maxproc2:
            maxproc2 = ntasks2[key]
    for key in ntasks2:
        id1 = 'NTASKS_' + key.upper()
        case_config.set('env_mach_pes', id1, str(ntasks2[key]))
        unuseid.remove(id1)
        id2 = 'ROOTPE_' + key.upper()
        case_config.set('env_mach_pes', id2, str(roots2[key]))
    for id in unuseid:
        case_config.set('env_mach_pes', id, str(maxproc2))
        case_config.set('env_mach_pes', 'ROOTPE_' + id[7:], '0')
    with open(file_mincost, 'w+') as f2:
        case_config.write(f2)
        
    return file_mincost

def layout_write_default(layout_dir, case_config_name, num_procs):
    #写入默认进程排布
    file_default = layout_dir + '/default.ini'
    case_config =  configparser.ConfigParser()
    case_config.read(case_config_name)
    ids = ['NTASKS_ATM', 'NTASKS_WRF','NTASKS_GEA','NTASKS_SRD','NTASKS_LND','NTASKS_ICE','NTASKS_OCN','NTASKS_CPL','NTASKS_GLC']
    for id in ids:
        case_config.set('env_mach_pes', id, str(num_procs))
        case_config.set('env_mach_pes', 'ROOTPE_' + id[7:], '0')
    with open(file_default, 'w+') as f:
        case_config.write(f)
    
    return file_default
     
def get_layout(case_config_name, force_sampling, mode, similar_layout,layout_dir, num_procs, sampling_days,sampling_modules, mintasks,max_npr_yz):
    #获取case配置
    case_config = configparser.ConfigParser()
    case_config.read(case_config_name)
    stop_option = case_config.get('env_run', 'STOP_OPTION')
    stop_n = case_config.getint('env_run', 'STOP_N')
    modelname = case_config.get('MODEL', 'modelname')
    compset = case_config.get('COMPSET', 'compset')
    res = case_config.get('RESOLUTION', 'res')
    casename = case_config.get('CASE', 'case')
    model_dir = case_config.get('MODEL_DIR','model_dir')
    uq_path    = os.environ['UQ_PATH']
    runpath   = uq_path+'/casesm_cases/'
    #在新case下运行，不更改用户原有case
    
    tmp_count = 1
    casename  = casename + '_opt'
    # if os.path.exists(runpath + '/' + casename):
    while os.path.exists(runpath + '/' + casename + str(tmp_count)):
        tmp_count += 1
    casename = casename + str(tmp_count)
    #获取实际module进程信息
    real_procs = {}
    for item in case_config.items('env_mach_pes'):
        if item[0][:6].upper() == 'NTASKS':
            real_procs[item[0][-3:].lower()] = int(item[1])
    case_config_tmp = configparser.ConfigParser()
    case_config_tmp.read(case_config_name)
    case_config_tmp.set("env_run", "STOP_OPTION", "nday")
    case_config_tmp.set("env_run", "STOP_N", str(sampling_days))
    case_config_tmp.set("CASE", "case", casename)
    case_config_path_tmp = curpath  + '/casesm_config_tmp.ini'
    
    with open(case_config_path_tmp, 'w+') as f:
        case_config_tmp.write(f)
    # try:
        # start_date = case_config.get('env_conf', 'RUN_STARTDATE')
        # stop_date = case_config.get('env_run', 'STOP_DATE')
        
    # except:
    #运行时间 换算为day
    model_time = -1
    if stop_option == 'nseconds' or stop_option == 'nsecond':
        model_time = stop_n / 86400
    elif stop_option == 'nminutes' or stop_option == 'nminute':
        model_time = stop_n / 1440
    elif stop_option == 'nhours' or stop_option == 'nhour':
        model_time = stop_n / 24
    elif stop_option == 'ndays' or stop_option == 'nday':
        model_time = stop_n
    elif stop_option == 'nmonths' or stop_option == 'nmonth':
        model_time = stop_n *30
    elif stop_option == 'nyears' or stop_option == 'nyear':
        model_time = stop_n *365
    # print("model_time: ", model_time)
    #case namelist
    case_sections = case_config.sections()
    case_namelistsections = []
    for case_section in case_sections:
        if case_section[-5:] == '_PARA' or case_section[-5:] ==  '_FILE' :
            case_namelistsections.append(case_section)
    case_namelists = {}
    for case_namelistsection in case_namelistsections:
        tmp_items = case_config.items(case_namelistsection)
        if tmp_items != []:
            case_namelists[case_namelistsection] = dict(tmp_items)
    
    fitcaseid = -1
    if force_sampling:
        print('force_sampling')
        sampling_procs = []
        tmp_modules = list(sampling_modules.keys())
        tmp_procs = len(sampling_modules[tmp_modules[0]])
        for i in range(tmp_procs):
            tmp_dir1= {}
            for tmp_module in tmp_modules:
                tmp_dir1[tmp_module] = sampling_modules[tmp_module][i]
            sampling_procs.append(tmp_dir1)

        print("sampling_procs", sampling_procs)
        fit_result = sample_run.sample_run(case_config_path_tmp,sampling_procs,max_npr_yz)
        os.chdir(curpath)
        
        
        submodules = list(fit_result.keys())
        fitparameters = {}
        for module in submodules:
            fitparameters[module] = eval(fit_result[module])
        #检查数据库中有无匹配算例，若无，写入数据库
        fitcase_search = []
        fitcase_results = fitcase_search_records(modelname,compset,res)
        if fitcase_results:
            for fitcase_result in fitcase_results:
                fitcase_config_file = open(curpath + "/tmp/fitcase.ini", "wb")
                fitcase_config_file.write(fitcase_result[2])
                fitcase_config_file.close()
                fitcase_config = configparser.ConfigParser()
                fitcase_config.read(curpath + "/tmp/fitcase.ini")
                fitcase_sections = fitcase_config.sections()
                fitcase_namelistsections = []
                for fitcase_section in fitcase_sections:
                    if fitcase_section[-5:] == '_PARA' or  fitcase_section[-5:] == '_FILE' :
                        fitcase_namelistsections.append(fitcase_section)
                fitcase_namelists = {}
                # print(fitcase_namelistsections)
                for fitcase_namelistsection in fitcase_namelistsections:
                    tmp_items = fitcase_config.items(fitcase_namelistsection)
                    if tmp_items != []:
                        fitcase_namelists[fitcase_namelistsection] = dict(tmp_items)
                # print('fitcase_namelists', fitcase_namelists)
                # print('case_namelists', case_namelists)
                #验证该判断是否合理
                if fitcase_namelists == case_namelists: #判断namelist是否一致
                    fitcase_search = fitcase_result
                    break
        # env_mach_name = layout_dir + '/env_mach_pes.xml'
        
        config_grid_file = model_dir + '/scripts/ccsm_utils/Case.template/config_grid.xml'
        domTree = parse(config_grid_file)
        rootNode = domTree.documentElement
        entrys = rootNode.getElementsByTagName('horiz_grid')
        glob_grid = {}
        for entry in entrys:
            if entry.getAttribute('GLOB_GRID'):
                glob_grid[entry.getAttribute('GLOB_GRID')] = {'nx': entry.getAttribute('nx'), 'ny':entry.getAttribute('ny')}
            if entry.getAttribute('SHORTNAME') == res:
                ice_grid = entry.getAttribute('ICE_GRID')
                # print(ice_grid)
        ice_nx = int(glob_grid[ice_grid]['nx'])
        ice_ny = int(glob_grid[ice_grid]['ny'])
        MAX_Blocks = ice_nx *ice_ny
        sushu=set()
        def getsushu(num):
            isZhishu = True
            i = 2
            square = int(math.sqrt(num)) + 1
            while i <= square:
                if num % i == 0:
                    sushu.add(i)
                    isZhishu = False
                    getsushu(num / i)
                    i += 1
                    break
                i += 1
            if isZhishu and num > 1:
                sushu.add(int(num))
        getsushu(MAX_Blocks)
        ice_procs = []
        for factor in range(4, num_procs +1):
            if MAX_Blocks % factor == 0:
                ice_procs.append(factor)
        if sushu == {2}:
            if num_procs >128:
                for i in range(4, 129):
                    if i not in ice_procs:
                        ice_procs.append(i)
            else:
                for i in range(4, num_procs+1):
                    if i not in ice_procs:
                        ice_procs.append(i)
        ice_procs = sorted(ice_procs)
            
        layout_time, layout_cost = lb.model_layout(num_procs, submodules, mintasks = mintasks,  fitparameters = fitparameters, ice_procs = ice_procs)
        if layout_time:
            file_mintime= layout_write_mintime(layout_dir, case_config_name, layout_time[1])
            if model_time != -1:
                pre_mintime = layout_time[1]['mintime'] / sampling_days * model_time
                print('时间最优方案排布\nntasks:  ', layout_time[1]['ntasks'], '\nroots: ', layout_time[1]['roots'], '\npre time: ', pre_mintime, 's')
            else:
                print('时间最优方案排布\nntasks:  ', layout_time[1]['ntasks'], '\nroots: ', layout_time[1]['roots'])
            print('最优方案写入配置文件\n时间最优方案配置文件: ', file_mintime)
        if layout_cost:
            file_mincost= layout_write_mincost(layout_dir, case_config_name, layout_cost[1])
            if model_time != -1:
                pre_mincost = layout_cost[1]['mincost'] / sampling_days * model_time
                print('机时最优方案排布\nntasks:  ', layout_cost[1]['ntasks'], '\nroots: ', layout_cost[1]['roots'], '\npre cost: ', pre_mincost, 's')
            else:
                print('机时最优方案排布\nntasks:  ', layout_cost[1]['ntasks'], '\nroots: ', layout_cost[1]['roots'])
            print('机时最优方案配置文件: ', file_mincost)
        if layout_time == None or layout_cost == None:
            if layout_time == None and layout_cost == None:
                file_default = layout_write_default(layout_dir,case_config_name, num_procs)
                print('注意：默认进程排布并不一定适合算例。若默认进程排布不匹配，请修改相应子模式进程数')
                print('默认进程排布配置文件:  ', file_default)
            return
        if layout_time == None or layout_cost == None:
            if fitcase_search == []:
                #数据库无匹配，写入数据库
                config_ini_file = open(case_config_name,"rb")
                config_ini_content = config_ini_file.read()
                config_ini_file.close()
                componentmodel = ' '.join(list(fit_result.keys()))
                
                fitcaseid = FITCASE_write(modelname,compset,res,componentmodel,config_ini_content)
                for k in fit_result.keys():
                    FIT_write(fitcaseid,k,fit_result[k])
        else:
            layout = {}
            layout['mintime'] = layout_time[1]
            layout['mincost'] = layout_cost[1]
            layout['nproc'] = num_procs
            if fitcase_search == []:
                #数据库无匹配，写入数据库
                config_ini_file = open(case_config_name,"rb")
                config_ini_content = config_ini_file.read()
                config_ini_file.close()
                componentmodel = ' '.join(list(fit_result.keys()))
                
                layout_tmp_file = open(curpath + "/tmp/tmp.layout", "wb")
                layout_tmp_file.write(str(layout).encode())
                layout_tmp_file.write("\n".encode())
                layout_tmp_file.close()
                
                layout_tmp_file = open(curpath + "/tmp/tmp.layout", "rb")
                layout_tmp = layout_tmp_file.read()
                layout_tmp_file.close()
                fitcaseid = FITCASE_write(modelname,compset,res,componentmodel,config_ini_content,layout_tmp)
                for k in fit_result.keys():
                    FIT_write(fitcaseid,k,fit_result[k])
            else:
                #排布数据写入数据库
                fitcaseid = fitcase_search[0]
                layout_tmp_file = open(curpath + "/tmp/tmp.layout", "wb")
                if fitcase_search[3] != None:
                    layout_tmp_file.write(fitcase_search[3])
                    layout_tmp_file.write(str(layout).encode())
                    layout_tmp_file.write("\n".encode())
                else:
                    layout_tmp_file.write(str(layout).encode())
                    layout_tmp_file.write("\n".encode())
                layout_tmp_file.close()
                
                layout_tmp_file = open(curpath + "/tmp/tmp.layout", "rb")
                layout_tmp = layout_tmp_file.read()
                layout_tmp_file.close()
                change_table_FITCASE(fitcaseid, layout_tmp)

    else:
        #从数据库中获取参数信息
        
        #fitcaseid 初始-1 默认进程排布 -2 采样 -3 模糊匹配 -4
        fitcase_results = fitcase_search_records(modelname,compset,res)
        fuzzymarch = fitcase_search_records(modelname,None,res)
        fitcase_search = []
        slowflog = 0 #判断是否采样
        if fitcase_results:
            for fitcase_result in fitcase_results:
            #比较namelist
            #比较namelist时，匹配成功如line48-67， 匹配失败先判断是否模糊匹配（mode），模糊匹配成功返回fitcaseid，失败返回-2 / (-2： 返回默认进程排布)
                #筛选namelist
                fitcase_config_file = open(curpath + "/tmp/fitcase.ini", "wb")
                fitcase_config_file.write(fitcase_result[2])
                fitcase_config_file.close()
                fitcase_config = configparser.ConfigParser()
                fitcase_config.read(curpath + "/tmp/fitcase.ini")
                fitcase_sections = fitcase_config.sections()
                fitcase_namelistsections = []
                for fitcase_section in fitcase_sections:
                    if fitcase_section[-5:] == '_PARA' or  fitcase_section[-5:] == '_FILE' :
                        fitcase_namelistsections.append(fitcase_section)
                fitcase_namelists = {}
                # print(fitcase_namelistsections)
                for fitcase_namelistsection in fitcase_namelistsections:
                    tmp_items = fitcase_config.items(fitcase_namelistsection)
                    if tmp_items != []:
                        fitcase_namelists[fitcase_namelistsection] = dict(tmp_items)
                # print('fitcase_namelists', fitcase_namelists)
                # print('case_namelists', case_namelists)
                #验证该判断是否合理
                if fitcase_namelists == case_namelists: #判断namelist是否一致
                    print("数据库有匹配算例")
                    if fitcase_result[3] != None:#数据库有排布数据时，返回layout
                    #数据库layout使用
                        layout_file = open(curpath + "/tmp/fitcase.layout", "wb")
                        layout_file.write(fitcase_result[3])
                        layout_file.close()
                        layout_file = open(curpath + "/tmp/fitcase.layout", "r")
                        layout = layout_file.read().split('\n')
                        layout_file.close()
                        while '' in  layout:
                            layout.remove('')
                        similars = []
                        for i in range(len(layout)):
                            tmp_layout = eval(layout[i])
                            if tmp_layout['nproc'] == num_procs:
                                print("获取匹配进程排布")
                                if model_time != -1:
                                    pre_mintime = tmp_layout['mintime']['mintime'] / sampling_days * model_time
                                    pre_mincost = tmp_layout['mincost']['mincost'] / sampling_days * model_time
                                    print('时间最优方案排布\nntasks:  ', tmp_layout['mintime']['ntasks'], '\nroots: ', tmp_layout['mintime']['roots'], '\npre time: ', pre_mintime, 's')
                                    
                                    print('机时最优方案排布\nntasks:  ', tmp_layout['mincost']['ntasks'], '\nroots: ', tmp_layout['mincost']['roots'], '\npre cost: ', pre_mincost, 's')
                                else:
                                    print('时间最优方案排布\nntasks:  ', tmp_layout['mintime']['ntasks'], '\nroots: ', tmp_layout['mintime']['roots'])
                                    
                                    print('机时最优方案排布\nntasks:  ', tmp_layout['mincost']['ntasks'], '\nroots: ', tmp_layout['mincost']['roots'])
                                #写入文件
                                file_mintime= layout_write_mintime(layout_dir, case_config_name, tmp_layout['mintime'])
                                file_mincost= layout_write_mincost(layout_dir, case_config_name, tmp_layout['mincost'])
                                print('最优方案写入配置文件\n时间最优方案配置文件: ', file_mintime, '\n机时最优方案配置文件: ', file_mincost)
                                return
                            distance = abs(tmp_layout['nproc'] - num_procs) / num_procs
                            #如果进程差小于10%，则视为相似进程
                            if distance < 0.10:
                                similars.append((i, distance))
                        #模糊匹配, 相同配置近似进程排布
                        if similar_layout and similars:
                            similars = sorted(similars, key= lambda x : x[1])
                            print("获取相似进程排布")
                            tmp_layout = eval(layout[similars[0][0]])
                            if model_time != -1:
                                pre_mintime = tmp_layout['mintime']['mintime'] / sampling_days * model_time
                                pre_mincost = tmp_layout['mincost']['mincost'] / sampling_days * model_time
                                print('时间最优方案排布\nntasks:  ', tmp_layout['mintime']['ntasks'], '\nroots: ', tmp_layout['mintime']['roots'], '\npre time: ', pre_mintime, 's')
                                
                                print('机时最优方案排布\nntasks:  ', tmp_layout['mincost']['ntasks'], '\nroots: ', tmp_layout['mincost']['roots'], '\npre cost: ', pre_mincost, 's')
                            else:
                                print('时间最优方案排布\nntasks:  ', tmp_layout['mintime']['ntasks'], '\nroots: ', tmp_layout['mintime']['roots'])
                                
                                print('机时最优方案排布\nntasks:  ', tmp_layout['mincost']['ntasks'], '\nroots: ', tmp_layout['mincost']['roots'])
                            #写入文件
                            file_mintime= layout_write_mintime(layout_dir, case_config_name, tmp_layout['mintime'])
                            file_mincost= layout_write_mincost(layout_dir, case_config_name, tmp_layout['mincost'])
                            print('最优方案写入配置文件\n时间最优方案配置文件: ', file_mintime, '\n机时最优方案配置文件: ', file_mincost)
                            return
                        else:
                            print("无相似进程排布")
                            fitcaseid = fitcase_result[0]
                            fitcase_search = fitcase_result
                            break
                    else:
                        print("数据库中无进程排布数据")
                        fitcaseid = fitcase_result[0]
                        fitcase_search = fitcase_result
                        break
                else: #namelist匹配失败, 判断是否模糊匹配, 当前case不匹配
                    if mode.lower() == 'fast' and fitcaseid < 0:
                        print("数据库中无匹配算例，获取相近算例")
                        fitcaseid = fitcase_result[0]
                        fitcase_search = fitcase_result
                        # break
                    elif mode.lower() == 'slow':
                        fitcaseid = -3
        elif fuzzymarch and mode.lower() == 'fast' and fitcaseid < 0:
            fitcaseid = -4
            # fuzzymarch.append(search_fitcase) #添加模糊匹配算例
        elif mode.lower() == 'fast' and fitcaseid < 0 and fitcaseid != -4:
            fitcaseid = -2
        elif mode.lower() == 'slow':
            fitcaseid = -3
        # print(fitcaseid)
        
        config_grid_file = model_dir + '/scripts/ccsm_utils/Case.template/config_grid.xml'
        domTree = parse(config_grid_file)
        rootNode = domTree.documentElement
        entrys = rootNode.getElementsByTagName('horiz_grid')
        glob_grid = {}
        for entry in entrys:
            if entry.getAttribute('GLOB_GRID'):
                glob_grid[entry.getAttribute('GLOB_GRID')] = {'nx': entry.getAttribute('nx'), 'ny':entry.getAttribute('ny')}
            if entry.getAttribute('SHORTNAME') == res:
                ice_grid = entry.getAttribute('ICE_GRID')
                # print(ice_grid)
        ice_nx = int(glob_grid[ice_grid]['nx'])
        ice_ny = int(glob_grid[ice_grid]['ny'])
        MAX_Blocks = ice_nx *ice_ny
        sushu=set()
        def getsushu(num):
            isZhishu = True
            i = 2
            square = int(math.sqrt(num)) + 1
            while i <= square:
                if num % i == 0:
                    sushu.add(i)
                    isZhishu = False
                    getsushu(num / i)
                    i += 1
                    break
                i += 1
            if isZhishu and num > 1:
                sushu.add(int(num))
        getsushu(MAX_Blocks)
        ice_procs = []
        for factor in range(4, num_procs +1):
            if MAX_Blocks % factor == 0:
                ice_procs.append(factor)
        if sushu == {2}:
            if num_procs >128:
                for i in range(4, 129):
                    if i not in ice_procs:
                        ice_procs.append(i)
            else:
                for i in range(4, num_procs+1):
                    if i not in ice_procs:
                        ice_procs.append(i)
        ice_procs = sorted(ice_procs)
            
        if fitcaseid == -2:
            # env_mach_name = layout_dir + '/default_env_mach_pes.xml'
            # lb.write_pe_template(env_mach_name, default_layout['ntasks'], default_layout['roots'], num_procs)
            file_default = layout_write_default(layout_dir, case_config_name, num_procs)
            print('模糊匹配失败，采用默认进程排布')
            print('注意：默认进程排布并不一定适合算例。若默认进程排布不匹配，请修改相应子模式进程数')
            print('默认进程排布配置文件:  ', file_default)
            return
            # return {'task_layout': env_mach_name}
        elif fitcaseid == -3:
            print('无匹配算例，进行采样')
            sampling_procs = []
            tmp_modules = list(sampling_modules.keys())
            tmp_procs = len(sampling_modules[tmp_modules[0]])
            for i in range(tmp_procs):
                tmp_dir1= {}
                for tmp_module in tmp_modules:
                    tmp_dir1[tmp_module] = sampling_modules[tmp_module][i]
                sampling_procs.append(tmp_dir1)
            print('准备采样')
            fit_result = sample_run.sample_run(case_config_path_tmp, sampling_procs,max_npr_yz)
            config_ini_file = open(case_config_path_tmp,"rb")
            config_ini_content = config_ini_file.read()
            config_ini_file.close()
            componentmodel = ' '.join(list(fit_result.keys()))
            fitcaseid = FITCASE_write(modelname,compset,res,componentmodel,config_ini_content)
            for k in fit_result.keys():
                FIT_write(fitcaseid,k,fit_result[k])
            
            slowflog = 1
        elif fitcaseid == -4:
            print('准备模糊匹配')
            #run case
            print("运行算例")
            #采样天下运行
            casesm_run.casesm_run(case_config_path_tmp)
            case_run_flag = 0
            while(not os.path.exists(runpath + '/' + casename + "/archive") and case_run_flag == 0):
                time.sleep(60)
                #检测是否运行失败
                tmp_value = os.system('grep -q "Model did not complete"  ' +runpath + '/' + casename + '/'+ casename+ '*')
                if tmp_value == 0:
                    case_run_flag = 1
            
            if case_run_flag == 1:
                print("运行失败, 返回默认进程排布")
                file_default = layout_write_default(layout_dir, case_config_name, num_procs)
                print('注意：默认进程排布并不一定适合算例。若默认进程排布不匹配，请修改相应子模式进程数')
                print('默认进程排布配置文件:  ', file_default)
                return
            print("运行成功")
            #use timing file
            command = "find " + runpath + "/" + casename + '/timing   '  + "-name  "  + '"ccsm_timing.' + casename + '.*"'
            ccsm_timing_file = os.popen(command).read().split('\n')[0]
            real_time = {}
            submodules = []
            with open(ccsm_timing_file, 'r') as ccsm_timing:
                for line in ccsm_timing:
                    if re.search(r'[\s\S]+Run Time:[\S\s]+myears/wday', line):
                        if not re.search(r'TOT Run Time:', line):
                            submodule = re.search(r'[\S\s]+Run Time', line).group()
                            submodule = submodule.strip().split(' ')[0]
                            sub_runtime = float(re.search(r"\d+.\d+", line).group())
                            if submodule != 'CPL' and sub_runtime != 0.0:
                                submodules.append(submodule.lower())
                                real_time[submodule.lower()] = sub_runtime
            #获取在nprocs下各模糊匹配算例各module的预测时间，找出与排布算例各模块最相近的预测函数参数进行组合
            fuzzymodule = {}
            print("组合模糊匹配算例")
            for submodule in submodules:
                fuzzymodule[submodule] = []
                for row in fuzzymarch:
                    fit_result=fit_search_records(row[0],submodule)
                    pre_module = {}
                    fitparameter = eval(fit_result)
                    pre_moduletime = fit_pre(fitparameter, real_procs[submodule])
                    pre_module['pre_moduletime'] = pre_moduletime
                    pre_module['fitparameter'] = fitparameter
                    fuzzymodule[submodule].append(pre_module)
            fitparameters = {}
            for submodule in fuzzymodule:
                pre_list = fuzzymodule[submodule]
                sub_runtime = real_time[submodule]
                for comb in pre_list:
                    comb['pre_moduletime'] = abs(comb['pre_moduletime'] - sub_runtime)
                pre_list = sorted(pre_list, key = lambda x:x['pre_moduletime'])
                fitparameters[submodule] = pre_list[0]['fitparameter']
            # print('fitparameters',fitparameters)
            # env_mach_name = layout_dir + '/env_mach_pes.xml'
            print("进程排布")
            layout_time, layout_cost = lb.model_layout(num_procs, submodules, mintasks = mintasks, fitparameters = fitparameters, ice_procs = ice_procs)
            if layout_time:
                file_mintime= layout_write_mintime(layout_dir, case_config_name, layout_time[1])
                if model_time != -1:
                    pre_mintime = layout_time[1]['mintime'] / sampling_days * model_time
                    print('时间最优方案排布\nntasks:  ', layout_time[1]['ntasks'], '\nroots: ', layout_time[1]['roots'], '\npre time: ', pre_mintime, 's')
                else:
                    print('时间最优方案排布\nntasks:  ', layout_time[1]['ntasks'], '\nroots: ', layout_time[1]['roots'])
                print('最优方案写入配置文件\n时间最优方案配置文件: ', file_mintime)
            if layout_cost:
                file_mincost= layout_write_mincost(layout_dir, case_config_name, layout_cost[1])
                if model_time != -1:
                    pre_mincost = layout_cost[1]['mincost'] / sampling_days * model_time
                    print('机时最优方案排布\nntasks:  ', layout_cost[1]['ntasks'], '\nroots: ', layout_cost[1]['roots'], '\npre cost: ', pre_mincost, 's')
                else:
                    print('机时最优方案排布\nntasks:  ', layout_cost[1]['ntasks'], '\nroots: ', layout_cost[1]['roots'])
                print('机时最优方案配置文件: ', file_mincost)
            if layout_time == None or layout_cost == None:
                if layout_time == None and layout_cost == None:
                    file_default = layout_write_default(layout_dir,case_config_name, num_procs)
                    print('注意：默认进程排布并不一定适合算例。若默认进程排布不匹配，请修改相应子模式进程数')
                    print('默认进程排布配置文件:  ', file_default)
                return
            return
            
        elif fitcaseid == -1:
            print('运行出错')
            return
        if fitcaseid >= 0: #匹配成功
            print('进程排布')
            fitparameters = {}
            if slowflog == 1:
                submodules = componentmodel.split(' ')
            else:
                submodules = fitcase_search[1].split(' ')
            for submodule in submodules:
                fitparameters[submodule] = eval(fit_search_records(fitcaseid, submodule))
            # env_mach_name = layout_dir + '/env_mach_pes.xml'
            print('参与排布的模式分量: ', ','.join(submodules))
            layout_time, layout_cost = lb.model_layout(num_procs, submodules, mintasks =mintasks,  fitparameters = fitparameters, ice_procs = ice_procs)
            if layout_time:
                file_mintime= layout_write_mintime(layout_dir, case_config_name, layout_time[1])
                if model_time != -1:
                    pre_mintime = layout_time[1]['mintime'] / sampling_days * model_time
                    print('时间最优方案排布\nntasks:  ', layout_time[1]['ntasks'], '\nroots: ', layout_time[1]['roots'], '\npre time: ', pre_mintime, 's')
                else:
                    print('时间最优方案排布\nntasks:  ', layout_time[1]['ntasks'], '\nroots: ', layout_time[1]['roots'])
                print('最优方案写入配置文件\n时间最优方案配置文件: ', file_mintime)
            if layout_cost:
                file_mincost= layout_write_mincost(layout_dir, case_config_name, layout_cost[1])
                if model_time != -1:
                    pre_mincost = layout_cost[1]['mincost'] / sampling_days * model_time
                    print('机时最优方案排布\nntasks:  ', layout_cost[1]['ntasks'], '\nroots: ', layout_cost[1]['roots'], '\npre cost: ', pre_mincost, 's')
                else:
                    print('机时最优方案排布\nntasks:  ', layout_cost[1]['ntasks'], '\nroots: ', layout_cost[1]['roots'])
                print('机时最优方案配置文件: ', file_mincost)
            if layout_time == None or layout_cost == None:
                if layout_time == None and layout_cost == None:
                    file_default = layout_write_default(layout_dir,case_config_name, num_procs)
                    print('注意：默认进程排布并不一定适合算例。若默认进程排布不匹配，请修改相应子模式进程数')
                    print('默认进程排布配置文件:  ', file_default)
                return
            #排布数据写入数据库
            if layout_cost and layout_time:
                layout = {}
                layout['mintime'] = layout_time[1]
                layout['mincost'] = layout_cost[1]
                layout['nproc'] = num_procs
                layout_tmp_file = open(curpath + "/tmp/tmp.layout", "wb")
                if fitcase_search and fitcase_search[3] != None:
                    layout_tmp_file.write(fitcase_search[3])
                    layout_tmp_file.write(str(layout).encode())
                    layout_tmp_file.write("\n".encode())
                else:
                    layout_tmp_file.write(str(layout).encode())
                    layout_tmp_file.write("\n".encode())
                layout_tmp_file.close()
                
                layout_tmp_file = open(curpath + "/tmp/tmp.layout", "rb")
                layout_tmp = layout_tmp_file.read()
                layout_tmp_file.close()
                change_table_FITCASE(fitcaseid, layout_tmp)
            return

def case_run(layout, case_config_name,max_npr_yz):
        
        case_config = configparser.ConfigParser()
        case_config.read(case_config_name)
        
        env_mach_pes = parse(layout['task_layout'])
        
        rootNode = env_mach_pes.documentElement
        entrys = rootNode.getElementsByTagName('entry')
        ntasks_atm = -1
        for entry in entrys:
            id = entry.getAttribute('id')
            value = entry.getAttribute('value')
            if id == 'NTASKS_ATM':
                ntasks_atm = int(value)
            if id[:6] == 'NTASKS' or id[:4] == 'ROOT' or id == 'MAX_TASKS_PER_NODE':
                case_config.set('env_mach_pes', id, value)
        
        npr_y = max_npr_yz
        npr_z = ntasks_atm
        while npr_z % npr_y != 0:
            npr_y -= 1
        npr_z = npr_z / npr_y
        case_config.set('CAM_PARA', 'npr_yz&spmd_iap_inparm', "%d,%d,%d,%d"%(npr_y,npr_z,npr_z,npr_y))
        case_config_ini = curpath  + '/casesm_config.ini'
        with open(case_config_ini, 'w+') as f:
            case_config.write(f)
        casesm_run.casesm_run(case_config_ini)
        print('Success run')

def schedule_optimize(layoutini):
    #主函数
    strtobool = lambda x :  True if x.upper() == 'TRUE' else False
    
    layout_config = configparser.ConfigParser()
    
    layout_config.read(layoutini)
    
    #获取layout配置
    case_config_name = layout_config.get('input', 'case_config')
    force_sampling = layout_config.get('input', 'force_sampling')
    mode = layout_config.get('input', 'mode')
    similar_layout = layout_config.get('input', 'similar_layout')
    layout_dir = layout_config.get('input', 'layout_dir')
    try:
        num_procs = layout_config.getint('input', 'process')
    except ValueError:
        print("process must be int ")
        return 
    assert os.path.exists(case_config_name), "case_config does not exist"
    assert os.path.exists(layout_dir), "layout_dir does not exist"
    
    assert force_sampling != '',  "force_sampling must be set"

    assert mode != '',  "mode must be set"
    assert mode == 'fast' or mode == 'slow', "mode must be fase or slow"
    assert similar_layout != '',  "similar_layout must be set"
    assert layout_dir != '',  "layout_dir must be set"
    assert case_config_name != '',  "case_config_name must be set"
    
    force_sampling = strtobool(force_sampling)
    similar_layout = strtobool(similar_layout)
    assert similar_layout == False or similar_layout == True, "similar_layout must be true or false"
    assert force_sampling == False or force_sampling == True, "force_sampling must be true or false"
    #sampling_days = layout_config.getint('input', 'samplingdays')
    sampling_days = 5 #默认5天采样
    mintasks = 16
    sampling_modules = {}
    max_npr_yz = -1
    #test use
    if force_sampling or mode == 'slow':
        try:
            max_npr_yz = layout_config.getint('sampling', 'max_npr_yz')
        except ValueError:
            print("max_npr_yz must be int ")
            return 
        numprocs_debug = set()
        for item in layout_config.items('sampling'):
            tmp_item = item[0].split('_',1)
            if len(tmp_item) == 2 and tmp_item[0] == "sampling":
                tmp_procs = item[1].split(',')
                numprocs_debug.add(len(tmp_procs))
                tmp_procs = [int(i) for i in tmp_procs]
                sampling_modules[tmp_item[1]] = tmp_procs
        assert len(numprocs_debug) == 1, 'The number of sampling processes must be the same for different modules!'
    
    get_layout(case_config_name, force_sampling, mode, similar_layout,layout_dir, num_procs, sampling_days, sampling_modules,mintasks, max_npr_yz)
    print("Run TaskOptimize successfully, the output is in TaskOptimize_FunLayer/T1/output_layout")
    return

try:
    myinput = sys.argv[1]
except IndexError:
    myinput = curpath + '/proc_layout.ini'

# print(input)
result = schedule_optimize(myinput)

taskllog.close()
# print(result)