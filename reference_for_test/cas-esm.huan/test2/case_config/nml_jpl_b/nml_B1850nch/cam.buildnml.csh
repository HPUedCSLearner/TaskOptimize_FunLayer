#! /bin/csh -f 

#******************************************************************#
#                  WARNING:                                        #
# - CAM and CLM namelist variable dtime must have same values      #
# - If the user changes any input datasets - be sure to give it a  #
#   unique filename. Do not duplicate any existing input files     #
#******************************************************************#

#&cam_inparm
# fincl2 = 'U:A','PS:A','TS:A','PRECT:A','FLUT:A'
 # fexcl1 = 'DTH','DTV','UU','VV'
 # nhtfrq = -24,-24,-24,-24,-24
 # mfilt = 1,1,1,1,1,1
 
 # ncdata		= '$DIN_LOC_ROOT/atm/cam/inic/IAP/IAPi_0000-01-01_128x256_L35_c180626.nc'
set exedir = $RUNDIR; cd $exedir

@ zz=128
@ zz/=32
cat >! atm_in << EOF
&zyxconv_nl
 zmh_tau = 3000
/
&aerodep_flx_nl
 aerodep_flx_cycle_yr		= 2000
 aerodep_flx_datapath		= '$DIN_LOC_ROOT/atm/cam/chem/trop_mozart_aero/aero'
 aerodep_flx_file		= 'aerosoldep_monthly_1849-2006_1.9x2.5_c090803.nc'
 aerodep_flx_type		= 'CYCLICAL'
/
&cam_inparm
 bnd_topo		= '$DIN_LOC_ROOT/atm/cam/topo/USGS-gtopo30_128x256_c130401_IAP.nc'
 bnd_topo2		= '$DIN_LOC_ROOT/atm/cam/topo/USGS_gtopo30_cube1.5min_to_128x256_c190611_IAP-720dir.nc'
 cam_branch_file		= ' '
 dtime		= 1800
 ncdata		= '$DIN_LOC_ROOT/atm/cam/inic/IAP/IAPi_0000-01-01_128x256_L35_c180626.nc'
/
&chem_inparm
 ext_frc_type		= 'CYCLICAL'
 srf_emis_type		= 'CYCLICAL'
 tracer_cnst_cycle_yr		= 1850
 tracer_cnst_file		= 'oxid_1.9x2.5_L26_1850clim_c091123.nc'
 tracer_cnst_type		= 'CYCLICAL'
/
&chem_surfvals_nl
 ch4vmr		= 791.6e-9
 co2vmr		= 284.7e-6
 f11vmr		= 12.48e-12
 f12vmr		= 0.0
 n2ovmr		= 275.68e-9
/
&cldfrc_nl
 cldfrc_dp1		=  0.10D0 
 cldfrc_dp2		=  500.0D0 
 cldfrc_freeze_dry		= .true.
 cldfrc_ice		= .true.
 cldfrc_premit		=  40000.0D0 
 cldfrc_rhminh		=  0.800D0 
 cldfrc_rhminl		=  0.89D0 
 cldfrc_sh1		=  0.07D0 
 cldfrc_sh2		=  500.0D0 
/
&cldsed_nl
 cldsed_ice_stokes_fac		=  1.0D0 
/
&cldwat_nl
 cldwat_conke		=   5.0e-6  
 cldwat_icritc		=  16.0e-6  
 cldwat_icritw		=   4.0e-4  
 cldwat_r3lcrit		=   10.0e-6  
/
&gw_drag_nl
 effgw_beres		= 	0.1	
 fcrit2		= 1.0
 gw_drag_file		= '$DIN_LOC_ROOT/atm/waccm/gw/newmfspectra40_dc25.nc'
 gw_drag_scheme		= 	1	
/
&hkconv_nl
 hkconv_c0		=   1.0e-4 
 hkconv_cmftau		=  1800.0D0 
/
&phys_ctl_nl
 cam_chempkg		= 'none'
 cam_physpkg		= 'cam5'
 conv_water_in_rad		=  1 
 deep_scheme		= 'ZM'
 do_iss		=  .true.  
 do_tms		=  .true.  
 eddy_scheme		= 'diag_TKE'
 history_microphysics		=   .true.  
 microp_scheme		= 'MG'
 shallow_scheme		= 'UW'
 srf_flux_avg		= 0
 tms_orocnst		=  1.0D0   
 tms_z0fac		=  0.075D0 
