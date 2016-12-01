USE [master]
RESTORE DATABASE [WideWorldImportersDW] FROM  DISK = N'C:\SQLbackups\WideWorldImportersDW-Full.bak' WITH  FILE = 1,  MOVE N'WWI_Primary' TO N'C:\SQL_Data\WideWorldImportersDW.mdf',  
MOVE N'WWI_UserData' TO N'C:\SQL_Data\WideWorldImportersDW_UserData.ndf',  MOVE N'WWI_Log' TO N'C:\SQL_Logs\SQL2016\WideWorldImportersDW.ldf', 
MOVE N'WWIDW_InMemory_Data_1' TO N'C:\SQL_Data\WideWorldImportersDW_InMemory_Data_1',  NOUNLOAD,  REPLACE,  STATS = 5
GO