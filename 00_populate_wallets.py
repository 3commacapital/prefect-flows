from services.nhaga_db import session, Valuation, Wallet, Snapshot
import pandas as pd
from prefect import flow, get_run_logger, task, variables


def save_wallets():
    wallets = variables.get("wallets")
    for name, address in wallets:
        session.add(Wallet(address=address, name=name))
    session.commit()


@task(name="Save Wallet Valuations", task_run_name="save-wallet-value-{wallet}")
def save_wallet_value(date, wallet, value):
    logger = get_run_logger()
    existing = (
        session.query(Valuation).filter_by(date=date, wallet_address=wallet).scalar()
    )

    if not existing:
        session.add(Valuation(date=date, value=value, wallet_address=wallet))
        logger.info(f"Saving {date} valuation for {wallet}: {value:+,.2f}")
    else:
        logger.info(f"Valuation for {date} and {wallet} already exists")


@flow
def save_past_valuations():
    valuations = pd.read_csv("../3comma_regular_valuations/3comma_valuations.csv")

    for row in valuations.head().itertuples():
        save_wallet_value(row.date, row.address, row.value)
    session.commit()


def save_past_snapshots():
    snapshots = pd.read_csv("../3comma_regular_valuations/3comma_snapshots.csv")

    for row in snapshots.head().itertuples():
        print(row)
        # save_wallet_value(row.date, row.address, row.value)
    # session.commit()


if __name__ == "__main__":
    # save_past_valuations()
    save_past_snapshots()
