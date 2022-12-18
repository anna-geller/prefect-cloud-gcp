"""
Example file to download: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet
"""
from datetime import datetime, timedelta
import pandas as pd
from prefect import task, get_run_logger
from prefect.tasks import task_input_hash
from typing import List
from urllib.error import HTTPError
from urllib.request import urlopen
from prefect_utils.postgres_pandas import PostgresPandas


MAIN_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/"


@task
def get_files_to_process(year: int = 2022, service_type: str = "yellow") -> List[str]:
    svc = f"{service_type}_tripdata_{year}"
    files = [f"{svc}-{str(i).zfill(2)}.parquet" for i in range(1, 13)]
    valid_files = []
    for file in files:
        try:
            status_code = urlopen(f"{MAIN_URL}{file}").getcode()
            if status_code == 200:
                valid_files.append(file)
        except HTTPError:
            pass
    return valid_files


@task
def extract(file_name: str) -> pd.DataFrame:
    logger = get_run_logger()
    try:
        raw_df = pd.read_parquet(f"{MAIN_URL}{file_name}")
        logger.info("Extracted %s with %d rows", file_name, len(raw_df))
        return raw_df
    except HTTPError:
        logger.warning("File %s is not available in TLC Trip Record Data")


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def transform(
    df: pd.DataFrame, file_name: str, service_type: str = "yellow"
) -> pd.DataFrame:
    df["file"] = file_name
    df[service_type] = service_type
    df["ingested"] = datetime.utcnow().isoformat()
    return df


@task
def load_to_postgres(df: pd.DataFrame, tbl: str, if_exists: str = "append") -> None:
    logger = get_run_logger()
    block = PostgresPandas.load("default")
    block.load_data(df, tbl, if_exists)
    logger.info("%d rows loaded to table %s", len(df), tbl)


@task
def extract_jaffle_shop(dataset: str) -> pd.DataFrame:
    file = f"https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/{dataset}.csv"
    return pd.read_csv(file)
