INSERT INTO Dim.Account (AccountID, AccountName)
SELECT 
	AccountStr
FROM (
	SELECT 
		DISTINCT AccountStr
	FROM Staging.Statement) sub; 


INSERT INTO Dim.SubAccount (SubAccountID, SubAccountName)
SELECT 
	SubAccountStr
FROM (
SELECT 
	DISTINCT SubAccountStr
FROM Staging.Statement) sub;

