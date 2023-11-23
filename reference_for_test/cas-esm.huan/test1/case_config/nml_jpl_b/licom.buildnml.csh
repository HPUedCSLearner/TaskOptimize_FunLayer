#! /bin/csh -f

#======================================================================
# Purpose:
#  1) define and prestage small ascii input files (input_template files)
#  2) define large initialization datasets (inputdata files)
#  3) create the licom namelist input file, licom_in
#======================================================================

#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
# NOTICE: 
#   This script was custom-generated on Fri Dec  4 21:45:13 CST 2020 for 
#   /public/home/thudess6/liuyao/pljiao/function_level/uq/casesm_cases/case_B1850_3
#   as a startup run using the licom ocean model at the gx1v6 resolution
#   DO NOT COPY this script to another case; use the create_clone script
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


setenv runtype   startup
if ($CONTINUE_RUN == 'TRUE') setenv runtype  continue

setenv OCN_PRESTAGE  FALSE 

set exedir   = $RUNDIR
set ocndir   = $EXEROOT/ocn
set rundir   = $RUNDIR
set objdir   = $OBJROOT/ocn/obj
set srcdir   = $CODEROOT/ocn/licom
set my_path  = $CASEROOT/SourceMods/src.licom
setenv MY_PATH $CASEROOT/SourceMods/src.licom    # used in ocn.*.setup.csh
                                                # must be unresolved env var

setenv INPUT            $EXEROOT/ocn/input
setenv INPUTDATA        $DIN_LOC_ROOT/ocn/pop
setenv INPUT_TEMPLATES  $srcdir/input_templates

setenv SRCDIR              /public/home/thudess6/uq/CAS-ESM/models/ocn/licom

setenv LICOM_DOCDIR         $CASEBUILD/licomdoc
setenv LICOM_BLDNML         $LICOM_DOCDIR/document_licom_buildnml
setenv LICOM_IN             $LICOM_DOCDIR/document_licom_in
setenv LICOM_INLIST         $LICOM_DOCDIR/document_licom_input_files
setenv LICOM_TAVG_NML_BASE  $LICOM_DOCDIR/licom_tavg_nml_base
setenv LICOM_TAVG_NML       $LICOM_DOCDIR/licom_tavg_nml

setenv OCN_GRID gx1v6 # used in ocn.*.setup.csh scripts

set ocn_tracers = (`echo $LICOM_TRACER_MODULES`)

if !( -d $ocndir/rest  )  mkdir -p $ocndir/rest   || exit 2
if !( -d $ocndir/hist  )  mkdir -p $ocndir/hist   || exit 2
if !( -d $ocndir/input )  mkdir -p $ocndir/input  || exit 2

