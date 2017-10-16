#1/bin/bash
cat > /dev/ttyUSB2 &

./cpp/run.sh | python . -z | ssh timothy@192.168.2.101 "cat > /home/timothy/avbotz/visualiser/visual"

& tail -f out.log
