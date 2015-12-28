# FinDW
Data Warehouse for financial statement data and stock prices
## Strictly Structure and ETL
### source folders
- stmt
	- py _python html download and parse scipts_
	- schema _sql database, schema, table, index creation scripts_
	- etl _ssis etl projects_

### data flow
- raw html is downloaded
	[ ] python querys SSISDB to get list of spec (cid, period count) tuples
- html is parsed into csv
- csv is loaded into staging schema
- 

