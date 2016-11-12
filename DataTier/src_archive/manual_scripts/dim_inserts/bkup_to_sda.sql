INSERT INTO SourceDataArchive.Statement 
([import_file],
[FiscalQuarterStr],
[PeriodEndDateStr],
[AccountStr],
[SubAccountStr],
[ValueStr])
SELECT 
	[import_file],
	[FiscalQuarterStr],
	[PeriodEndDateStr],
	[AccountStr],
	[SubAccountStr],
	[ValueStr]
FROM Staging.Statement;