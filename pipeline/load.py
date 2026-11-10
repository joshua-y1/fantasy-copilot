import os
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv() # reads .env so the key path and project ID are available

SEASON = "2026-27" 
DATASET = "fantasy_raw"
# CHANGED: removed TABLE. Each call now says which table it loads.

def section(title):
    print(f"\n{'=' * 50}\n{title}\n{'=' * 50}")

def load(file_path, table): # CHANGED: takes the file and table as inputs
    # 1. connect to BigQuery as pipeline-loader 
    client = bigquery.Client(project=os.getenv("GCP_PROJECT_ID"))
    
    # 2. where the data goes (file_path now comes in as an input)
    table_id = f"{client.project}.{DATASET}.{table}" # CHANGED: uses the input
     
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
    table_obj = client.get_table(table_id) # CHANGED: renamed so it doesn't clash with the input
    return table_id, table_obj.num_rows

if __name__ == "__main__":
    section("Load Complete")
    # CHANGED: one line per file and table to load
    for file_path, table in [
        (f"data/raw/box_scores_{SEASON}.parquet", "box_scores"),
        (f"data/raw/schedule_{SEASON}.parquet", "schedule"),
    ]:
        table_id, num_rows = load(file_path, table)
        print(f"{num_rows:,} rows loaded into {table_id}")