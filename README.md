# 3Comma Tasks

## Tasks

| # | Name | Frequency |
|---|---|---|
| 01 | Wallet valuations | Daily |
| 02 | Wallet snapshots | Daily |
| 03 | Funds (Global Growth) pre close files | Daily |
| 04 | Funds close analysis | Daily |
| 05 | Send Fund prices to bloomberg | Daily |
| 06 | Factsheet data | Weekly |
| 07 | Send VaR to CMVM | Monthly |
| 08 | Save Benchmark values to DB | Daily |


## Configure

prefect profile use 'nhaga.xyz'

prefect config set PREFECT_API_URL="http://nhaga.xyz:4200/api"


### Deployment
prefect deploy
cron pattern 0 16 * * *