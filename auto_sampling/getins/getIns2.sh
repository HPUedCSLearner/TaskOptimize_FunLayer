tmp=$*

tmp=${tmp##*/}

sourcebc=${tmp%.*}.bc

sources=${tmp%.*}.s
sourceo=${tmp%.*}.o

opt -load $CASEROOT/sampling/pass/instrument_time_function.so -Ins_TimeFunc $sourcebc -o $sourcebc
opt -load $CASEROOT/sampling/pass/insert_tableline.so -Insert_Tableline $sourcebc -o $sourcebc

llc $sourcebc -o $sources
as $sources -o $sourceo
