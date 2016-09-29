FROM ubuntu:14.04

RUN apt-get update && apt-get install -y tar wget git && apt-get install -y openjdk-7-jdk && apt-get install -y autoconf libtool && apt-get -y install build-essential python-dev libcurl4-nss-dev libsasl2-dev libsasl2-modules maven libapr1-dev libsvn-dev

WORKDIR /home
RUN git clone https://git-wip-us.apache.org/repos/asf/mesos.git

WORKDIR /home/mesos
RUN ./bootstrap && mkdir -p /home/mesos/build
WORKDIR /home/mesos/build
RUN ../configure && make && make install
WORKDIR /home/mesos/build
COPY slave_start.sh /home
WORKDIR /home
RUN chmod 777 /home/slave_start.sh
EXPOSE 5050
CMD ["./slave_start.sh"]