date      > $LICOM_BLDNML
echo " " >> $LICOM_BLDNML
echo ------------------------------------------------------------------------ >> $LICOM_BLDNML
echo  Begin identifying and collecting all licom input datasets                >> $LICOM_BLDNML

  #------------------------------------------------------------------------
  #  1) define and prestage small ascii input files (input_template files)
  #     ==================================================================
  #
  #    The input_templates datasets are small ascii text files that by
  #    default are located in $srcdir/input_templates.  A user may
  #    choose to put a modified copy of the input_templates datasets in
  #    their $my_path directory. The input_templates datasets are always
  #    copied ("prestaged") to $ocndir/input prior to each run.
  #------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------
    # define all standard input_templates files; set unavailable filenames to 'unknown_$file
    #----------------------------------------------------------------------------------------------
     set input_templates_files = ( depth_accel history_contents movie_contents region_ids tavg_contents transport_contents vert_grid overflow )

     set input_templates_filenames = ( )
     foreach file ($input_templates_files)
       if (-f ${my_path}/gx1v6_$file) then
         set input_templates_filenames =  ($input_templates_filenames ${my_path}/gx1v6_$file)
       else if (-f $INPUT_TEMPLATES/gx1v6_$file) then
         set input_templates_filenames =  ($input_templates_filenames $INPUT_TEMPLATES/gx1v6_$file)
       else
         set input_templates_filenames =  ($input_templates_filenames unknown_$file)
       endif
     end

    #----------------------------------------------------------------------
    # copy all input_templates files into $ocndir prior to execution
    #----------------------------------------------------------------------
     foreach filename ($input_templates_filenames)
     if (-f $filename) cp -fp $filename $ocndir/input
     end

    #----------------------------------------------------------------------
    # tavg_contents OCN_TAVG_HIFREQ exception 
    #----------------------------------------------------------------------
     foreach filename ($input_templates_filenames)
      if ($filename:t == gx1v6_tavg_contents) then
       if ($OCN_TAVG_HIFREQ == TRUE) then
          if (-f ${my_path}/gx1v6_tavg_contents_high_freq) then
            cp -fp ${my_path}/gx1v6_tavg_contents_high_freq $ocndir/input/gx1v6_tavg_contents
          else if (-f $INPUT_TEMPLATES/gx1v6_tavg_contents_high_freq) then
            cp -fp $INPUT_TEMPLATES/gx1v6_tavg_contents_high_freq $ocndir/input/gx1v6_tavg_contents
          endif
       endif # OCN_TAVG_HIFREQ
      endif # tavg_contents
     end


    #----------------------------------------------------------------------
    # After copying input_templates files to $ocndir/input, point filenames
    # to the copies in the $ocndir/input directory.  These filenames will
    # be used to build the licom_in namelists
    #----------------------------------------------------------------------
    set input_filenames = ( )
    foreach file ($input_templates_files)
    if (-f $ocndir/input/gx1v6_$file) then
      setenv ${file}_filename  $ocndir/input/gx1v6_$file
    else
      setenv ${file}_filename  unknown_$file
    endif
    end

  #------------------------------------------------------------------------
  #  2) define large initialization datasets (inputdata files)
  #     ======================================================
  #
  #  These large datasets reside in $inputdata by default. They will be referenced
  #  directly in the licom_in file, without being copied to $ocndir/input first
  #------------------------------------------------------------------------

    #------------------------------------------------------
    #  initialize all inputdata filenames in this section 
    #  nonstandard files can be defined in the next section 
    #------------------------------------------------------
    set bottom_cell_filename  = 'unknown_bottom_cell'
    set bathymetry_filename   = 'unknown_bathymetry'
    set chl_filename          = 'unknown_chl'
    set horiz_grid_filename   = 'unknown_horiz_grid'
    set init_ts_filename      = 'unknown_init_ts'
    set regionmask_filename   = 'unknown_region_mask'
    set shf_filename          = 'unknown_shf'
    set sfwf_filename         = 'unknown_sfwf'
    set tidal_mixing_filename = 'unknown_tidal_mixing'
    set topography_filename   = 'unknown_topography'


    #-----------------------------------------------------------------------------
    #  identify all gx1v6 datasets residing in $DIN_LOC_ROOT
    #-----------------------------------------------------------------------------
    set init_ts_filename      = $DIN_LOC_ROOT/ocn/pop/gx1v6/ic/ts_PHC2_jan_ic_gx1v6_20090205.ieeer8
    set horiz_grid_filename   = $DIN_LOC_ROOT/ocn/pop/gx1v6/grid/horiz_grid_20010402.ieeer8
    set regionmask_filename   = $DIN_LOC_ROOT/ocn/pop/gx1v6/grid/region_mask_20090205.ieeei4
    set topography_filename   = $DIN_LOC_ROOT/ocn/pop/gx1v6/grid/topography_20090204.ieeei4
    set shf_filename          = $DIN_LOC_ROOT/ocn/pop/gx1v6/forcing/shf_mm_all_85-88_20010308.ieeer8
    set sfwf_filename         = $DIN_LOC_ROOT/ocn/pop/gx1v6/forcing/sfwf_mm_PHC2_salx_flxio_20090205.ieeer8
    set tidal_mixing_filename = $DIN_LOC_ROOT/ocn/pop/gx1v6/forcing/tidal_energy_gx1v6_20090205.ieeer8
    set chl_filename          = $DIN_LOC_ROOT/ocn/pop/gx1v6/forcing/chl_filled_20061230.ieeer8

