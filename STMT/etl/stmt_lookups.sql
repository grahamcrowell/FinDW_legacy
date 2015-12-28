USE FinDW
GO

IF EXISTS (SELECT * FROM sys.objects WHERE name = 'StatementLookup' and type = N'P')
BEGIN
	PRINT 'drop dbo.StatementLookup'
	DROP PROCEDURE dbo.StatementLookup
END	
GO

PRINT 'create StatementLookup'
GO

CREATE PROCEDURE dbo.StatmentLookup 
AS
BEGIN
	UPDATE FinDW.staging.Statement SET CID = CAST(CIDStr AS int);

	UPDATE FinDW.staging.Statement SET PeriodEndDateID = dt_dim.DateID
		FROM dim.Date AS dt_dim
		WHERE dt_dim.mdy = PeriodEndDateStr

	UPDATE FinDW.staging.Statement SET FiscalQuarter = CAST(FiscalQuarterStr AS int);

	UPDATE FinDW.staging.Statement SET StatementID = CAST(StatementIDStr AS int);

	UPDATE FinDW.staging.Statement SET AccountID = acct_dim.AccountID 
		FROM dim.Account AS acct_dim
		WHERE acct_dim.AccountName = AccountStr

	UPDATE FinDW.staging.Statement SET SubAccountID = sub_dim.SubAccountID 
		FROM dim.SubAccount AS sub_dim
		WHERE sub_dim.SubAccountName = SubAccountStr

	UPDATE FinDW.staging.Statement SET Value = CAST(VALUEStr AS bigint);
END
GO

IF OBJECT_ID('StatementFactLoad','P') IS NOT NULL
BEGIN
	PRINT 'drop dbo.StatementFactLoad'
	DROP PROCEDURE dbo.StatementFactLoad
END	
GO

PRINT 'create StatementFactLoad'
GO
CREATE PROCEDURE dbo.StatementFactLoad
AS
BEGIN

	TRUNCATE TABLE FinDW.dbo.Statement;

	MERGE FinDW.dbo.[Statement] AS target 
	USING (
	SELECT 
		--getFactID(CID, PeriodEndDateID, StatementID, AccountID, SubAccountID) AS FactID
		CID
		,FiscalQuarter
		,PeriodEndDateID
		,StatementID
		,AccountID
		,SubAccountID
		,Value 
	FROM FinDW.staging.[Statement]) AS source (
		--getFactID(CID, PeriodEndDateID, StatementID, AccountID, SubAccountID) AS FactID
		CID
		,FiscalQuarter
		,PeriodEndDateID
		,StatementID
		,AccountID
		,SubAccountID
		,Value
	)
	ON (
		--source.FactID = target.FactID
		dbo.getFactID(source.CID, source.PeriodEndDateID, source.StatementID, source.AccountID, source.SubAccountID) = target.FactID
		AND source.CID = target.CID
		AND source.PeriodEndDateID = target.PeriodEndDateID
		AND source.StatementID = target.StatementID
		AND source.AccountID = target.AccountID
		AND source.SubAccountID = target.SubAccountID
	)
	WHEN MATCHED THEN 
	UPDATE SET Value = source.Value
	WHEN NOT MATCHED THEN 
	INSERT (
		FactID
		,CID
		,FiscalQuarter
		,PeriodEndDateID
		,StatementID
		,AccountID
		,SubAccountID
		,Value
	)
	VALUES (
		dbo.getFactID(source.CID, source.PeriodEndDateID, source.StatementID, source.AccountID, source.SubAccountID)
		,source.CID
		,source.FiscalQuarter
		,source.PeriodEndDateID
		,source.StatementID
		,source.AccountID
		,source.SubAccountID
		,source.Value
	);
END
GO