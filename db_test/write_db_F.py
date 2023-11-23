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
compset='FAMIPC5X'
res='fd14_fd14'
componentmodel='atm lnd ocn ice'
config_ini_file = open('./casesm_config.ini.F', 'rb')
config_ini = config_ini_file.read()

config_ini_file.close()


fitcaseid = FITCASE_write(modulename,compset,res,componentmodel,config_ini)

parameters_data = json.load(open('./fit_parameters.json.F','r'))

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
