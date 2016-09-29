#!/bin/sh

cd /home/zeppelin
./bin/zeppelin-daemon.sh start


cd /home/mesos/build
./bin/mesos-master.sh --ip="$(ip addr show eth0 | grep 'inet\b' | awk '{print $2}' | cut -d/ -f1)" --work_dir=/var/lib/mesos