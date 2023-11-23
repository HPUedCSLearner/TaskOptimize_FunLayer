import os
import sys
uq_path    = os.environ['UQ_PATH']
script_path = uq_path + '/model_scripts/CAS-ESM/'
sys.path.append(script_path)

import casesm_run

casesm_run.casesm_run("/data/wujx01/EARthLab_UQ/TaskOptimize_FunLayer/case_config/casesm_config.ini.BNCH")