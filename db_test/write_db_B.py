import sys
import os
uq_path    = os.environ['UQ_PATH']
db_path    = uq_path+'/DataBase/'
sys.path.append(db_path)
from fit_db_inter import *
import json

# create_table_FIT()
# create_table_FITCASE()

modulename = 'CAS-ESM'
compset='B1850C5X'
res='fd14_licom'
componentmodel='atm lnd ocn ice'
config_ini_file = open('./casesm_config.ini.B', 'rb')
config_ini = config_ini_file.read()

config_ini_file.close()


layout = {}
layout['mintime'] = {'mintime': 748.9739217362039, 'submoduletime': {'atm': 707.4434588232617, 'ocn': 18.05076912205725, 'lnd': 23.28977215086786, 'ice': 23.47969379088503}, 'maxtasks': 128, 'pattern': '[(2,), (3, 4), (1,)]', 'ntasks': {'atm': 128, 'ocn': 127, 'lnd': 63, 'ice': 63}, 'roots': {'cpl': 0, 'atm': 0, 'ocn': 0, 'lnd': 0, 'ice': 63}}
layout['mincost'] = {'mincost': 92657.38983477459, 'maxtasks': 128, 'pattern': '[(2,), (3, 4), (1,)]', 'ntasks': {'atm': 116, 'ocn': 116, 'lnd': 58, 'ice': 56}, 'roots': {'cpl': 0, 'atm': 0, 'ocn': 0, 'lnd': 0, 'ice': 58}}
layout['nproc'] = 128

layout_tmp_file = open("./tmp.layout", "wb")
layout_tmp_file.write(str(layout).encode())
layout_tmp_file.write("\n".encode())
layout_tmp_file.close()


layout_tmp_file = open("./tmp.layout", "rb")
layout_tmp = layout_tmp_file.read()
layout_tmp_file.close()

fitcaseid = FITCASE_write(modulename,compset,res,componentmodel,config_ini,layout_tmp)

# fitcaseid = FITCASE_write(modulename,compset,res,componentmodel,config_ini)

parameters_data = json.load(open('./fit_parameters.json.B','r'))

submodule='atm'
parameters_atm = parameters_data[submodule]

#加上cplatm的参数
parameters_cplatm = parameters_data['cplatm']

for key in parameters_atm:
    tmp_parameter1= parameters_atm[key]['parameter']
    tmp_parameter2= parameters_cplatm[key]['parameter']
    tmp_parameter3 = []
    for i in range(len(tmp_parameter1)):
        tmp_parameter3.append(tmp_parameter1[i] + tmp_parameter2[i])
    parameters_atm[key]['parameter'] = tmp_parameter3

# print(parameters_atm)
FIT_write(fitcaseid,submodule,str(parameters_atm))

submodule = 'lnd'
parameters = str(parameters_data[submodule])
FIT_write(fitcaseid,submodule,parameters)

submodule = 'ocn'
parameters = str(parameters_data[submodule])
FIT_write(fitcaseid,submodule,parameters)

submodule = 'ice'
parameters = str(parameters_data[submodule])
FIT_write(fitcaseid,submodule,parameters)
