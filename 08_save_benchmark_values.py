from prefect import task, flow, get_run_logger

from services.cf_benchmarks import CFBenchmark
from services.nhaga_db import session, AssetValue
from prefect.blocks.system import Secret
from datetime import datetime


secret_block = Secret.load("cfbenchmakrs-api")
CFBENCHMARKS_KEY = secret_block.get()
ASSET_ID = 2

@task(name="Save Benchmark Value", task_run_name="save-benchmark-value-{value_date}")
def save_benchmark_value(value_date, value):
    logger = get_run_logger()
    exists = session.query(AssetValue).filter_by(
        asset_id=ASSET_ID,
        date=value_date
        ).first()
    if exists:
        logger.info(f"Value for {value_date} already exists")
    else:

        logger.info("Inserting", value_date, value)
        session.add(
            AssetValue(
                asset_id = ASSET_ID,
                date=value_date,
                value=value
            )
        )
        session.commit()

@flow(name="08 Save Benchmark values to DB")
def save_benchmark_values():
    cf = CFBenchmark(CFBENCHMARKS_KEY)
    values = cf.values("UC5_EUR_RR_TR")
    value_date = datetime.fromtimestamp(values[-1]['time'] / 1e3).strftime("%Y-%m-%d")
    value = values[-1]['value']
    save_benchmark_value(value_date, value)


if __name__ == "__main__":
    save_benchmark_values()