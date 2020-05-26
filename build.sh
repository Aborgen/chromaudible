#!/usr/bin/env bash

outDir=./build

serverDir=back/
vueDir=front/

[ -d $outDir ] && rm -rf $outDir && mkdir $outDir
cp $serverDir/server.py $outDir/main.py
cp $serverDir/requirements.txt $outDir/requirements.txt
cp -a $serverDir/src $outDir/src
echo "Directory $outDir prepared"

npm run --prefix=$vueDir build | tee /dev/tty
