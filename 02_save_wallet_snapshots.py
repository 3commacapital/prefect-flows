from datetime import datetime

from services.debank import Debank
from services.nhaga_db import session, Snapshot

from prefect.blocks.system import Secret
from prefect import task, flow, get_run_logger, variables

secret_block = Secret.load("debank-api")
DEBANK_KEY = secret_block.get()


@task(
    name="Check wallet Snapshot", task_run_name="check-wallet-snapshot-{date}-{wallet}"
)
def check_wallet_snapshot_exists(date, wallet):
    return session.query(Snapshot).filter_by(date=date, wallet_address=wallet).scalar()


@task(name="Get Wallet Snapshot", task_run_name="get-wallet-snapshot-{wallet}")
def get_wallet_snapshot(wallet, debank):
    tokens = debank.tokens(wallet)
    projects = debank.project_list(wallet)
    return tokens.text, projects.text


@task(name="Save Wallet Snapshots", task_run_name="save-wallet-snapshots-{wallet}")
def save_wallet_snapshot(date, wallet, tokens, projects):
    session.add(
        Snapshot(date=date, tokens=tokens, projects=projects, wallet_address=wallet)
    )


@flow(name="02 Get Wallet Snapshots")
def get_wallet_snapshots():
    logger = get_run_logger()

    wallets = variables.get("wallets")
    debank = Debank(DEBANK_KEY)
    today = datetime.now().strftime("%Y-%m-%d")
    for wallet in wallets:
        if not check_wallet_snapshot_exists(today, wallet):
            tokens, projects = get_wallet_snapshot(wallet, debank)
            save_wallet_snapshot(today, wallet, tokens, projects)
            logger.info(f"Saving {today} snapshot for {wallet}")
        else:
            logger.info(f"Snapshot for {today} and {wallet} already exists")
    session.commit()


if __name__ == "__main__":
    get_wallet_snapshots()
