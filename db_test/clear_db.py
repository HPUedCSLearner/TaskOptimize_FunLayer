import sys
import os
uq_path    = os.environ['UQ_PATH']
db_path    = uq_path+'/DataBase/'
sys.path.append(db_path)
from fit_db_inter import *


create_table_FIT()
create_table_FITCASE()