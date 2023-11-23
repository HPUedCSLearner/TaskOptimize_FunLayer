#! /bin/csh -f

#--------------------------------------------------------------------
# check basic task and thread settings
#--------------------------------------------------------------------

set exedir  = $RUNDIR
set rundir  = $RUNDIR
set objdir  = $OBJROOT/ocn/obj
set ocndir  = $RUNDIR
set srcdir  = $CODEROOT/ocn/licom
set my_path = $CASEROOT/SourceMods/src.licom

set ntask   = $NTASKS_OCN
set ocn_tracers = (`echo $LICOM_TRACER_MODULES`)

setenv OCN_PRESTAGE FALSE
setenv INPUT        $EXEROOT/ocn/input
setenv LICOM_DOCDIR  $CASEBUILD/licomdoc
setenv LICOM_BLDNML  $LICOM_DOCDIR/document_licom_buildnml
setenv runtype      $RUN_TYPE

setenv OCN_GRID gx1v6 # used in ocn.*.setup.csh scripts

cd $objdir

echo -------------------------------------------------------------------------
echo Begin the process of building the licom executable
echo -------------------------------------------------------------------------
echo " "

setenv BLCKX $LICOM_BLCKX
setenv BLCKY $LICOM_BLCKY
setenv MXBLCKS $LICOM_MXBLCKS
setenv DECOMPTYPE $LICOM_DECOMPTYPE

echo -----------------------------------------------------------------
echo Create the internal directory structure
echo -----------------------------------------------------------------

set compile_dir = $objdir
set source_dir  = $OBJROOT/ocn/source

if !(-d $source_dir  ) mkdir -p $source_dir
if !(-d $compile_dir ) mkdir -p $compile_dir

#echo -----------------------------------------------------------------
#echo Create domain_size.F90 in $source_dir, first computing NT
#echo -----------------------------------------------------------------
#
#echo 2 > $source_dir/NT
#foreach module ( $ocn_tracers )
#  if (-f ${my_path}/ocn.${module}.setup.csh) then
#     ${my_path}/ocn.${module}.setup.csh set_nt $source_dir/NT || exit $status
#  else if (-f $srcdir/input_templates/ocn.${module}.setup.csh ) then
#     $srcdir/input_templates/ocn.${module}.setup.csh set_nt $source_dir/NT || exit $status
#  else
#     echo error in licom.buildexe.csh unknown tracer: $module
#     exit -3
#  endif
#end
#set NT = `cat $source_dir/NT`
#
#if (-f ${my_path}/gx1v6_domain_size.F90) then
#   set domain_size_infile = ${my_path}/gx1v6_domain_size.F90
#else
#   set domain_size_infile = $srcdir/input_templates/gx1v6_domain_size.F90
#endif
#
##
##  If new domain_size.F90 is identical to existing one, do nothing.
##  This is in order to preserve file timestamps and avoid unnecessary
##  compilation cascade.
##
#
#sed -e "s#nt *= *2#nt = $NT#" < $domain_size_infile > $source_dir/domain_size.F90.new
#if (-f $source_dir/domain_size.F90) then
#  diff $source_dir/domain_size.F90.new $source_dir/domain_size.F90
#  if ($status) then
#    mv $source_dir/domain_size.F90.new $source_dir/domain_size.F90
#    cp ${my_path}/gx1v6_domain_size.F90 domain_size.F90
#  else
#    rm -f $source_dir/domain_size.F90.new
#  endif
#else
#  mv $source_dir/domain_size.F90.new $source_dir/domain_size.F90
#  cp ${my_path}/gx1v6_domain_size.F90 domain_size.F90
#endif
#
################ needed during LANL merge transition #####################
#if (-f ${my_path}/gx1v6_LICOM_DomainSizeMod.F90) then
#   cp -fp  ${my_path}/gx1v6_LICOM_DomainSizeMod.F90 $source_dir/LICOM_DomainSizeMod.F90
#else
#   cp -fp $srcdir/input_templates/gx1v6_LICOM_DomainSizeMod.F90 $source_dir/LICOM_DomainSizeMod.F90
#endif
########################## end LANL merge transition #####################