/
&prescribed_aero_nl
 prescribed_aero_cycle_yr		= 2000
 prescribed_aero_datapath		= '$DIN_LOC_ROOT/atm/cam/chem/trop_mozart_aero/aero'
 prescribed_aero_file		= 'aero_1.9x2.5_L26_2000clim_c091112.nc'
 prescribed_aero_specifier		= 'sulf:SO4', 'bcar1:CB1', 'bcar2:CB2', 'ocar1:OC1', 'ocar2:OC2', 'sslt1:SSLT01', 'sslt2:SSLT02',
  'sslt3:SSLT03', 'sslt4:SSLT04', 'dust1:DST01', 'dust2:DST02', 'dust3:DST03', 'dust4:DST04'
 prescribed_aero_type		= 'CYCLICAL'
/
&prescribed_ozone_nl
 prescribed_ozone_cycle_yr		= 1850
 prescribed_ozone_datapath		= '$DIN_LOC_ROOT/atm/cam/ozone'
 prescribed_ozone_file		= 'ozone_1.9x2.5_L26_1850clim_c090420.nc'
 prescribed_ozone_name		= 'O3'
 prescribed_ozone_type		= 'CYCLICAL'
/
&rad_cnst_nl
 icecldoptics		= 'mitchell'
 iceopticsfile		= '$DIN_LOC_ROOT/atm/cam/physprops/iceoptics_c080917.nc'
 liqcldoptics		= 'gammadist'
 liqopticsfile		= '$DIN_LOC_ROOT/atm/cam/physprops/F_nwvl200_mu20_lam50_res64_t298_c080428.nc'
 rad_climate		= 'P_Q:H2O', 'D_O2:O2', 'D_CO2:CO2', 'D_ozone:O3', 'D_N2O:N2O', 'D_CH4:CH4', 'D_CFC11:CFC11',
  'D_CFC12:CFC12', 'D_sulf:$DIN_LOC_ROOT/atm/cam/physprops/sulfate_rrtmg_c080918.nc',
  'D_dust1:$DIN_LOC_ROOT/atm/cam/physprops/dust1_rrtmg_c080918.nc',
  'D_dust2:$DIN_LOC_ROOT/atm/cam/physprops/dust2_rrtmg_c080918.nc',
  'D_dust3:$DIN_LOC_ROOT/atm/cam/physprops/dust3_rrtmg_c080918.nc',
  'D_dust4:$DIN_LOC_ROOT/atm/cam/physprops/dust4_rrtmg_c080918.nc',
  'D_bcar1:$DIN_LOC_ROOT/atm/cam/physprops/bcpho_rrtmg_c080918.nc',
  'D_bcar2:$DIN_LOC_ROOT/atm/cam/physprops/bcphi_rrtmg_c080918.nc',
  'D_ocar1:$DIN_LOC_ROOT/atm/cam/physprops/ocpho_rrtmg_c080918.nc',
  'D_ocar2:$DIN_LOC_ROOT/atm/cam/physprops/ocphi_rrtmg_c080918.nc',
  'D_sslt1:$DIN_LOC_ROOT/atm/cam/physprops/seasalt1_rrtmg_c080918.nc',
  'D_sslt2:$DIN_LOC_ROOT/atm/cam/physprops/seasalt2_rrtmg_c080918.nc',
  'D_sslt3:$DIN_LOC_ROOT/atm/cam/physprops/seasalt3_rrtmg_c080918.nc',
  'D_sslt4:$DIN_LOC_ROOT/atm/cam/physprops/seasalt4_rrtmg_c080918.nc'
/
&solar_inparm
 solar_data_file		= '$DIN_LOC_ROOT/atm/cam/solar/SOLAR_SPECTRAL_Lean_1610-2008_annual_c090324.nc'
 solar_data_type		= 'FIXED'
 solar_data_ymd		= 18500101
 solar_htng_spctrl_scl		= .true.
/
&tropopause_nl
 tropopause_climo_file		= '$DIN_LOC_ROOT/atm/cam/chem/trop_mozart/ub/clim_p_trop.nc'
/
&uwshcu_nl
 uwshcu_rpen		=   10.0 
/
&zmconv_nl
 zmconv_c0_lnd		=  0.0059D0 
 zmconv_c0_ocn		=  0.0450D0 
 zmconv_dmpdz		=  -1.0E-3 
 zmconv_ke		=  1.0E-6 
/
&spmd_iap_inparm
 npr_yz         = 32,$zz,$zz,32
 Ndt            = 2
 Ndq            = 2
 DTDY           = 180.0D0
/
EOF
