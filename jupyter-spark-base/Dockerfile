FROM jupyter-cluster-base

# -- Layer: Apache Spark

ARG spark_version=3.1.3
ARG hadoop_version=3.2
ARG HADOOP_AWS_VERSION=3.2.0
ARG AWS_SDK_VERSION=1.11.375

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends curl && \
    curl https://archive.apache.org/dist/spark/spark-${spark_version}/spark-${spark_version}-bin-hadoop${hadoop_version}.tgz -o spark.tgz && \
    tar -xf spark.tgz && \
    mv spark-${spark_version}-bin-hadoop${hadoop_version} /usr/bin/ && \
    mkdir /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}/logs && \
    rm spark.tgz && \
    SPARK_HOME=/usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version} && \
    curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_AWS_VERSION}/hadoop-aws-${HADOOP_AWS_VERSION}.jar -o $SPARK_HOME/jars/hadoop-aws-${HADOOP_AWS_VERSION}.jar && \
    curl https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_VERSION}/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar -o $SPARK_HOME/jars/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar && \
    echo "spark.hadoop.fs.s3a.endpoint                 http://minio:9000" >> $SPARK_HOME/conf/spark-defaults.conf && \
    echo "spark.hadoop.fs.s3a.access.key               minio" >> $SPARK_HOME/conf/spark-defaults.conf && \
    echo "spark.hadoop.fs.s3a.secret.key               minio123" >> $SPARK_HOME/conf/spark-defaults.conf && \
    echo "spark.hadoop.fs.s3a.path.style.access        true" >> $SPARK_HOME/conf/spark-defaults.conf && \
    echo "spark.hadoop.fs.s3a.impl                     org.apache.hadoop.fs.s3a.S3AFileSystem" >> $SPARK_HOME/conf/spark-defaults.conf && \
    echo "spark.hadoop.fs.s3a.connection.ssl.enabled   false" >> $SPARK_HOME/conf/spark-defaults.conf && \
    # Clean up apt cache
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV SPARK_HOME /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}
ENV SPARK_MASTER_HOST jupyter-spark-master
ENV SPARK_MASTER_PORT 7077
ENV SPARK_UI_PORT 4040
ENV PYSPARK_PYTHON python3

# -- Runtime

WORKDIR ${SPARK_HOME}