echo -----------------------------------------------------------------
echo  Copy the necessary files into $source_dir                     
echo -----------------------------------------------------------------
cd $source_dir
cp -fp $srcdir/source/*               .
#cp -fp $srcdir/mpi/*.F90                   .
#cp -fp $srcdir/drivers/cpl_share/*.F90     .
if ($COMP_INTERFACE == 'MCT') then
#  cp -fp $srcdir/drivers/cpl_mct/*.F90     .
else if ($COMP_INTERFACE == 'ESMF') then
#  cp -fp $srcdir/drivers/cpl_esmf/*.F90    .
else
  echo "ERROR: must specifiy valid $COMP_INTERFACE value"
  exit -1
endif

#
#  copy src.licom files
#

if (-d $my_path ) cp -fp $my_path/*   .
rm -f gx1v6_domain_size.F90
#
#  recompile if 2d decomp is changed
#
#set nx=20
#set ny=6
set lname=$CCSM_LCOMPSET
set sname=$CCSM_SCOMPSET
if ($lname == 'B_1850_CAM5X_CM' | $sname == 'B1850C5XCM') then
set biochemistry=define
else
set biochemistry=undef
endif
if ($DEF_CHANGE == "TRUE") then
set co2switch = undef
cat >! def-undef.h <<EOF3
#define SPMD
#define  SYNCH
#undef  FRC_ANN
#define CDFIN
#undef  FRC_DAILY
#undef  FRC_CORE
#define SOLAR
#define  ACOS
#undef  BIHAR
#undef  SMAG_FZ
#undef  SMAG_OUT
#define NETCDF
#undef BOUNDARY
#define NODIAG
#undef  ICE
#undef SHOW_TIME
#define DEBUG
#define COUP
#define  ISO
#define D_PRECISION
#define  CANUTO
#undef SOLARCHLORO
#undef LDD97
#undef TSPAS
#undef  SMAG
#define BACKMX
#define NEWSSBC
#$biochemistry biochem
#define  USE_OCN_CARBON
#undef   carbonC14
#undef   carbonC
#define  carbonBio
#undef  Felimit
#define mom_xu_pt
#undef   scav_moore08
#undef   carbonAbio
#define  preindustrial
#undef  murnane1999
#define  anderson1995
#undef   progca
#undef   buchang
#undef   carbonDebug
#undef   printcall
#undef   nc14wind
#define  o2limit
#$co2switch CO2
EOF3
endif
set recompile = FALSE
echo gx1v6 $ntask ${BLCKX} ${BLCKY} ${MXBLCKS} >! $objdir/ocnres.new
diff $objdir/ocnres.new $objdir/ocnres.old || set recompile = TRUE
if ($recompile == 'TRUE') then
    touch `grep -l BLCKX $source_dir/*`  # force recompile
    touch `grep -l BLCKY $source_dir/*`  # force recompile
    touch `grep -l MXBLCKS $source_dir/*`  # force recompile
endif  
echo gx1v6 $ntask ${BLCKX} ${BLCKY} ${MXBLCKS} >! $objdir/ocnres.old

echo -----------------------------------------------------------------
echo  Compile licom library
echo -----------------------------------------------------------------
cd $compile_dir
\cat >! Filepath <<EOF
 $source_dir
EOF

cd $compile_dir

set licomdefs = "-DCCSMCOUPLED -DBLCKX=$BLCKX -DBLCKY=$BLCKY -DMXBLCKS=$MXBLCKS"
if ($LICOM_ICE_FORCING == 'inactive' ) then
set licomdefs = "$licomdefs -DZERO_SEA_ICE_REF_SAL"
endif

if ($OCN_GRID =~ tx0.1* ) then
set licomdefs = "$licomdefs -D_HIRES"
endif

gmake complib -j $GMAKE_J MODEL=pop2 COMPLIB=$LIBROOT/libocn.a MACFILE=$CASEROOT/Macros.$MACH USER_CPPDEFS="$licomdefs" -f $CASETOOLS/Makefile || exit 2

set f90_dir = $source_dir/f90
if !(-d  $f90_dir ) mkdir -p $f90_dir

echo " "
echo ----------------------------------------------------------------------------
echo  Note that f90 files may not exist on all machines
echo ----------------------------------------------------------------------------
mv -f *.f90 $f90_dir

if !(-f $LIBROOT/libocn.a) then
  echo "ERROR: licom library not available"
  exit -1
endif

echo " "
echo -------------------------------------------------------------------------
echo  Successful completion of the licom executable building process
echo -------------------------------------------------------------------------
