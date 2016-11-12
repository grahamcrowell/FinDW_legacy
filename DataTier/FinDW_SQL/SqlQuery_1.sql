:setvar DatabaseName "Staging"
:setvar DefaultFilePrefix "Staging"
:setvar DefaultDataPath "C:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\DATA\"
:setvar DefaultLogPath "C:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\DATA\"

GO

SELECT '$(DatabaseName)' AS DatebaseName;