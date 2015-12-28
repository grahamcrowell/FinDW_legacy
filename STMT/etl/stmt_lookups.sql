USE FinDW
GO	

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

UPDATE FinDW.staging.Statement SET Value = CAST(ValueStr AS bigint);


MERGE FinDW.dbo.[Statement] AS target 
USING (
	SELECT 
		CID
		,FiscalQuarter
		,PeriodEndDateID
		,StatementID
		,AccountID
		,SubAccountID
		,Value 
FROM FinDW.staging.[Statement]) AS source (
	CID
	,FiscalQuarter
	,PeriodEndDateID
	,StatementID
	,AccountID
	,SubAccountID
	,Value
)
ON (
	source.CID = target.CID
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
		CONCAT(source.CID, source.PeriodEndDateID, source.StatementID, FORMAT(source.AccountID,'00#'), FORMAT(source.SubAccountID,'00#'))
		,source.CID
		,source.FiscalQuarter
		,source.PeriodEndDateID
		,source.StatementID
		,source.AccountID
		,source.SubAccountID
		,source.Value
	);
