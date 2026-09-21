# Multi-City Weather Data Engineering Pipeline

An end-to-end data engineering pipeline that ingests hourly weather data
for multiple Indian cities from the Open-Meteo REST API, stores raw data
in AWS S3, processes it with Databricks and PySpark using a
Bronze--Silver--Gold architecture, models the curated data as a star
schema with Delta Lake, performs SQL analytics, and orchestrates the
workflow with Databricks Lakeflow Jobs.

## Architecture

``` text
                    Open-Meteo REST API
                            │
                            ▼
                    Python Ingestion
                            │
                            ▼
                         AWS S3
                      Raw JSON Data
                            │
                            ▼
                ┌───────────────────────┐
                │       Databricks      │
                │       PySpark         │
                └───────────┬───────────┘
                            │
                            ▼
                     Bronze Layer
                  weather_bronze
                            │
                            ▼
                     Silver Layer
                  weather_silver
                 Data Quality Checks
                            │
                            ▼
                      Gold Layer
                 ┌──────────┼──────────┐
                 ▼          ▼          ▼
           dim_location  dim_date  fact_weather
                 └──────────┼──────────┘
                            │
                            ▼
                      SQL Analytics
                            │
                            ▼
                  Databricks Lakeflow Jobs
             Bronze → Silver → Gold → SQL
```

## Project Overview

The project demonstrates a complete batch-oriented data engineering
workflow:

1.  Fetch weather data from a public REST API using Python.
2.  Store the raw JSON responses in AWS S3.
3.  Read and process the raw data in Databricks using PySpark.
4.  Create a Bronze layer containing structured hourly weather records.
5.  Transform and validate the data in the Silver layer.
6.  Build a Gold layer using dimensional/star-schema modeling.
7.  Store curated datasets as Delta tables.
8.  Run SQL analytics against the curated data.
9.  Orchestrate the complete workflow with Databricks Lakeflow Jobs.
10. Version-control the Databricks notebooks with Git/GitHub.

## Technology Stack

  Area                Technology
  ------------------- --------------------------
  Data Source         Open-Meteo REST API
  Ingestion           Python, Requests
  Object Storage      AWS S3
  Processing          Databricks, PySpark
  Storage Format      Delta Lake
  Data Architecture   Bronze / Silver / Gold
  Data Modeling       Star Schema
  Analytics           SQL
  Orchestration       Databricks Lakeflow Jobs
  Version Control     Git, GitHub

## Data Coverage

The pipeline currently processes:

-   **6 cities**
    -   Bengaluru
    -   Chennai
    -   Coimbatore
    -   Delhi
    -   Hyderabad
    -   Mumbai
-   **7 days** of hourly weather observations
-   **1,008 hourly records**
-   Weather attributes including:
    -   Temperature
    -   Relative humidity
    -   Precipitation
    -   Wind speed
    -   Timestamp
    -   City
    -   Latitude
    -   Longitude

## Pipeline Layers

### 1. Data Ingestion

The Python ingestion process sends requests to the Open-Meteo REST API
for each configured city and saves the API responses as JSON files.

The raw files are then stored in AWS S3.

``` text
Open-Meteo API
      ↓
Python / Requests
      ↓
Raw JSON
      ↓
AWS S3
```

The source data is preserved before transformation so that downstream
processing starts from the original ingested records.

### 2. Bronze Layer

The Bronze notebook reads the raw JSON files from S3 using PySpark.

The nested hourly weather arrays are exploded into individual hourly
records and stored as the Delta table:

``` text
weather_bronze
```

The Bronze layer contains fields such as:

``` text
city
latitude
longitude
timestamp
temperature_2m
relative_humidity_2m
precipitation
wind_speed_10m
```

### 3. Silver Layer

The Silver notebook reads:

``` text
weather_bronze
```

and performs data transformation and validation.

Transformations include:

-   Timestamp conversion
-   Date extraction
-   Hour extraction
-   Day-of-week derivation
-   Month derivation
-   Data-quality validation
-   Duplicate checking
-   Null checking
-   Range validation

