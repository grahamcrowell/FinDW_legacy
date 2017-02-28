USE FinDW
GO

SELECT *
FROM sys.tables AS tab;

CREATE TABLE [dbo].[Statement]
(
    [import_path] NVARCHAR(500) NULL, 
    [CIDStr] NVARCHAR(50) NOT NULL, 
    [StatementIDStr] NVARCHAR(100) NOT NULL, 
    [download_date] NVARCHAR(12) NOT NULL,
	[FiscalQuarterStr] NVARCHAR(100) NOT NULL,
	[PeriodEndDateStr] NVARCHAR(120) NOT NULL,
	[AccountStr] NVARCHAR(20) NOT NULL,
	[SubAccountStr] NVARCHAR(20) NOT NULL,
	[ValueStr] NVARCHAR(500) NOT NULL
)
