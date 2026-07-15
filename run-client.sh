#!/usr/bin/env bash

GenRandNameFolder()
{
  nrCharsForName=10
  tr -dc A-Za-z0-9 </dev/urandom | head -c ${nrCharsForName}
}
cd clientdir/ZipsToBorrow || exit 1
zips=( *.zip )
cd ..
sysarhi=( x86_64 arm64 aarch_64 )
compileFor=( RELEASE DEBUG LIBRARY )

randZips=$(( $RANDOM % ${#zips[@]} ))
#echo ${arr[$rand]}
randSys=$[$RANDOM % ${#sysarhi[@]}]
randComp=$[$RANDOM % ${#compileFor[@]}]

#for zip in "${zips[@]}"; do
#  echo "$zip"
#done
nrClients=2
ls
for ((i=0;i<nrClients;i++)); do
  vc=${compileFor[randComp]}
  vs=${sysarhi[randSys]}
  nume=${GenRandNameFolder}
  mkdir ${nume}
  for ((j=0;j<${randZips};j++)); do
      cp ZipsToBorrow/${zips[randZips]} ${nume}
  done
  cd ..
  python3 -m clientdir.client ${vc} ${vs} ${RANDOM}%2 ${nume}
done
