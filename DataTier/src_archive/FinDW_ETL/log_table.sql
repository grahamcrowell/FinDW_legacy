drop table log;

create table log (
	log_message nvarchar(max)
	,log_date date DEFAULT NULL
);
GO

CREATE TRIGGER log_date ON log 
AFTER INSERT
AS 
UPDATE log 
SET log_date = GETDATE()
FROM log 
WHERE log.log_date IS NULL;
GO

INSERT INTO log (log_message)
VALUES ('c:/asdf/sdfs/');

SELECT * FROM log;

