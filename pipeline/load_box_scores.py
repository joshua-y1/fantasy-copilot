import os
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv() # reads .env so the key path and project ID are available

SEASON = "2026-27" 
DATASET = "fantasy_raw"
TABLE = "box_scores"

def section(title):
    print(f"\n{'=' * 50}\n{title}\n{'=' * 50}")

def load(season):
    # 1. connect to BigQuery as pipeline-loader 
    client = bigquery.Client(project=os.getenv("GCP_PROJECT_ID"))
    
    # 2. where the data comes from and where it goes
    file_path = f"data/raw/box_scores_{season}.parquet"
    table_id = f"{client.project}.{DATASET}.{TABLE}"
     
    # 3. upload settings: parquet format, replace the table each run
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    
    # 4. upload the file and wait for it to finish
    with open(file_path, "rb") as f:
        job = client.load_table_from_file(f, table_id, job_config=job_config)
    job.result()
    
    # 5. ask BigQuery how many rows landed
    table = client.get_table(table_id)
    return table_id, table.num_rows

if __name__ == "__main__":
    table_id, num_rows = load(SEASON)
    section("Load Complete")
    print(f"{num_rows:,} rows loaded into {table_id}")