#--------------------------------------------
#  set domain decomposition information
#--------------------------------------------
 setenv NPROCS_CLINIC  $NTASKS_OCN
 setenv NPROCS_TROPIC  $NTASKS_OCN

#----------------------------------------------------------------------
# Document the origins of licom input_templates files
#----------------------------------------------------------------------
 
 echo " " >&! $LICOM_INLIST
 echo "  ----------------------------------------------------------------------- " >> $LICOM_INLIST
 echo "   Origin of  $CASE licom input_template datasets used in this run       " >> $LICOM_INLIST
 echo "   `date`                                                               " >> $LICOM_INLIST
 echo "  ----------------------------------------------------------------------- " >> $LICOM_INLIST
 echo " " >> $LICOM_INLIST

 #-----  document input_template filenames
 foreach filename ($input_templates_filenames)
  if (-f $filename) ls -l $filename >> $LICOM_INLIST
 end

#----------------------------------------------------------------------
# optional prestaging inputdata files has been disabled
#----------------------------------------------------------------------
 if ($OCN_PRESTAGE == TRUE) then
   echo "OCN_PRESTAGE option is not supported" 
   exit -999
 endif # OCN_PRESTAGE


#-----------------------------------------
#  determine licom restart-file format
#-----------------------------------------
   if (-e $exedir/rpointer.ocn.restart && $CONTINUE_RUN == 'TRUE') then
    grep 'RESTART_FMT=' $exedir/rpointer.ocn.restart >&! /dev/null
    if ($status == 0) then
      setenv RESTART_INPUT_TS_FMT `grep RESTART_FMT\= $exedir/rpointer.ocn.restart | cut -c13-15`
    else
      setenv RESTART_INPUT_TS_FMT 'bin'
    endif
  else
    setenv RESTART_INPUT_TS_FMT 'bin'
  endif


echo " " >&! $LICOM_IN 
echo ------------------------------------------------------------------------ >> $LICOM_BLDNML
echo  Define the licom_in namelist file                                       >> $LICOM_BLDNML

#==========================================================================
#  3) create the licom namelist input file, licom_in
#     ============================================
#  
#     The following settings have been customized for this case  based upon
#     resolution, compset, and interactions among the default options.  A user
#     can change any of the following settings prior to run-time, but be aware of
#     option interdependencies when doing so. 
#==========================================================================


#--------------------------------------------------------------------------
# define variables needed by the pop2_in file
#--------------------------------------------------------------------------
set output_L = $rundir
set output_d = $rundir/$CASE.pop.d

set output_r     = ./$CASE.pop.r
set output_h     = ./$CASE.pop.h
set pop2_pointer = ./rpointer.ocn


if ( $LICOM_DECOMPTYPE == spacecurve) then
  set clinic_distribution_type = spacecurve
  set tropic_distribution_type = spacecurve
else
  set clinic_distribution_type = cartesian
  set tropic_distribution_type = cartesian
endif

if ($CALENDAR == GREGORIAN) then
 set allow_leapyear = .true.
else
 set allow_leapyear = .false.
endif

cat >> $LICOM_IN << EOF1

#==========================================================================
#  Begin pop2_in namelist build
#==========================================================================

&domain_nml
  nprocs_clinic            = $NPROCS_CLINIC
  nprocs_tropic            = $NPROCS_TROPIC
  clinic_distribution_type = '$clinic_distribution_type'
  tropic_distribution_type = '$tropic_distribution_type'
  ew_boundary_type         = 'cyclic'
  ns_boundary_type         = 'closed'
/

&io_nml
  num_iotasks          = 1 
  lredirect_stdout     = .true. 
  log_filename         = '$output_L/ocn.log.$LID'
  luse_pointer_files   = .true.
  pointer_filename     = './rpointer.ocn'
  luse_nf_64bit_offset = .true.
/


