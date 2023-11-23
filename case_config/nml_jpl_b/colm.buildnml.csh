#! /bin/csh -f 

#******************************************************************#
#                  WARNING:                                        #
# - If the user changes any input datasets - be sure to give it a  #
#   unique filename. Do not duplicate any existing input files     #
#******************************************************************#

set exedir = $RUNDIR; cd $exedir

set lnd_yy   = 0001
set lnd_dd   = 1
set lnd_ss   = 0

setenv DATA_CoLM $DIN_LOC_ROOT_CSMDATA/lnd/colm/
ln -s $DATA_CoLM/rdirc.05 .

setenv DATA_CoLM $CCSMROOT/newdata/jiduoying
gzip -dc ${DATA_CoLM}/CoLM-srf-IAP-CMIP-${ATM_GRID}.gz > CoLM-srf-IAP-CMIP-${ATM_GRID}
gzip -dc ${DATA_CoLM}/CoLM-srf-IAP-AMIP-${ATM_GRID}.gz > CoLM-srf-IAP-AMIP-${ATM_GRID}
gzip -dc ${DATA_CoLM}/CoLM-lai-IAP-CMIP-${ATM_GRID}.gz > CoLM-lai-IAP-CMIP-${ATM_GRID}
gzip -dc ${DATA_CoLM}/CoLM-lai-IAP-AMIP-${ATM_GRID}.gz > CoLM-lai-IAP-AMIP-${ATM_GRID}
gzip -dc ${DATA_CoLM}/CoLM-ini-IAP-CMIP-${ATM_GRID}.gz > CoLM-ini-IAP-CMIP-${ATM_GRID}
gzip -dc ${DATA_CoLM}/CoLM-ini-IAP-AMIP-${ATM_GRID}.gz > CoLM-ini-IAP-AMIP-${ATM_GRID}
gzip -dc ${DATA_CoLM}/CoLM-sbc-IAP-CMIP-${ATM_GRID}.gz > CoLM-sbc-IAP-CMIP-${ATM_GRID}
gzip -dc ${DATA_CoLM}/CoLM-sbc-IAP-AMIP-${ATM_GRID}.gz > CoLM-sbc-IAP-AMIP-${ATM_GRID}

cat >! lnd_in << EOF
 &clmexp
  fsrf = 'CoLM-srf-IAP-CMIP-128x256'
  flai = 'CoLM-lai-IAP-CMIP-128x256'
  fini = 'CoLM-ini-IAP-CMIP-128x256'
  fsbc = 'CoLM-sbc-IAP-CMIP-128x256'
 frivinp_rtm    = 'rdirc.05'
 lnd_cflux_year = 9999
 co2_type       = 'constant'
 co2_ppmv       = 284.7
 lhist_yearly   = .true.
 lhist_monthly  = .true.
 lhist_daily    = .false.
 lhist_3hourly  = .false.
 lon_points     = 256 
 lat_points     = 128
 dtime          = 1800
 /

EOF
