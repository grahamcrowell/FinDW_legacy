USE FinDW
GO

IF OBJECT_ID('dbo.FactID','FN') IS NOT NULL
BEGIN
	PRINT 'drop dbo.FactID'
	DROP FUNCTION dbo.FactID;
END 
GO

CREATE FUNCTION dbo.FactID (
	@CID bigint
	,@PeriodEndDateID int
	,@StatementID tinyint
	,@AccountID int
	,@SubAccountID int
) 
RETURNS bigint 
AS
BEGIN
	RETURN CONCAT(@CID, @PeriodEndDateID, @StatementID, FORMAT(@AccountID,'00#'), FORMAT(@SubAccountID,'00#'));
END