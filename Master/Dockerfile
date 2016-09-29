FROM ubuntu:14.04


RUN apt-get update && apt-get install -y tar \
    wget \
    openjdk-7-jdk \
    autoconf \
    libtool \
    build-essential \
    python-dev \
    libfuse-dev \
    libssl-dev \
    libxml2-dev \
    libcurl4-nss-dev \
    libsasl2-dev \
    libsasl2-modules \
    libapr1-dev \
    libsvn-dev \
    autotools-dev \
    g++ \
    make \
    pkg-config \
    git \
    exfat-fuse \
    exfat-utils \
    curl


WORKDIR /tmp
RUN wget http://apache.mirror.anlx.net/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz && tar -zxf apache-maven-3.3.9-bin.tar.gz && cp -R apache-maven-3.3.9 /usr/local && ln -s /usr/local/apache-maven-3.3.9/bin/mvn /usr/bin/mvn && ln -s /usr/local/apache-maven-3.3.9/bin/mvnDebug /usr/bin/mvnDebug && rm  /tmp/apache-maven-3.3.9-bin.tar.gz && rm -rf /tmp/apache-maven-3.3.9


ENV SCALA_VERSION 2.11.5
ENV SCALA_DEB_FILE_NAME=scala-$SCALA_VERSION.deb
RUN wget http://www.scala-lang.org/files/archive/$SCALA_DEB_FILE_NAME
RUN dpkg -i $SCALA_DEB_FILE_NAME
RUN rm -f $SCALA_DEB_FILE_NAME


ENV SBT_VERSION 0.13.7
ENV SBT_DEB_FILE_NAME=sbt-$SBT_VERSION.deb
RUN wget https://dl.bintray.com/sbt/debian/$SBT_DEB_FILE_NAME
RUN dpkg -i $SBT_DEB_FILE_NAME
RUN rm -f $SBT_DEB_FILE_NAME


WORKDIR /home 
RUN git clone https://github.com/SciSpark/SciSpark.git
WORKDIR /home/SciSpark
RUN sbt clean assembly


ENV ZEPPELIN_PORT 8080
ENV ZEPPELIN_HOME /usr/zeppelin
ENV ZEPPELIN_CONF_DIR $ZEPPELIN_HOME/conf
ENV ZEPPELIN_NOTEBOOK_DIR $ZEPPELIN_HOME/notebook

WORKDIR /home
RUN git clone https://github.com/apache/zeppelin.git
WORKDIR /home/zeppelin
RUN mvn clean install -DskipTests


ENV ZEPPELIN_JAVA_OPTS="-Dspark.jars=/home/SciSpark/target/scala-2.11/SciSpark.jar -Dspark.executor.memory=6g"
ENV SPARK_SUBMIT_OPTIONS="--jars /home/SciSpark/target/scala-2.11/SciSpark.jar --driver-java-options -Xmx20g"
ENV ZEPPELIN_WEBSOCKET_MAX_TEXT_MESSAGE_SIZE="1048576"


WORKDIR /home
RUN git clone https://git-wip-us.apache.org/repos/asf/mesos.git
WORKDIR /home/mesos
RUN ./bootstrap && mkdir -p /home/mesos/build
WORKDIR /home/mesos/build
RUN ../configure && make && make install
WORKDIR /home


RUN wget http://d3kbcqa49mib13.cloudfront.net/spark-2.0.0-bin-hadoop2.7.tgz && tar -zxf spark-2.0.0-bin-hadoop2.7.tgz && rm spark-2.0.0-bin-hadoop2.7.tgz
WORKDIR /home/spark-2.0.0-bin-hadoop2.7/conf
RUN cp spark-env.sh.template spark-env.sh && echo "export MESOS_NATIVE_JAVA_LIBRARY=/usr/local/lib/libmesos.so" >> spark-env.sh && echo "export SPARK_EXECUTOR_URI=http://d3kbcqa49mib13.cloudfront.net/spark-2.0.0-bin-hadoop2.7.tgz" >> spark-env.sh  && echo "$(ip addr show eth0 | grep 'inet\b' | awk '{print $2}' | cut -d/ -f1)"


COPY master_start.sh /home
WORKDIR /home
RUN cat /home/master_start.sh && chmod 777 /home/master_start.sh
CMD ["./master_start.sh"]