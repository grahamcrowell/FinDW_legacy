CREATE TABLE [Dim].[Account]
(
	AccountID int IDENTITY(0,1), 
    [AccountName] NVARCHAR(50) NOT NULL, 
    CONSTRAINT [PK_Account] PRIMARY KEY (AccountID)

)

GO
