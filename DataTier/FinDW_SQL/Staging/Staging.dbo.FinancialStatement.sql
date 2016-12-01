USE FinDW
GO

-- CREATE SCHEMA Staging;
GO

-- DROP TABLE FinDW.Staging.FinancialStatement;
-- GO
-- CREATE TABLE FinDW.Staging.FinancialStatement
-- (
-- 	import_path varchar(500)
-- 	,CIDStr int
-- 	,StatementIDStr int
-- 	,download_date varchar(500)
-- 	,FiscalQuarterStr int
-- 	,PeriodEndDateStr varchar(500)
-- 	,AccountStr varchar(500)
-- 	,SubAccountStr varchar(500)
-- 	,ValueStr bigint
-- )

-- -- C:/Users/user/Dropbox/sublime_config/pymake.py

-- TRUNCATE TABLE FinDW.Staging.FinancialStatement;
-- GO
SELECT COUNT(*)
FROM FinDW.Staging.FinancialStatement