##########################################################
WARNING: DO NOT CHANGE iyear0, imonth0, iday0, ihour0 
##########################################################

&time_manager_nml
  runid             = '$CASE'
  time_mix_opt      = 'avgfit'
  time_mix_freq     = 17
  dt_option         = 'steps_per_day'
  dt_count          = 23
  impcor            = .true.
  laccel            = .false.
  accel_file        = '$depth_accel_filename'
  dtuxcel           = 1.0 
  allow_leapyear    = $allow_leapyear
  iyear0            = 1            
  imonth0           = 1      
  iday0             = 2       
  ihour0            = 0    
  iminute0          = 0         
  isecond0          = 0        
  date_separator    = '-'
  stop_option       = 'nyear'
  stop_count        =  1000
  fit_freq          = 1
/

&grid_nml
   horiz_grid_opt       = 'file'
   horiz_grid_file      = '$horiz_grid_filename'
   vert_grid_opt        = 'file'
   vert_grid_file       = '$vert_grid_filename'
   topography_opt       = 'file'
   kmt_kmin             = 3
   topography_file      = '$topography_filename'
   topography_outfile   = '${output_h}.topography_bathymetry.ieeer8'
   bathymetry_file      = '$bathymetry_filename'
   partial_bottom_cells =  .false.
   bottom_cell_file     = '$bottom_cell_filename'
   n_topo_smooth        = 0
   flat_bottom          = .false.
   lremove_points       =  .false.
   region_mask_file     = '$regionmask_filename'
   region_info_file     = '$region_ids_filename'
   sfc_layer_opt        = 'varthick'
/
&init_ts_nml
   init_ts_option      = 'ccsm_$runtype'
   init_ts_suboption   = 'null'
   init_ts_file        = '$init_ts_filename'
   init_ts_file_fmt    = '$RESTART_INPUT_TS_FMT'
   init_ts_outfile     = '${output_h}.ts_ic'
   init_ts_outfile_fmt = 'nc'
/

EOF1

if ( $INFO_DBUG == 2 || $INFO_DBUG == 3 ) then
  set diag_freq_opt = nstep
else
  set diag_freq_opt = nmonth
endif

cat >> $LICOM_IN << EOF1
&diagnostics_nml
   diag_global_freq_opt   = '$diag_freq_opt'
   diag_global_freq       = 1
   diag_cfl_freq_opt      = '$diag_freq_opt'
   diag_cfl_freq          = 1
   diag_transp_freq_opt   = '$diag_freq_opt'
   diag_transp_freq       = 1
   diag_transport_file    = '$transport_contents_filename'
   diag_outfile           = '${output_d}d'
   diag_transport_outfile = '${output_d}t'
   cfl_all_levels         = .false.
   diag_all_levels        = .false.
   diag_velocity_outfile  = '${output_d}v'
   ldiag_velocity         = .true.
/

EOF1

if ( $OCN_TAVG_HIFREQ == FALSE ) then
  set ldiag_global_tracer_budgets = .true.
else
  set ldiag_global_tracer_budgets = .false.
endif

cat >> $LICOM_IN << EOF1
&budget_diagnostics_nml
   ldiag_global_tracer_budgets = $ldiag_global_tracer_budgets
/

&bsf_diagnostic_nml
   ldiag_bsf = .true.
/

&restart_nml
   restart_freq_opt    = 'nyear' 
   restart_freq        = 100000
   restart_start_opt   = 'nstep'
   restart_start       =  0
   restart_outfile     = '$output_r'
   restart_fmt         = 'bin'
   leven_odd_on        = .false. 
   even_odd_freq       = 100000
   pressure_correction = .false.
/

EOF1

#############################################################################
# The following setting are for the base model only.
#   Change base-model   tavg_nml setting here.
#   Change tracer-model tavg_nml settings in the ocn.*.setup.csh scripts.
#   The final tavg_nml (base model + extra-tracer models) is constructed below.
#############################################################################

