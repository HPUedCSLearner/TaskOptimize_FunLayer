#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 14:12:55 2020

@author: wujiexia

This is to read configure file and create shell scripts for CAS-ESM runs (F&B COMPSET TESTED)

"""
def sample_run (configini,procs,max_npr_yz):

    import os
    import configparser
    import shutil
    import sys

    uq_path    = os.environ['UQ_PATH']
    db_path    = uq_path+'/DataBase/'
    sys.path.append(db_path)
    import db_init
    import db_inter
    curpath = os.path.split(os.path.realpath(__file__))[0]
    auto_sampling_path = curpath + '/auto_sampling'
    sys.path.append(auto_sampling_path)
    import auto_sampling
    
    #initialization
    config = configparser.ConfigParser()

    
    config.read(configini)
    model_dir  = config.get('MODEL_DIR','model_dir')
    
    #######################
    #---start CESM run---#
    #######################

    compset    = str.upper(config.get('COMPSET','compset'))
    res        = str.lower(config.get('RESOLUTION','res'))
    mach       = config.get('MACHINE','mach')
    case       = config.get('CASE','case')
    qname      = config.get('QNAME','qname')
    nml_path    = config.get('NML_DIR','nml_dir')
    run_path   = uq_path+'/casesm_cases/'
    
    if os.path.exists(run_path+case):
        shutil.rmtree(run_path+case)
    os.chdir(model_dir + '/scripts/')
    
    #---create a new case---#
    command    = './create_newcase -case ' + run_path +'/'+case + ' -compset ' + compset + ' -res ' + res + ' -mach '+ mach + ' >' +run_path+'/'+case+'.log 2>&1'
    os.system(command)


    #---setup the model---#
    os.chdir(run_path + case)
    os.system('mv '+run_path+'/'+case+'.log ./'+case+'.log')
  
    #env_config
    os.system('cp '+nml_path+'/*.xml ./')
    for items in config.items('env_conf'):
        command='./xmlchange -file env_conf.xml -id ' + str.upper(items[0])+' -val '+items[1]
        os.system(command)
    shutil.copyfile(configini,'./casesm_config.ini')    
    #env_build
    for items in config.items('env_build'):
        command='./xmlchange -file env_build.xml -id ' + str.upper(items[0])+' -val '+items[1]
        os.system(command)
    command='./xmlchange -file env_build.xml -id EXEROOT -val '+run_path+'/'+case+'/build/' 
    os.system(command)

    #env_mach
    for items in config.items('env_mach_pes'):
        command='./xmlchange -file env_mach_pes.xml -id ' + str.upper(items[0])+' -val '+items[1]
        os.system(command)   

    command    = './configure -case >> ./' + case + '.log 2>&1'
    os.system(command)
    os.system('cp ./env_conf.xml ./LockedFiles/env_conf.xml.locked')
    os.system('cp ./env_mach_pes.xml ./LockedFiles/env_mach_pes.xml.locked')
    
    #############################
    #---read namelist changes---#
    #############################
    
    os.system('cp '+nml_path+'/*.csh '+run_path+case+'/Buildconf/')   

    #---modify namelists PARA---#
    models=['cam','colm','licom','cice']
    section=['CAM','COLM','LICOM','CICE']
    subgroup=['atm_in','lnd_in','LICOM_IN','ice_in']

    for index in range(0,3):

        if (os.path.exists('./Buildconf/'+models[index]+'.buildnml.csh')):
            for items in config.items(section[index]+'_PARA'):
                namelist=items[0].split("&",1)

    #match namelist group name#
                command='grep "'+'&'+namelist[1]+'" '+run_path+case+'/Buildconf/'+models[index]+'.buildnml.csh >> ./' + case + '.log  2>&1'
                result_nl = os.system(command)
                if result_nl == 256:
                    command = 'sed -i '+ '"' + '/^cat >! ' + subgroup[index] + ' << EOF'+'/a\\'  + '&' + namelist[1] + '" ' +run_path+case+ '/Buildconf/'+models[index]+'.buildnml.csh >> ./' + case + '.log 2>&1'
                    os.system(command)
                    command = 'sed -i '+ '"/&' + namelist[1]+'/a\\'  + '\/" ' +run_path+case+ '/Buildconf/'+models[index]+'.buildnml.csh >> ./' + case + '.log 2>&1'
                    os.system(command)

    #match parameter name#
                result_para = os.system('grep '+'"'+namelist[0]+'" '+run_path+case+'/Buildconf/'+models[index]+'.buildnml.csh >> ./' + case + '.log 2>&1')
                if result_para == 256:
                    command = 'sed -i '+ '"' + '/^&'+namelist[1]+'/a\\ '  + namelist[0] + ' = ' + items[1]+  '" ' +run_path+case+'/Buildconf/'+models[index]+'.buildnml.csh >> ./' + case + '.log 2>&1'
                    os.system(command)
                else:   
                    os.system('sed -i ' + '"' + 's/'+namelist[0]+ ' .*/ ' + namelist[0] + ' = ' + items[1] + '/g' + '" ' + run_path+case+ '/Buildconf/'+models[index]+'.buildnml.csh >> ./' + case + '.log 2>&1')
                    os.system('sed -i ' + '"' + 's/'+namelist[0]+ '=.*/ ' + namelist[0] + ' = ' + items[1] + '/g' + '" ' + run_path+case+ '/Buildconf/'+models[index]+'.buildnml.csh >> ./' + case + '.log 2>&1') 

    #---modify namelist FILE---#

            for items in config.items(section[index]+'_FILE'):
                namelist=items[0].split("&",1)

    #match namelist group name#
                result_nl = os.system('grep "'+'&'+namelist[1]+'" '+ run_path+case+'/Buildconf/'+models[index]+'.buildnml.csh >> ./' + case + '.log 2>&1')

                if result_nl == 256:
                    command = 'sed -i '+ '"' + '/^cat >! '+ subgroup[index] + '<< EOF'+'/a\\ '  + '&' + namelist[1] + '" ' + run_path+case+ '/Buildconf/'+models[index]+'.buildnml.csh >> ./' + case + '.log 2>&1'
                    os.system(command)
                    command = 'sed -i '+ '"/&' + namelist[1]+'/a\\'  + '\/" ' + run_path+case+ '/Buildconf/'+models[index]+'.buildnml.csh >> ./' + case + '.log 2>&1'
                    os.system(command)

    #match parameter name#
                result_para = os.system('grep '+'"'+namelist[0]+'" '+ run_path+case+'/Buildconf/'+models[index]+'.buildnml.csh >> ./' + case + '.log 2>&1')
                if result_para == 256:
                    command = 'sed -i '+ '"' + '#&'+namelist[1]+'#a\\ '  + namelist[0] + ' = ' + items[1]+  '" ' + run_path+case+ '/Buildconf/'+models[index]+'.buildnml.csh >> ./' + case + '.log 2>&1'
                    os.system(command)
                else:
                    os.system('sed -i ' + '"' + 's#'+namelist[0]+ ' .*# ' + namelist[0] + ' = ' + items[1] + '#g' + '" ' + run_path+case+ '/Buildconf/'+models[index]+'.buildnml.csh >> ./' + case + '.log 2>&1')
                    os.system('sed -i ' + '"' + 's#'+namelist[0]+ '\t.*# ' + namelist[0] + ' = ' + items[1] + '#g' + '" ' + run_path+case+'/Buildconf/'+models[index]+'.buildnml.csh >> ./' + case + '.log 2>&1')
                    os.system('sed -i ' + '"' + 's#'+namelist[0]+ '=.*# ' + namelist[0] + ' = ' + items[1] + '#g' + '" ' + run_path+case+ '/Buildconf/'+models[index]+'.buildnml.csh >> ./' + case + '.log 2>&1')
        else:
            print(models[index]+' is not active')


    #SPPT source code copy#
    for items in config.items('sppt_src'):
        command='cp ' + items[1] + '/*.F90 ' + run_path + case+ '/SourceMods/src.cam/'
        os.system(command)

    #############
    #---build---#
    #############
    # command='./'+case+'.'+mach+'.build >> ./' + case + '.log 2>&1'
    # os.system(command)
    
    #################
    #---xmlchange---#
    #################

    #---env_run---#
    
    for items in config.items('env_run'):
        command='./xmlchange -file env_run.xml -id ' + str.upper(items[0])+' -val '+items[1]
        os.system(command)
    archive_loc = run_path+case+'/archive/'
    command='./xmlchange -file env_run.xml -id DOUT_S_ROOT -val '+archive_loc
    os.system(command)
    
    #env_conf #env_conf must be changed before ./configure, file locked afterwards
    command='cp ./LockedFiles/env_conf.xml.locked ./env_conf.xml'
    os.system(command)
 
    #---env_case---#
    for items in config.items('env_case'):
        command='./xmlchange -file env_case.xml -id ' + str.upper(items[0])+' -val '+items[1]
        os.system(command)
    
    
    #BGM copy restart files
    for items in config.items('bgm_restart'):
        command='cp ' + items[1] + '/*.nc ' + run_path + case+ '/build/run/'
        os.system(command)
    
    #SPPT source code copy#
    for items in config.items('sppt_src'):
        command='cp ' + items[1] + '/*.F90 ' + run_path + case+ '/SourceMods/src.cam/'
        os.system(command)

    print('sampling......')
    fit_result = auto_sampling.sampling(run_path + '/' + case, mach, model_dir, case, procs,qname, max_npr_yz)

    return fit_result
    
