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
--EXISTS (SELECT * FROM sys.objects WHERE name = '[dbo].[StatmentLookup]' and type = N'P') OR 
IF OBJECT_ID('sp_StatmentLookup','P') IS NOT NULL
BEGIN
	PRINT 'drop sp_StatmentLookup'
	DROP PROCEDURE [dbo].sp_StatmentLookup
END	
GO

PRINT 'create sp_StatmentLookup'
GO

CREATE PROCEDURE dbo.sp_StatmentLookup 
AS
BEGIN
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

IF OBJECT_ID('sp_StatementFactLoad','P') IS NOT NULL
BEGIN
	PRINT 'drop dbo.sp_StatementFactLoad'
	DROP PROCEDURE dbo.sp_StatementFactLoad
END	
GO

PRINT 'create sp_StatementFactLoad'
GO
CREATE PROCEDURE dbo.sp_StatementFactLoad
AS
BEGIN
	SET NOCOUNT ON;
	
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
		--source.FactID = ta;p0orget.FactID
		dbo.getFactID(source.CID, source.PeriodEndDateID, source.StatementID, source.AccountID, source.SubAccountID) = target.FactID
		--AND source.CID = target.CID
		--AND source.PeriodEndDateID = target.PeriodEndDateID
		--AND source.StatementID = target.StatementID
		--AND source.AccountID = target.AccountID
		--AND source.SubAccountID = target.SubAccountID
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

--EXEC sys.sp_refreshsqlmodule 'getFactID';
--IF OBJECTPROPERTY (OBJECT_ID(N'[dbo].[getFactID]'),'IsDeterministic') = 1
--   PRINT 'Function is detrministic.'
--ELSE IF OBJECTPROPERTY (OBJECT_ID(N'[dbo].[getFactID]'),'IsDeterministic') = 0
--   PRINT 'Function is NOT detrministic'
--GO

--SELECT dbo.getFactID(stg_stmt.CID, stg_stmt.PeriodEndDateID, stg_stmt.StatementID, stg_stmt.AccountID, stg_stmt.SubAccountID)
--FROM staging.Statement AS stg_stmt


EXEC sp_StatmentLookup;
--EXEC sp_StatementFactLoad;
