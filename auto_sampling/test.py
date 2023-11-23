import sys
import os

uq_path    = os.environ['UQ_PATH']
db_path    = uq_path+'/DataBase/'
sys.path.append(db_path)
import db_init
import db_inter
import math

#---get scheduler name---#
ini = db_init.INI_search()[1:4]
if ini[0] == 1:
    arch  = ['SBATCH']
elif ini[1] == 1:
    arch  = ['PBS']
elif ini[2] ==1:
    arch  = ['BSUB']
else:
    print('No Scheduler specified') 
archs          = ['PBS','SBATCH','BSUB']
name_code      = ['-N','-J','-J']
procs_code     = ['-n','-N','-n']
queue_code     = ['-q','-p','-q']
out_code       = ['-o','-o','-o']
err_code       = ['-e','-e','-e']
arch_rm = set(archs).difference(set(arch))
case_name = "procs_test"
machine = "huan_intel"
num_procs = 334
qname = "normal"
case_path="/data/wujx01/EARthLab_UQ/TaskOptimize_FunLayer/auto_sampling/"
ntaskspernode=32

os.chdir("/data/wujx01/EARthLab_UQ/TaskOptimize_FunLayer/auto_sampling")

for i in arch_rm:
    os.system('sed -i '+"'"+'/#'+i+' -/d'+"'"+' ./*.run')
index   = archs.index(arch[0])

#---modify case name patition name and number of procs---#

#job casename
result = os.system('grep ' + '"'+arch[0]+' '+name_code[index]+'" '+case_name + '.' +machine+ '.run >> ./' + case_name + '.log 2>&1')
if result == 0:
    command   = 'sed -i '+"'"+'s/*#'+arch[0]+' '+name_code[index]+' '+case_name+'.*/#'+arch[0]+' '+name_code[index]+' '+case_name+'/g'+"' "+ case_name + '.' +machine+ '.run >> ./' + case_name + '.log 2>&1'
    os.system(command)

#num_procs
if arch == ['SBATCH']:
    num_node = str(int(math.ceil(int(num_procs) / ntaskspernode)))
    result = os.system('grep ' + '"'+arch[0]+' '+procs_code[index]+'" '+case_name+ '.' +machine+ '.run')
    if result == 0:
        command   = 'sed -i '+"'"+'s/#'+arch[0]+' '+procs_code[index]+'.*/#'+arch[0]+' '+procs_code[index]+' '+num_node+'/g'+"' "+ case_name + '.' +machine+ '.run'
        os.system(command)
    else:
        command = 'sed -i '+ '"/^#' + arch[0]+' '+name_code[index]+'.*'+'/a\\'  +'#'+arch[0]+' '+procs_code[index]+' '+num_node+'" ' + case_name + '.' +machine+ '.run'
        os.system(command)

#ntasks-per-node
if arch == ['SBATCH']:
    result = os.system('grep ' + '"^#'+arch[0]+' '+"--ntasks-per-node"+'" '+case_name+ '.' +machine+ '.run')
    if result == 0:
        command   = 'sed -i '+"'"+'s/^#'+arch[0]+' '+"--ntasks-per-node"+'.*/#'+arch[0]+' '+"--ntasks-per-node="+str(ntaskspernode)+'/g'+"' "+ case_name + '.' +machine+ '.run'
        os.system(command)
    else:
        command = 'sed -i '+ '"/^#' + arch[0]+' '+name_code[index]+'.*'+'/a\\'  +'#'+arch[0]+' '+"--ntasks-per-node="+str(ntaskspernode)+'" ' + case_name + '.' +machine+ '.run'
        os.system(command)


###---mark out two sections
#queue 
result = os.system('grep ' + '"'+arch[0]+' '+queue_code[index]+'" '+case_name+ '.' +machine+ '.run >> ./' + case_name + '.log 2>&1')
if result == 0:
    command   = 'sed -i '+"'"+'s/#'+arch[0]+' '+queue_code[index]+'.*/#'+arch[0]+' '+queue_code[index]+' '+qname+'/g'+"' "+ case_name + '.' +machine+ '.run >> ./' + case_name + '.log 2>&1'
    os.system(command)
else:
    command = 'sed -i '+ '"/^#' + arch[0]+' '+name_code[index]+'.*'+'/a\\'  +'#'+arch[0]+' '+queue_code[index]+' '+qname+'" ' + case_name + '.' +machine+ '.run >> ./' + case_name + '.log 2>&1'
    os.system(command)


#output
result = os.system('grep ' + '"'+arch[0]+' '+out_code[index]+'" '+case_name+ '.' +machine+ '.run >> ./' + case_name + '.log')
if result == 0:
    command   = 'sed -i '+"'"+'s/#'+arch[0]+' '+out_code[index]+'.*/#'+arch[0]+' '+out_code[index]+' '+case_path+ case_name+'/g'+"' "+ case_name + '.' +machine+ '.run >> ./' + case_name + '.log 2>&1'
    os.system(command)
else:
    command = 'sed -i '+ '"/^#' + arch[0]+' '+name_code[index]+'.*'+'/a\\'  +'#'+arch[0]+' '+out_code[index]+' '+case_path+'" ' + case_name + '.' +machine+ '.run >> ./' + case_name + '.log 2>&1'
    os.system(command)
