#!/bin/bash

DATE=logs/`date +%Y-%m-%d_%H-%M-%S`

mkdir $DATE
mkdir $DATE/rbuoys
mkdir $DATE/pvc
mkdir $DATE/path
mkdir $DATE/original
mkdir $DATE/flashlight

./bin/interface $DATE/
