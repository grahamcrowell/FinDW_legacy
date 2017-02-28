USE FinDW
GO
SET NOCOUNT ON;

BEGIN
	DECLARE @date date = DATEFROMPARTS(1995,1,1);
	DECLARE @enddate date = DATEFROMPARTS(2020,12,31);;
	DECLARE @dateid int = CAST(CONVERT(varchar(8),@date, 112) AS int);
	
	PRINT 'truncate dim.Date'
	TRUNCATE TABLE dim.Date;
	PRINT 'generate dim.Date'
	WHILE @date <= @enddate
	BEGIN
		SET @dateid = CAST(CONVERT(varchar(8),@date, 112) AS int);
		INSERT INTO dim.Date (DateID, Date) VALUES (@dateid, @date);
		SET @date = DATEADD(day,1,@date);
	END
END