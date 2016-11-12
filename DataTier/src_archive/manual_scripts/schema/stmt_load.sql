--DELETE sda.dbo.Statement;
--DELETE sda.dbo.Statement2;
--DELETE FinDW.dbo.Statement2;

	INSERT INTO sda.dbo.Statement2
	SELECT 
		[import_path]
		,[import_date]
		,[download_date]
		,[CIDStr]
		,[PeriodEndDateStr]
		,[FiscalQuarterStr]
		,[StatementIDStr]
		,[AccountStr]
		,[SubAccountStr]
		,[ValueStr]
	FROM (
		MERGE FinDW.dbo.Statement2 AS target 
		USING (
		SELECT 
			TOP 100
			--getFactID(CID, PeriodEndDateID, StatementID, AccountID, SubAccountID) AS FactID
			[import_path]
			,[import_date]
			,[download_date]
			,[CIDStr]
			,[PeriodEndDateStr]
			,[FiscalQuarterStr]
			,[StatementIDStr]
			,[AccountStr]
			,[SubAccountStr]
			,[ValueStr]
			,CID
			,FiscalQuarter
			,PeriodEndDateID
			,StatementID
			,AccountID
			,SubAccountID
			,Value 
		FROM FinDW.staging.[Statement]) AS source (
			--getFactID(CID, PeriodEndDateID, StatementID, AccountID, SubAccountID) AS FactID
			[import_path]
			,[import_date]
			,[download_date]
			,[CIDStr]
			,[PeriodEndDateStr]
			,[FiscalQuarterStr]
			,[StatementIDStr]
			,[AccountStr]
			,[SubAccountStr]
			,[ValueStr]
			,CID
			,FiscalQuarter
			,PeriodEndDateID
			,StatementID
			,AccountID
			,SubAccountID
			,Value)
				ON (dbo.getFactID(source.CID, source.PeriodEndDateID, source.StatementID, source.AccountID, source.SubAccountID) = target.FactID)
		WHEN MATCHED AND target.Value <> source.Value THEN UPDATE 
			SET Value = source.Value
		WHEN NOT MATCHED THEN INSERT (
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
			)
		OUTPUT $action, 
			source.[import_path]
			,source.[import_date]
			,source.[download_date]
			,source.[CIDStr]
			,source.[PeriodEndDateStr]
			,source.[FiscalQuarterStr]
			,source.[StatementIDStr]
			,source.[AccountStr]
			,source.[SubAccountStr]
			,source.[ValueStr]) AS Changes (Action, [import_path]
			,[import_date]
			,[download_date]
			,[CIDStr]
			,[PeriodEndDateStr]
			,[FiscalQuarterStr]
			,[StatementIDStr]
			,[AccountStr]
			,[SubAccountStr]
			,[ValueStr]);



SELECT *
FROM sda.dbo.Statement2;