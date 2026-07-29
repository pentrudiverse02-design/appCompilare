#!/usr/bin/env bash

GenRandNameFolder()
{
  nrCharsForName=10
  tr -dc A-Za-z0-9 </dev/urandom | head -c ${nrCharsForName}
}
random()
{
  echo $(( (( RANDOM % $1 )) +1 ))
}
#set -x
cd clientdir/ZipsToBorrow || exit 1
echo ""
pwd
ls
zips=($(ls -x *.zip))
echo "${zips[@]}"
cd .. || exit 1
echo ""
pwd
ls
sysarhi=( x86_64 arm64 aarch_64 )
compileFor=( RELEASE DEBUG LIBRARY )

lenZips="${#zips[@]}"
lenSys="${#sysarhi[@]}"
lenComp="${#compileFor[@]}"

nrClients=1

mkdir clients
echo ""
pwd
ls

cd clients
echo "inainte de for clients"
pwd
ls

echo ""
echo ""
echo ""
echo ""
variabilaRandCompile=$(($(random ${lenComp})-1))
variabilaRandArchitecture=$(($(random ${lenSys})-1))
vc=${compileFor[${variabilaRandCompile}]}
echo "${vc}"
vs=${sysarhi[${variabilaRandArchitecture}]}
echo "${vs}"
vstay=$(($(random 2)-1))

nume=$(GenRandNameFolder)
echo "${nume}"

mkdir ${nume}
echo "11"
pwd
ls

cd ..
echo "INCEPEM COPIERE"
pwd
ls
#
limita=$(random lenZips)
#  limita=10
echo "  o sa copiem pentru ${limita} .zips"
for ((j=0;j<limita;j++)); do
  index=$(($(random ${lenZips})-1))
  zipul="ZipsToBorrow/${zips[${index}]}"
  destinatia="clients/${nume}"
#    echo "${zipul}"
#    echo  "${destinatia}"
  cp ${zipul} ${destinatia}
#    echo ""
done

echo "TERMINAM COPIERE"
cd ..
pwd
ls

python3 -m clientdir.client -comp ${vc} -archi ${vs} -s ${vstay} -f ${nume}
cd clientdir/clients || exit 1
echo "44"
pwd
ls