cat >&! $LICOM_TAVG_NML_BASE << EOF1
&tavg_nml
   n_tavg_streams              = 3
   ltavg_streams_index_present = .true.
   tavg_freq_opt               = 'nmonth' 'nday' 'once'
   tavg_freq                   = 1 1 1
   tavg_file_freq_opt          = 'nmonth' 'nmonth' 'once'
   tavg_file_freq              = 1 1 1
   tavg_stream_filestrings     = 'nmonth1' 'nday1' 'once'
   tavg_start_opt              = 'nstep' 'nstep' 'nstep'
   tavg_start                  = 0 0 0
   tavg_fmt_in                 = 'nc' 'nc' 'nc'
   tavg_fmt_out                = 'nc' 'nc' 'nc'
   tavg_contents               ='$tavg_contents_filename'
   ltavg_nino_diags_requested  = .true.
   tavg_infile                 ='${output_h}restart.end'
   tavg_outfile                ='$output_h'
   ltavg_has_offset_date       = .false. .false. .false.
   tavg_offset_years           = 1 1 1
   tavg_offset_months          = 1 1 1
   tavg_offset_days            = 2 2 2
   ltavg_one_time_header       = .false. .false. .false.
/

EOF1
cat >> $LICOM_IN << EOF1
&history_nml
   history_freq_opt  = 'never'
   history_freq      = 1
   history_outfile   = '${output_h}s'
   history_fmt       = 'nc'
   history_contents  = '$history_contents_filename'
/

&movie_nml
   movie_freq_opt = 'never'
   movie_freq     = 1
   movie_outfile  = '${output_h}m'
   movie_fmt      = 'nc'
   movie_contents = '$movie_contents_filename'
/

&solvers
   solverChoice         = 'ChronGear'
   convergenceCriterion = 1.0e-13 
   maxIterations        = 1000
   convergenceCheckFreq = 10
   preconditionerChoice = 'diagonal'
   preconditionerFile   = 'unknownPrecondFile'
/

&vertical_mix_nml
   vmix_choice           = 'kpp'
   aidif                 = 1.0
   implicit_vertical_mix = .true.
   convection_type       = 'diffusion'
   nconvad               = 2
   convect_diff          = 10000.0
   convect_visc          = 10000.0
   bottom_drag           = 1.0e-3
   bottom_heat_flx       = 0.0
   bottom_heat_flx_depth = 1000.0e2
/

&vmix_const_nml
   const_vvc = 0.25
   const_vdc = 0.25
/

&vmix_rich_nml
   bckgrnd_vvc = 1.0
   bckgrnd_vdc = 0.1
   rich_mix    = 50.0
/

&tidal_nml
  ltidal_mixing          = .true.
  local_mixing_fraction  = 0.33
  mixing_efficiency      = 0.2
  vertical_decay_scale   = 500.0e02
  tidal_mix_max          = 100.0
  tidal_energy_file      = '$tidal_mixing_filename'
  tidal_energy_file_fmt  = 'bin'
/

&vmix_kpp_nml
   bckgrnd_vdc1           = 0.16
   bckgrnd_vdc2           = 0.0
   bckgrnd_vdc_eq         = 0.01
   bckgrnd_vdc_psim       = 0.13
   bckgrnd_vdc_ban        = 1.0
   bckgrnd_vdc_dpth       = 1000.0e02
   bckgrnd_vdc_linv       = 4.5e-05
   Prandtl                = 10.0
   rich_mix               = 50.0
   lrich                  = .true.
   ldbl_diff              = .true.
   lshort_wave            = .true.
   lcheckekmo             = .false.
   num_v_smooth_Ri        = 1
   lhoriz_varying_bckgrnd = .true.
   llangmuir              = .false.
   linertial              = .false.
/

&advect_nml
   tadvect_ctype = 'upwind3'
/

&hmix_nml
   hmix_momentum_choice = 'anis'
   hmix_tracer_choice   = 'gent'
   lsubmesoscale_mixing = .true.
/

&hmix_del2u_nml
   lauto_hmix          = .false. 
   lvariable_hmix      = .false. 
   am                  = 0.5e8
