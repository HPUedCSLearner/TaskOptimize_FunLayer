import sys
import os
uq_path    = os.environ['UQ_PATH']
db_path    = uq_path+'/DataBase/'
sys.path.append(db_path)
from fit_db_inter import *


modulename = 'CAS-ESM'
compset='B1850C5X'
res='fd14_licom'

fitcase_results = fitcase_search_records(modulename,compset,res)
fitcaseid = fitcase_results[0][0]
change_table_FITCASE(fitcaseid,None)
# print(fit_result)
# print(fitcase_results)
