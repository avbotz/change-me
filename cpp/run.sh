#!/bin/bash
PAT=`realpath $0`
cd "dirpath=$PAT"

DATE=logs/`date +%Y-%m-%d_%H-%M-%S`

mkdir cpp/$DATE
mkdir cpp/$DATE/rbuoys
mkdir cpp/$DATE/pvc
mkdir cpp/$DATE/path
mkdir cpp/$DATE/original
mkdir cpp/$DATE/flashlight

./cpp/bin/interface cpp/$DATE/