/

&hmix_del2t_nml
   lauto_hmix          = .false.
   lvariable_hmix      = .false.
   ah                  = 0.6e7
/

&hmix_del4u_nml
   lauto_hmix          = .false. 
   lvariable_hmix      = .false.
   am                  = -0.6e20
/

&hmix_del4t_nml
   lauto_hmix          = .false.
   lvariable_hmix      = .false.
   ah                  = -0.2e20
/

&hmix_gm_nml
   kappa_isop_choice      = 'bfre'
   kappa_thic_choice      = 'bfre'
   kappa_freq_choice      = 'once_a_day'
   slope_control_choice   = 'notanh'
   kappa_depth_1          = 1.0
   kappa_depth_2          = 0.0
   kappa_depth_scale      = 150000.0
   ah                     = 3.0e7
   ah_bolus               = 3.0e7
   use_const_ah_bkg_srfbl = .true.
   ah_bkg_srfbl           = 3.0e7
   ah_bkg_bottom          = 0.0
   slm_r                  = 0.3
   slm_b                  = 0.3
   diag_gm_bolus          = .true.
   transition_layer_on    = .true.
   read_n2_data           = .false.
   buoyancy_freq_filename = '$EXEROOT/ocn/input/buoyancy_freq'
   buoyancy_freq_fmt      = 'nc'
   const_eg               = 1.2
   gamma_eg               = 500.0
   kappa_min_eg           = 0.35e7
   kappa_max_eg           = 2.0e7
/

&mix_submeso_nml
   efficiency_factor          = 0.07
   time_scale_constant        = 8.64e4
   luse_const_horiz_len_scale = .false.
   hor_length_scale           = 5.0e5
/

&hmix_aniso_nml
   hmix_alignment_choice     = 'east'
   lvariable_hmix_aniso      = .true.
   lsmag_aniso               = .false.
   visc_para                 = 50.0e7
   visc_perp                 = 50.0e7
   c_para                    = 8.0
   c_perp                    = 8.0
   u_para                    = 5.0
   u_perp                    = 5.0
   vconst_1                  = 0.6e7
   vconst_2                  = 0.5
   vconst_3                  = 0.16
   vconst_4                  = 2.e-8
   vconst_5                  = 3
   vconst_6                  = 0.6e7
   vconst_7                  = 45.0
   smag_lat                  = 20.0
   smag_lat_fact             = 0.98
   smag_lat_gauss            = 98.0
   var_viscosity_infile      = 'ccsm-internal'
   var_viscosity_infile_fmt  = 'bin'
   var_viscosity_outfile     = '${output_h}v'
   var_viscosity_outfile_fmt = 'nc'
/

&state_nml
   state_choice     = 'mwjf'
   state_file       = 'internal'
   state_range_opt  = 'enforce'
   state_range_freq = 100000
/

&baroclinic_nml
   reset_to_freezing = .false.
/

&ice_nml
   ice_freq_opt     = 'coupled'
   ice_freq         =  100000
   kmxice           = 1
   lactive_ice      = .true.
/

&pressure_grad_nml
   lpressure_avg  = .true.
   lbouss_correct = .false.
/

&topostress_nml
   ltopostress  = .false.
   nsmooth_topo = 0
/

&forcing_ws_nml
   ws_data_type      = 'none'
   ws_data_inc       = 24.
   ws_interp_freq    = 'every-timestep'
   ws_interp_type    = 'linear'
   ws_interp_inc     = 72.
   ws_filename       = 'unknown-ws'
   ws_file_fmt       = 'bin'
   ws_data_renorm(1) = 10.
/

&forcing_shf_nml
   shf_formulation      = 'restoring'
   shf_data_type        = 'none'
   shf_data_inc         = 24.
   shf_interp_freq      = 'every-timestep'
   shf_interp_type      = 'linear'
   shf_interp_inc       = 72.
   shf_restore_tau      = 30.
   shf_filename         = '$shf_filename'
   shf_file_fmt         = 'bin'
   shf_data_renorm(3)   = 0.94
   shf_weak_restore     = 0.
   shf_strong_restore   = 0.0
   luse_cpl_ifrac       = .false.
   shf_strong_restore_ms= 92.64
