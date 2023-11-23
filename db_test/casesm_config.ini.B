#####################################
#User's configuration file
#####################################

###----------------------Required section-----------------------###
#for CAS-ESM runs,all sections are required
#---model selection--#

[BASE]
uq_path                      =/data/wujx01/EARthLab_UQ/ 
[MODEL]
modelname                    = CAS-ESM
[MODEL_DIR]
#do not include scripts or models
model_dir                    =/data/wujx01//cas-esm_new/
#testcases FAMIPC5X fd14_fd14, B1850C5X fd14_licom
[COMPSET]
compset                      = B1850C5X
[RESOLUTION]
res                          = fd14_licom
[CASE]
case                         = jpl_B1
[MACHINE]
mach             	     = huan_intel
[QNAME]
qname                        = normal
[NUM_PROCS]
num_procs                    = 128
[NML_DIR]
nml_dir                      =/data/wujx01/EARthLab_UQ/TaskOptimize_FunLayer/case_config/nml_jpl_b

###----------------------end of required section----------------------###

##########################
#---namelist
##########################

#---ATMOSPHERE---#

###---CAM /Buildconf/cam.buildnml.csh---###

[CAM_PARA] 

mfilt&cam_inparm                              = 1,30,30,30,30,30
nhtfrq&cam_inparm                             = 0,-24,-24,-24,-24
fexcl1&cam_inparm                             = 'DTH','DTV','UU','VV'
fincl2&cam_inparm                             = 'U:A','PS:A','TS:A','PRECT:A','FLUT:A'

[CAM_FILE]


#---LAND---#
###---COLM /Buildconf/colm.buildnml.csh---###

[COLM_PARA]
###############################################################
#for Bcompset; unmark this section if running fd14_licom
###############################################################

fsrf&clmexp                               = 'CoLM-srf-IAP-CMIP-128x256'
flai&clmexp                               = 'CoLM-lai-IAP-CMIP-128x256'
fini&clmexp                               = 'CoLM-ini-IAP-CMIP-128x256'
fsbc&clmexp                               = 'CoLM-sbc-IAP-CMIP-128x256'

###############################################################
####end###
###############################################################


[COLM_FILE]


###---CLM /Buildconf/clm.buildnml.csh---###
                         
[CLM_PARA]                   


[CLM_FILE]

#---OCEAN---#
###---LICOM /Buildconf/licom.buildnml.csh ---###

[LICOM_PARA]
NUMBER&namctl = 120
nx_proc&namctl = 10
ny_proc&namctl = 12
[LICOM_FILE]

###---POP2 /Buildconf/pop.buildnml.csh---###

[POP_PARA]

[POP_FILE]


#---SEAICE---#
###---CICE /Buildconf/cice.buildnml.csh---###

[CICE_PARA]                    #output frequency


[CICE_FILE]
#albicei                           = 0.45


##########################
#---xmlchange
##########################

#---env_run---#
[env_run]
STOP_OPTION                    = nday
STOP_N                         = 5

#---env_conf---#
[env_conf]
RUN_TYPE                     = startup
#Run start date (yyyy-mm-dd). Only used for startup or hybrid runs (char)
#RUN_STARTDATE                 = 2000-05-01
DEF_CHANGE           =     TRUE
#RUN_REFDATE                  = 0001-01-03
#ATM_NCPL                     = 12

#---env_mach_pes---#
[env_mach_pes]

######################################################
### for B compset;if compset =FAMIPC5 please unmark this section
######################################################
NTASKS_ATM = 128
NTASKS_LND = 128
NTASKS_WRF = 128
NTASKS_GEA = 128
NTASKS_SRD = 128
NTASKS_CPL = 128
NTASKS_GLC = 128
NTASKS_OCN = 120
NTASKS_ICE = 120
######################################################
###end###
######################################################


#---env_case---#
[env_case]

#---env_build---#
[env_build]

#########################
#---bgm restart
##########################
[bgm_restart]
#resart_files                       = /archive/iamrich/


##########################
#SPPT
##########################
[sppt_src]
#sppt_loc                        = /sppt_dir/









