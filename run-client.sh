#!/usr/bin/env bash
cd clientdir/ZipsToBorrow || exit 1
zips=( *.zip )
for zip in "${zips[@]}"; do
  echo "$zip"
done
nrClients=2
ls
cd ..

for ((i=0;i<nrClients;i++)); do
  

done