/

&forcing_sfwf_nml
   sfwf_formulation       = 'restoring'
   sfwf_data_type         = 'none'
   sfwf_data_inc          = 24.
   sfwf_interp_freq       = 'every-timestep'
   sfwf_interp_type       = 'linear'
   sfwf_interp_inc        = 72.
   sfwf_restore_tau       = 30.
   sfwf_filename          = '$sfwf_filename'
   sfwf_file_fmt          = 'bin'
   sfwf_data_renorm(1)    = 0.001
   sfwf_weak_restore      = 0.0115
   sfwf_strong_restore    = 0.0
   sfwf_strong_restore_ms = 0.6648
   ladjust_precip         = .false.
   lms_balance            = .true.
   lfw_as_salt_flx        = .true.
   lsend_precip_fact      = .false.
/

&forcing_pt_interior_nml
   pt_interior_data_type         = 'none'
   pt_interior_data_inc          = 24.
   pt_interior_interp_freq       = 'every-timestep'
   pt_interior_interp_type       = 'linear'
   pt_interior_interp_inc        = 72.
   pt_interior_restore_tau       = 365.
   pt_interior_filename          = 'unknown-pt_interior'
   pt_interior_file_fmt          = 'bin'
   pt_interior_restore_max_level = 0 
   pt_interior_formulation       = 'restoring'
   pt_interior_data_renorm(1)    = 1.
   pt_interior_variable_restore  = .false.
   pt_interior_restore_filename  = 'unknown-pt_interior_restore'
   pt_interior_restore_file_fmt  = 'bin'
/

&forcing_s_interior_nml
   s_interior_data_type         = 'none'
   s_interior_data_inc          = 24.
   s_interior_interp_freq       = 'every-timestep'
   s_interior_interp_type       = 'linear'
   s_interior_interp_inc        = 72.
   s_interior_restore_tau       = 365.
   s_interior_filename          = 'unknown-s_interior'
   s_interior_file_fmt          = 'bin'
   s_interior_restore_max_level = 0 
   s_interior_formulation       = 'restoring'
   s_interior_data_renorm(1)    = 1.
   s_interior_variable_restore  = .false.
   s_interior_restore_filename  = 'unknown-s_interior_restore'
   s_interior_restore_file_fmt  = 'bin'
/

&forcing_ap_nml
   ap_data_type      = 'none'
   ap_data_inc       = 1.e20
   ap_interp_freq    = 'never'
   ap_interp_type    = 'nearest'
   ap_interp_inc     = 1.e20
   ap_filename       = 'unknown-ap'
   ap_file_fmt       = 'bin'
   ap_data_renorm    = 1.
/

&coupled_nml
   coupled_freq_opt  = 'nhour'
   coupled_freq      =  24
   qsw_distrb_opt    = 'cosz'
/

&sw_absorption_nml
   sw_absorption_type = 'chlorophyll'
   chl_option         = 'file'
   chl_filename       = '$chl_filename'
   chl_file_fmt       = 'bin'
   jerlov_water_type  = 3
/

The present code makes assumptions about the region boundaries, so
DO NOT change transport_reg2_names unless you know exactly what you are doing.
&transports_nml
  lat_aux_grid_type      = 'southern'
  lat_aux_begin          = -90.0
  lat_aux_end            =  90.0
  n_lat_aux_grid         = 180 
  moc_requested          = .true.
  n_heat_trans_requested = .true.
  n_salt_trans_requested = .true.
  transport_reg2_names   = 'Atlantic Ocean','Mediterranean Sea','Labrador Sea','GIN Sea','Arctic Ocean','Hudson Bay'
  n_transport_reg        = 2
/

&context_nml
   lcoupled                 = .true.
   lccsm                    = .true.
   b4b_flag                 = .false.
   lccsm_control_compatible = .false.
