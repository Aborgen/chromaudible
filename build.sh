#!/usr/bin/env bash
set -e

outDir=./build

serverDir=back/
clientDir=front/

if [ -d "$outDir" ] 
then
  rm -rf "$outDir"
fi

mkdir "$outDir"
printf "Directory $outDir prepared\n"
cp "$serverDir"/server.py "$outDir"/main.py
cp -a "$serverDir"/src "$outDir"/src
printf "Copied python server to $outDir\n\n"
sleep 0.600

if [ ! -d "$clientDir/node_modules" ]
then
  printf "node_modules not found, installing app"
  sleep 0.600
  npm install --prefix="$clientDir" | tee /dev/tty
fi

npm run --prefix="$clientDir" build | tee /dev/tty
