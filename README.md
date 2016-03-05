# FinDW
Data Warehouse for financial statement data and stock prices
## Strictly Structure and ETL
### source folders
- stmt
	- py _python html download and parse scipts_
	- schema _sql database, schema, table, index creation scripts_
	- etl _ssis etl projects_

## C# and python interface
download_html_stmt.py and parse_html_stmt.py called from C#
python does not interface with database

### data flow
- raw html is downloaded
	- [ ] python download and parse scripts called from C#
- html is parsed into csv
	- [ ] python parses all html in parsing folder
- csv is loaded into staging schema
	- [ ] SSIS loads csv
	- [ ] SSIS moves files to completed or failed folders

