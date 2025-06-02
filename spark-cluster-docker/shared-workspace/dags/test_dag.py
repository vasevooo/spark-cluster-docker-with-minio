from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.empty import EmptyOperator
from airflow.models import Variable

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 27),
    'email_on_failure': False, 
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='simple_spark_test',
    default_args=default_args,
    schedule_interval='@once',
    catchup=False,
    tags=['example', 'spark'],
) as dag:

    start = EmptyOperator(task_id='start')

    spark_job = SparkSubmitOperator(
        task_id='run_simple_spark_job',
        application='/opt/airflow/dags/simple_spark_app.py',  # путь к вашему spark приложению
        conn_id='spark_connection',  # имя Spark connection в Airflow
        name='simple_spark_test_job',
        verbose=True,
        conf={
            "spark.jars.repositories": "https://mmlspark.azureedge.net/maven",
            "spark.jars.packages": "org.apache.hadoop:hadoop-aws:3.2.0,org.apache.hadoop:hadoop-common:3.2.0",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
            "spark.hadoop.fs.s3a.endpoint": Variable.get("s3_endpoint_url"),
            "spark.hadoop.fs.s3a.access.key": Variable.get("s3_key"),
            'spark.hadoop.fs.s3a.aws.credentials.provider': 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider',
            "spark.hadoop.fs.s3a.secret.key": Variable.get("s3_secret")
        },
    )

    end = EmptyOperator(task_id='end')

    start >> spark_job >> end