The resulting curated table is:

``` text
weather_silver
```

### Data Quality Checks

The pipeline includes checks for:

-   Null city values
-   Null timestamps
-   Null temperature values
-   Null humidity values
-   Null precipitation values
-   Null wind-speed values
-   Duplicate `(city, timestamp)` records
-   Invalid humidity values
-   Invalid precipitation values
-   Invalid wind-speed values
-   Invalid temperature values

For the current dataset, the validated Silver output contains:

``` text
Total records: 1,008
Null values in validated fields: 0
Invalid values detected by range checks: 0
```

## 4. Gold Layer

The Gold notebook reads the Silver Delta table and creates a dimensional
model.

### Dimension: `dim_location`

Stores the city/location information:

``` text
location_id
city
latitude
longitude
```

Currently contains 6 city records.

### Dimension: `dim_date`

Stores date-related attributes:

``` text
date_id
date
year
month
month_name
day
day_of_week
```

Currently contains 7 date records.

### Fact: `fact_weather`

Stores the hourly weather measurements:

``` text
weather_id
location_id
date_id
timestamp
temperature
humidity
precipitation
wind_speed
```

The fact table currently contains 1,008 records.

### Star Schema

``` text
                  dim_location
                       │
                       │
                       ▼
                  fact_weather
                       ▲
                       │
                       │
                    dim_date
```

The dimensional model separates descriptive attributes from measurable
weather observations and allows the fact data to be analyzed by location
and date.

## SQL Analytics

A separate Databricks SQL notebook contains analytical queries against
the Silver and Gold tables.

The SQL analysis covers areas such as:

-   Weather records by city
-   Date-level analysis
-   Temperature analysis
-   Humidity analysis
-   Precipitation analysis
-   Wind-speed analysis
-   Dimension/fact validation
-   Data-quality validation

A total of **8 SQL analytical queries** were developed for the project.

## Orchestration

The complete workflow is orchestrated using **Databricks Lakeflow
Jobs**.

The job contains four dependent notebook tasks:

``` text
bronze_ingestion
       │
       ▼
silver_transformation
       │
       ▼
gold_modeling
       │
       ▼
gold_sql_analytics
```

Each task reads the persistent Delta table produced by the preceding
stage rather than relying on Python variables from another notebook.

The workflow has been successfully executed end-to-end.

## Repository Structure

``` text
Multi-City-Weather-Data-Engineering-Pipeline/
│
├── src/
│   └── api_ingestion.py
│
├── 01_Bronze_Weather_Ingestion.ipynb
├── 02_Silver_Weather_Transformation.ipynb
├── 03_Gold_Weather_Modeling.ipynb
├── 04_Gold_SQL_Analytics.ipynb
│
├── requirements.txt
│
└── README.md
```

## Key Engineering Concepts Demonstrated

-   REST API ingestion
-   Python-based data ingestion
-   AWS S3 object storage
-   JSON processing
-   PySpark DataFrame transformations
-   ETL pipeline design
-   Medallion architecture
-   Delta Lake tables
-   Data-quality validation
-   Duplicate detection
-   Dimensional modeling
-   Star schema design
-   Fact and dimension tables
-   SQL analytics
-   Databricks Lakeflow Jobs
-   Git/GitHub version control

## Project Outcome

The project demonstrates an end-to-end data pipeline from external API
ingestion through cloud storage, distributed processing, data-quality
validation, dimensional modeling, SQL analytics, workflow orchestration,
and source-code version control.

The current implementation processes 1,008 hourly weather observations
across 6 cities and 7 days, with validated Silver-layer data and a
Gold-layer star schema consisting of `fact_weather`, `dim_location`, and
`dim_date`.

## Author

**Akileshwaran S**

Integrated M.Tech -- Computer Science and Engineering\
VIT-AP University

GitHub: https://github.com/Konger121

LinkedIn: https://www.linkedin.com/in/akileshwarans/