/

&overflows_nml
   overflows_on           = .true.
   overflows_interactive  = .true.
   overflows_infile       = '$overflow_filename'
   overflows_diag_outfile = '${output_d}o'
   overflows_restart_type = 'ccsm_$runtype'
   overflows_restfile     = '${output_r}o'
/

EOF1




echo   Copy $LICOM_IN to $exedir/licom_in                                   >> $LICOM_BLDNML
echo ------------------------------------------------------------------------ >> $LICOM_BLDNML

if (-f $exedir/licom_in) rm $exedir/licom_in

cd $exedir

setenv data_licom $DIN_LOC_ROOT_CSMDATA/data_licom
#setenv DATA_CoLM $DIN_LOC_ROOT_CSMDATA/lnd/colm
cd $rundir
ln -s $data_licom/ahv_back.txt .
ln -s $data_licom/BASIN_eq1x1_362X196.nc BASIN.nc
ln -s $data_licom/dncoef_eq1x1.h dncoef.h1
ln -s $data_licom/Eq1x1_130824pm2.* .
ln -s $data_licom/domain_licom_eq1x1_cpl7_20120819.nc domain_licom.nc
ln -s $data_licom/INDEX.DATA .
ln -s $data_licom/MODEL.FRC .
ln -s $data_licom/TSinitial .
#ln -s $DATA_CoLM/CoLM-128x256-const-c-soic20-licom .
#ln -s $DATA_CoLM/CoLM-128x256-gridata-c-soic20-licom .
#ln -s $DATA_CoLM/CoLM-128x256-restart-c-soic20-licom .
#ln -s $DATA_CoLM/CoLM-128x256-sbcini-c-soic20-licom .
#ln -s $DATA_CoLM/MONTHLY_LAI_IAP.dat .
#ln -s $DATA_CoLM/rdirc.05 .
cp $data_licom/licom_change/* .
#cp -f atm_in.change atm_in
#cp -f drv_in.change drv_in
#cp -f seq_maps.rc.change seq_maps.rc
#cp -f dice_ice_in.change dice_ice_in
#cp -f ice_in.change ice_in
#cp -f lnd_in.change lnd_in
#cp -f ssmi_ifrac.clim.x0.5.txt.change ssmi_ifrac.clim.x0.5.txt
#cp -f nyf.giss.T62.stream.txt.change nyf.giss.T62.stream.txt
#cp -f nyf.gxgxs.T62.stream.txt.change nyf.gxgxs.T62.stream.txt
#cp -f nyf.ncep.T62.stream.txt.change nyf.ncep.T62.stream.txt
#cp -r runoff.1x1.stream.txt.change runoff.1x1.stream.txt

set lname=$CCSM_LCOMPSET
set sname=$CCSM_SCOMPSET
if ($lname == 'B_1850_CAM5X_CM' | $sname == 'B1850C5XCM') then
  cp $data_licom/OBM/* .
endif

set nx=$NX_PROC
set ny=$NY_PROC

cat >! licom_in <<EOF3
 &namctl
  DLAM       =1.0            !grid distance
  AM_TRO     = 6000
  AM_EXT     = 6000
  IDTB       =60
  IDTC       =720
  IDTS       =3600
  AFB1       =0.43
  AFC1       =0.43
  AFT1       =0.43
  AMV        = 1.0E-3
  AHV        = 0.3E-4
  NUMBER     = 60
  diag_msf   =.true.
  diag_mth   =.true.
  diag_bsf   =.true.
  IO_HIST    = 1
  IO_REST    = 1
  klv        = 30
  out_dir    = "./"
  nx_proc=6
  ny_proc=10
  imt_global=362
  jmt_global=196
  km=30
 &end
EOF3
#==========================================================================
#  End licom_in namelist build
#==========================================================================
echo  Successful completion                                                   >> $LICOM_BLDNML
echo ------------------------------------------------------------------------ >> $LICOM_BLDNML
echo " " >> $LICOM_BLDNML
date >> $LICOM_BLDNML
exit 0

