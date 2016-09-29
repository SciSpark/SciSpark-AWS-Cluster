#!/bin/sh

cd /home/mesos/build
./bin/mesos-slave.sh --master=$master_ip:5050 --work_dir=/var/lib/mesos
