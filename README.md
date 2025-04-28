# Spark Cluster Docker (Fork)

This repository is a **fork** of the original [Spark Cluster Docker](https://github.com/rockthejvm/spark-cluster-docker) created by [Rock the JVM](https://rockthejvm.com).

**Modifications in this fork:**

*   **Added MinIO Support:** Integrated a MinIO service (`minio/minio`) into the `docker-compose.yml` setup to provide an S3-compatible local object storage solution.
*   **Spark S3A Configuration:** Configured the Spark images (`jupyter-spark-base`, `jupyterlab`) with the necessary `hadoop-aws` and `aws-java-sdk-bundle` JARs and default S3A settings in `spark-defaults.conf` and `core-site.xml` to connect to the local MinIO instance via `s3a://` paths.
*  The cluster is set up for Spark 3.1.3 (updated from original 3.0.0). 
*    **Integrated `boto3` for MinIO Interaction:** The `jupyterlab` Docker image now includes `boto3`, the official AWS SDK for Python. This allows you to interact programmatically with the MinIO service directly from your Jupyter notebooks. You can use `boto3` to:
    *   Create buckets (as shown in example notebooks, reading credentials from environment variables).
    *   List buckets and objects.
    *   Upload or download files directly (though Spark's `s3a://` connector is typically used for data processing).
    *   Manage other S3-compatible operations.

---


## How to Run Locally

**Prerequisites:**

*   Docker and Docker Compose installed on your OS.

**Steps:**

1.  **Clone The Repo:**
    ```bash
    git clone git@github.com:vasevooo/spark-cluster-docker-with-minio.git
    cd spark-cluster-docker-with-minio
    ```

2.  **Build Docker Images:**
    This script builds the base images, Spark master/worker, JupyterLab (with S3 support), etc.
    ```bash
    ./build-images.sh
    ```
    *(This might take some time, especially the first time.)*

3.  **Start the Services:**
    This command starts the Spark master, workers, JupyterLab, PostgreSQL, and the MinIO service in detached mode (`-d`).
    ```bash
    docker-compose up -d
    ```

4.  **Access Services:**
    *   **JupyterLab:** http://localhost:8888
    *   **MinIO Console:** http://localhost:9001 (Log in with credentials from `docker-compose.yml`)
    *   **Spark Master UI:** http://localhost:8080
    *   Spark Worker UIs: http://localhost:8081, http://localhost:8082 
    *   Spark Application UI (when running a job): http://localhost:4040

5.  **(Optional) Create MinIO Bucket:**
    *   If not using automatic creation (e.g., via `boto3` in a notebook), log into the MinIO Console (http://localhost:9001) and create a bucket (e.g., `test-bucket`) before trying to write to it from Spark.

6.  **Stop the Services:**
    ```bash
    docker-compose down
    ```
    *(Use `docker-compose down -v` to also remove the data volumes like `minio-data` and `shared-workspace` if you want a completely clean start next time).*


## Other Tools


To kill the cluster without stopping the containers gracefully, hit Ctrl-C in the terminal running `docker-compose up` (if not detached), or run this command from another terminal:
```bash
docker-compose kill
```

To remove the containers (but not necessarily volumes), run:
```bash
docker-compose rm
```

To start a (Scala) Spark Shell:
```bash
./start-spark-shell.sh
```

To start a PySpark shell:
```bash
./start-pyspark.sh
```

To start a Spark SQL shell:
```bash
./start-spark-sql.sh
```

## PostgreSQL

*(Keep PostgreSQL section)*
This setup also has a SQL database (PostgreSQL) for students to access from Apache Spark. The database comes preloaded with a smaller version of the classical fictitious "employees" database.

To open a PSQL shell and manage the database manually, run the helper script:
```bash
./psql.sh
```

## How to upload data to the Spark cluster

You have two options:

1.  Use the JupyterLab upload interface while it's active.
2.  Copy your data to `shared-workspace` &mdash; the directory is auto-mounted on all the containers.

## How to port your notebooks to another Jupyter instance

Similar options:

1.  Use the JupyterLab interface to download your notebooks as `.ipynb` files.
2.  Copy the `.ipynb` files directly from the `shared-workspace` directory: everything you save will be immediately visible there.