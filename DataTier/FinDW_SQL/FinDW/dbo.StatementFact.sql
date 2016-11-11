CREATE TABLE [dbo].[StatementFact]
(
	StatementFactID numeric(20,0)
	,CID bigint NOT NULL
	-- ,FiscalYear int NOT NULL
	,FiscalQuarter smallint NOT NULL
	,PeriodEndDateID int NOT NULL
	,StatementID smallint NOT NULL
	,AccountID int NOT NULL
	,SubAccountID int NULL
	,Value bigint NOT NULL
	,CONSTRAINT PK_StatementFact PRIMARY KEY CLUSTERED (StatementFactID)
)
