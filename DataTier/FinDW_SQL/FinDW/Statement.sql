CREATE TABLE [Dim].[Statement]
(
	[StatementID] INT IDENTITY(0,1), 
    [StatementName] NVARCHAR(50) NULL, 
    CONSTRAINT [PK_Statement] PRIMARY KEY (StatementID)
)
