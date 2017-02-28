CREATE VIEW [Etl].[FinancialStatement]
AS 
SELECT 
	stmt.CIDStr AS NasdaqCid_Key
	,stmt.AccountStr AS Account_Lkup
	,stmt.SubAccountStr AS SubAccount_Lkup
	,stmt.FiscalQuarterStr AS FiscalQuarter_Int
	,stmt.PeriodEndDateStr AS PeriodEndDate_Lkup
	,stmt.ValueStr AS Value_Int
FROM dbo.Statement AS stmt
