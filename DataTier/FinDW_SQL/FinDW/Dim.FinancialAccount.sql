CREATE TABLE [Dim].[FinancialAccount]
(
	[FinancialAccountID] INT IDENTITY(0,1), 
    [FinancialMainAccount_Str] NVARCHAR(100) NULL, 
    [FinancialSubAccount_Str] NVARCHAR(100) NULL, 
    CONSTRAINT [PK_FinancialStatement] PRIMARY KEY ([FinancialAccountID]) 
)

GO


CREATE INDEX [IX_FinancialAccount_Lkup] ON [Dim].[FinancialAccount] ([FinancialMainAccount_Str], [FinancialSubAccount_Str])
