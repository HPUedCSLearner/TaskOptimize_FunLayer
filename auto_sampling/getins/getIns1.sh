tmp=$*


tmp=${tmp##*/}


sourcebc=${tmp%.*}.bc

sources=${tmp%.*}.s
sourceo=${tmp%.*}.o


opt -load $CASEROOT/sampling/pass/GetUsrDF.so -GetUsrDF $sourcebc -o $sourcebc

llc $sourcebc -o $sources
as $sources -o $sourceo


