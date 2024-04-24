# Real-Time Sales Data Pipeline with Kafka, Spark, Cassandra, and Redash

This repository provides a real-time sales data pipeline that ingests, processes, and stores sales data using Kafka, Spark, Cassandra, and Redash. It offers a comprehensive solution for streaming data analysis and visualization.

## Getting Started:

Follow these steps to set up and run the Real-Time Sales Data Pipeline:

### 1. Clone the Repository:
```bash
git clone https://github.com/saadkh1/Real-Time_Sales_Data_Pipeline_Kafa_Spark_Cassandra_Redash
```

### 2. Navigate to the Project Directory:
```bash
cd Real-Time_Sales_Data_Pipeline_Kafa_Spark_Cassandra_Redash
```

### 3. Run Docker Compose:

* Windows:
```bash
run.bat
```

* Linux:
```bash
run.sh
```

This command will use Docker Compose to start all the necessary Docker containers, including Kafka, Spark, Cassandra, and the FastAPI service. It will also create the Kafka topic and sets up the Cassandra keyspace and table.

### 4. Run Data Generators:

The `api-pos` directory contains Python scripts (`api_pos_1.py` and `api_pos_2.py`) that simulate sales data using the POST method. These scripts will send data to the FastAPI service, which will then forward it to the Kafka topic.

```bash
cd api-pos
python api_pos_1.py &  # Run in background
python api_pos_2.py &  # Run in background (optional for more data)
```

## Pipeline Overview:

### 1. Data Generation (Optional):
* The api-pos scripts (if run) generate synthetic sales data.
### 2. Data Ingestion:
* The generated data is sent to the FastAPI service using POST requests.
### 3. Data Processing by FastAPI:
* The FastAPI service receives the data and sends it to the Kafka topic.
### 4. Real-Time Data Stream:
* Kafka acts as a real-time message broker, streaming the sales data to the Spark application.
### 5. Data Processing by Spark:
* A Spark job continuously reads data from the Kafka topic.
* The data is processed (data transformations).
### 6. Data Storage in Cassandra:
* The processed data is saved to the Cassandra table (sales_data).
### 7. Data Visualization with Redash:
* Redash dashboards can be created to visualize the real-time sales data stored in Cassandra.
