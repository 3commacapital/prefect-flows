from datetime import datetime

from prefect import task, flow, get_run_logger

wallets = {
    "3C2": "0x417Ae5C04990507dE1552CC45a6A2BcdF27D01b3",
    "3C3": "0xA60B57183494973D6f5Dad9D967ca90982167455",
    "3C4": "0x825825cD8A38AB5a3EF402C0Baf8422428ce69c4",
    "3C5": "0x4ab010562AaF2417e9BFA776eBc2579Ba9C1EADF",
    "3C6": "0x6eF2730CA247a63bC2c11dC025052D0d97351E32",
    "3C8": "0xBCd6d81451C29E665feEC8a2028E40bd888cE5B0",
    "3C10": "0x74E671372EEB8c78Cf686EfF5252B31907953baF",
}


@task(
        name="Get Wallet Value",
        task_run_name="get-wallet-value-{wallet}",
    )
def get_wallet_value(wallet):
    return 555

@flow
def write_wallets():
    logger = get_run_logger()
    data = []
    dt = datetime.now().strftime("%Y-%m-%d")
    for label, wallet in wallets.items():
        value = get_wallet_value(wallet)
        data.append([dt, wallet, value])
        logger.info(f"Writing {wallet} with value {value}")




if __name__ == "__main__":
    write_wallets()
