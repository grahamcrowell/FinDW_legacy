# FinDW
Platform for financial analysis.

## Analysis Tier

### Stock Portfolio Object Model

- Country
	- Name 
	- Currency

- Exchange : Country
	- Name
	- Type := {Stock, Option, Bond, Currency, OTC, Other}

- Asset
	- Symbol
	- Exchange
	- PossibleTranscationTypes

- Stock : Asset
	+ Symbol
	+ Name
	- PossibleTranscationTypes

- Transaction : Asset
	- SettleDate
	- SettleCost
	- TranscationType := {deposit, buy, sell, sellshort}

- IHolding
	- EpochDate
	- Name
	- Collection<Transactions>
	+ GetQuantityHeldAsOf(date)
	+ GetBookValueAsOf(date)
	+ GetMarketValueAsOf(date)


- Portfolio


### Performance Measuring

- [Internal Rate of Return]()
- [Modified Dietz method]()
- [Time-Weighted Return]()

#### Asset Allocation Models

- [Capital Asset Pricing Model](https://en.wikipedia.org/wiki/Capital_asset_pricing_model)
- [Jensen Alpha](https://en.wikipedia.org/wiki/Jensen%27s_alpha)
- [Treynor ratio](https://en.wikipedia.org/wiki/Treynor_ratio)
- [Sharpe Ratio]()
- [Value at Risk]()
- [Mean Variance Analysis]()
- [Fama-French 3 Factor Model](https://en.wikipedia.org/wiki/Fama%E2%80%93French_three-factor_model)
## Data Tier
SQL data warehouse for financial statement data and stock prices using dimensional modelling (ie star schema).

1. Python scrapes and downloads data from internet in flat data files
2. SSIS updates fact tables

### source folders
- stmt
	- py _python html download and parse scipts_
	- schema _sql database, schema, table, index creation scripts_
	- etl _ssis etl projects_


### data flow
- raw html is downloaded
	- [ ] python download and parse scripts called from C#
- html is parsed into csv
	- [ ] python parses all html in parsing folder
- csv is loaded into staging schema
	- [ ] SSIS loads csv
	- [ ] SSIS moves files to completed or failed folders

