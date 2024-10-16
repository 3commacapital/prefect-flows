from datetime import datetime

from services.debank import Debank
from services.nhaga_db import session, Valuation

from prefect.blocks.system import Secret
from prefect import task, flow, get_run_logger, variables

secret_block = Secret.load("debank-api")
DEBANK_KEY = secret_block.get()


@task(name="Check wallet Value", task_run_name="check-wallet-value-{date}-{wallet}")
def check_wallet_value_exists(date, wallet):
    return session.query(Valuation).filter_by(date=date, wallet_address=wallet).scalar()


@task(name="Get Wallet Value", task_run_name="get-wallet-value-{wallet}")
def get_wallet_value(wallet, debank):
    res = debank.total_value(wallet)
    return res.json().get("total_usd_value")


@task(name="Save Wallet Valuations", task_run_name="save-wallet-value-{wallet}")
def save_wallet_value(date, wallet, value):
    session.add(Valuation(date=date, value=value, wallet_address=wallet))


@flow(name="01 Get Wallet Valuations")
def get_wallet_valuaions():
    logger = get_run_logger()

    wallets = variables.get("wallets")
    debank = Debank(DEBANK_KEY)
    today = datetime.now().strftime("%Y-%m-%d")
    for wallet in wallets:
        if not check_wallet_value_exists(today, wallet):
            val = get_wallet_value(wallet, debank)
            save_wallet_value(today, wallet, val)
            logger.info(f"Saving {today} valuation for {wallet}: {val:+,.2f}")
        else:
            logger.info(f"Valuation for {today} and {wallet} already exists")
    session.commit()


if __name__ == "__main__":
    get_wallet_valuaions()
