#! /bin/csh -f 

set exedir = $RUNDIR; cd $exedir

cat >! ice_in << EOF
&setup_nml
 diagfreq		=  24   
 hist_avg		= .true.  
 histfreq		= 'm','x','x','x','x'
 histfreq_n		= 1,1,1,1,1           
 ice_ic		= 'default'
 lcdf64		= .true. 
 pointer_file		= 'rpointer.ice'
 xndt_dyn		=  3.0 
/
&grid_nml
 grid_file		= '$DIN_LOC_ROOT/data_licom/Eq1x1_130824pm2.grid'
 grid_format		= 'bin'
 grid_type		= 'displaced_pole'
 kcatbound		=  0 
 kmt_file		= '$DIN_LOC_ROOT/data_licom/Eq1x1_130824pm2.kmt'
/
&ice_nml
 advection		= 'remap'
 albedo_type		= 'default'
 albicei		= 0.45
 albicev		= 0.75
 albsnowi		= 0.73
 albsnowv		= 0.98
 dt_mlt_in		=  1.50 
 evp_damping		= .false.
 kdyn		=  1 
 kitd		=  1 
 krdg_partic		= 1
 krdg_redist		= 1
 kstrength		=  1 
 ndte		=  120 
 r_snw		=   1.50 
 rsnw_melt_in		=  1500. 
 shortwave		= 'dEdd'
/
&tracer_nml
 tr_aero		=  .true. 
 tr_fy		=  .true. 
 tr_iage		=  .true. 
 tr_pond		=  .true. 
/
&domain_nml
 distribution_type		= '$CICE_DECOMPTYPE'
 ew_boundary_type		= 'cyclic'
 ns_boundary_type		= 'open'
 processor_shape		= 'square-pop'
/
&ice_prescribed_nml
 prescribed_ice		= .false.
/
&icefields_nml
 f_aero		= 'mxxxx'
 f_aicen		= 'mxxxx'
 f_aisnap		= 'mdxxx'
 f_apondn		= 'mxxxx'
 f_congel		= 'mxxxx'
 f_daidtd		= 'mxxxx'
 f_daidtt		= 'mxxxx'
 f_divu		= 'mxxxx'
 f_dvidtd		= 'mxxxx'
 f_dvidtt		= 'mxxxx'
 f_faero_atm		= 'mxxxx'
 f_faero_ocn		= 'mxxxx'
 f_fhocn		= 'mxxxx'
 f_fhocn_ai		= 'mxxxx'
 f_frazil		= 'mxxxx'
 f_fresh		= 'mxxxx'
 f_fresh_ai		= 'mxxxx'
 f_frz_onset		= 'xxxxx'
 f_frzmlt		= 'xxxxx'
 f_fsalt		= 'mxxxx'
 f_fsalt_ai		= 'mxxxx'
 f_fy		= 'mdxxx'
 f_hisnap		= 'mdxxx'
 f_icepresent		= 'mxxxx'
 f_meltb		= 'mxxxx'
 f_meltl		= 'mxxxx'
 f_meltt		= 'mxxxx'
 f_mlt_onset		= 'xxxxx'
 f_opening		= 'mxxxx'
 f_shear		= 'mxxxx'
 f_sig1		= 'mxxxx'
 f_sig2		= 'mxxxx'
 f_snoice		= 'mxxxx'
 f_sss		= 'xxxxx'
 f_sst		= 'xxxxx'
 f_strairx		= 'mxxxx'
 f_strairy		= 'mxxxx'
 f_strcorx		= 'mxxxx'
 f_strcory		= 'mxxxx'
 f_strength		= 'mxxxx'
 f_strintx		= 'mxxxx'
 f_strinty		= 'mxxxx'
 f_strocnx		= 'mxxxx'
 f_strocny		= 'mxxxx'
 f_strtltx		= 'xxxxx'
 f_strtlty		= 'xxxxx'
 f_uocn		= 'xxxxx'
 f_uvel		= 'mxxxx'
 f_vicen		= 'mxxxx'
 f_vocn		= 'xxxxx'
 f_vvel		= 'mxxxx'
/
EOF
