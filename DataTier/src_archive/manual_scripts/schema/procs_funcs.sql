USE FinDW
GO

IF OBJECT_ID('dbo.getFactID','FN') IS NOT NULL
BEGIN
	PRINT 'drop dbo.getFactID'
	DROP FUNCTION dbo.getFactID;
END 
GO

PRINT 'create dbo.getFactID'	
GO
CREATE FUNCTION dbo.getFactID (
	@CID bigint
	,@PeriodEndDateID int
	,@StatementID tinyint
	,@AccountID int
	,@SubAccountID int
) 
RETURNS numeric(20,0) 
WITH SCHEMABINDING
AS
BEGIN
	-- 8+1+2+2+5 = 18 (eg 2000 12 31 1 46 38 949111)
	RETURN CONCAT(ISNULL(@PeriodEndDateID, 0), ISNULL(@StatementID, 0), FORMAT(ISNULL(@AccountID, 0),'0#'), FORMAT(ISNULL(@SubAccountID, 0),'0#'), FORMAT(ISNULL(@CID, 0), '00000#'));
END
GO


USE FinDW
GO
	
--EXISTS (SELECT * FROM sys.objects WHERE name = 'dbo.StatmentLookup' and type = N'P') OR 
IF OBJECT_ID('usp_StatmentLookup','P') IS NOT NULL
BEGIN
	PRINT 'drop usp_StatmentLookup'
	DROP PROCEDURE dbo.usp_StatmentLookup
END	
GO

PRINT 'create usp_StatmentLookup'
GO

CREATE PROCEDURE dbo.usp_StatmentLookup 
AS
BEGIN
	-- convert Str columns in staging to table int lookup ID 
	UPDATE FinDW.staging.Statement SET CID = CAST(CIDStr AS bigint);

	UPDATE FinDW.staging.Statement SET PeriodEndDateID = dt_dim.DateID
		FROM dim.Date AS dt_dim
		WHERE dt_dim.mdy = PeriodEndDateStr

	UPDATE FinDW.staging.Statement SET FiscalQuarter = CAST(FiscalQuarterStr AS int);

	UPDATE FinDW.staging.Statement SET StatementID = CAST(StatementIDStr AS int);

	UPDATE FinDW.staging.Statement SET AccountID = ISNULL(acct_dim.AccountID, 0) 
		FROM dim.Account AS acct_dim
		WHERE acct_dim.AccountName = AccountStr

	UPDATE FinDW.staging.Statement SET SubAccountID = ISNULL(sub_dim.SubAccountID, 0) 
		FROM dim.SubAccount AS sub_dim
		WHERE sub_dim.SubAccountName = SubAccountStr

	UPDATE FinDW.staging.Statement SET Value = CAST(VALUEStr AS bigint);
END
GO

IF OBJECT_ID('usp_StatementFactSdaLoad','P') IS NOT NULL
BEGIN
	PRINT 'drop dbo.usp_StatementFactSdaLoad'
	DROP PROCEDURE dbo.usp_StatementFactSdaLoad
END	
GO

PRINT 'create usp_StatementFactSdaLoad'
GO
CREATE PROCEDURE dbo.usp_StatementFactSdaLoad
AS
BEGIN
	-- capture records that are merged (inserted or updated) into fact table and insert them into sda (as a back up)
	SET NOCOUNT ON;

	PRINT FORMATMESSAGE('EXECUTING: usp_StatementFactSdaLoad',CAST(@@ROWCOUNT AS varchar));

	INSERT INTO sda.dbo.Statement
	--DECLARE cur CURSOR FOR
	SELECT 
		import_path
		,import_date
		,download_date
		,CIDStr
		,PeriodEndDateStr
		,FiscalQuarterStr
		,StatementIDStr
		,AccountStr
		,SubAccountStr
		,ValueStr
	FROM (
		-- this nested merge statement populates fact table (FinDW.dbo.Statement) from staging table (FinDW.staging.Statement)
		MERGE FinDW.dbo.Statement AS target 
		USING (
		SELECT 
			import_path
			,import_date
			,download_date
			,CIDStr
			,PeriodEndDateStr
			,FiscalQuarterStr
			,StatementIDStr
			,AccountStr
			,SubAccountStr
			,ValueStr
			,CID
			,FiscalQuarter
			,PeriodEndDateID
			,StatementID
			,AccountID
			,SubAccountID
			,Value 
		FROM FinDW.staging.Statement) AS source (
			import_path
			,import_date
			,download_date
			,CIDStr
			,PeriodEndDateStr
			,FiscalQuarterStr
			,StatementIDStr
			,AccountStr
			,SubAccountStr
			,ValueStr
			,CID
			,FiscalQuarter
			,PeriodEndDateID
			,StatementID
			,AccountID
			,SubAccountID
			,Value)
				ON (dbo.getFactID(source.CID, source.PeriodEndDateID, source.StatementID, source.AccountID, source.SubAccountID) = target.FactID)
		-- if record already exists update value if different (almost never is different)
		WHEN MATCHED AND target.Value <> source.Value THEN UPDATE 
			SET Value = source.Value
		-- if record missing from fact then insert it (typical case)
		WHEN NOT MATCHED THEN INSERT (
			FactID
			,CID
			,FiscalQuarter
			,PeriodEndDateID
			,StatementID
			,AccountID
			,SubAccountID
			,Value)
			VALUES (
				dbo.getFactID(source.CID, source.PeriodEndDateID, source.StatementID, source.AccountID, source.SubAccountID)
				,source.CID
				,source.FiscalQuarter
				,source.PeriodEndDateID
				,source.StatementID
				,source.AccountID
				,source.SubAccountID
				,source.Value
			)
		-- capture records that participated in merge so they can inserted into sda
		OUTPUT $action, 
			source.import_path
			,source.import_date
			,source.download_date
			,source.CIDStr
			,source.PeriodEndDateStr
			,source.FiscalQuarterStr
			,source.StatementIDStr
			,source.AccountStr
			,source.SubAccountStr
			,source.ValueStr) AS new_records (
				Action 
				,import_path
				,import_date
				,download_date
				,CIDStr
				,PeriodEndDateStr
				,FiscalQuarterStr
				,StatementIDStr
				,AccountStr
				,SubAccountStr
				,ValueStr
		)
	WHERE Action = 'INSERT'
	OR Action = 'UPDATE';

	PRINT FORMATMESSAGE('number of new fact and sda rows: %s',CAST(@@ROWCOUNT AS varchar));
END
GO


--EXEC usp_StatmentLookup;
--EXEC usp_StatementFactSdaLoad;

