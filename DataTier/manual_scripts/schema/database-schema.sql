IF DB_ID('sda') IS NULL
BEGIN
	PRINT 'create database sda'
	EXEC sp_executesql N'CREATE DATABASE sda;'
END
GO

IF DB_ID('FinDW') IS NULL
BEGIN
	PRINT 'create database FinDW'
	EXEC sp_executesql N'CREATE DATABASE FinDW;'
END
GO

USE FinDW
GO

IF SCHEMA_ID('staging') IS NULL
BEGIN
	PRINT 'create schema staging'
	EXEC sp_executesql N'CREATE SCHEMA staging;'
END

IF SCHEMA_ID('dim') IS NULL
BEGIN
	PRINT 'create schema dim'
	EXEC sp_executesql N'CREATE SCHEMA dim;'
END

--IF SCHEMA_ID('fact') IS NULL
--BEGIN
--	PRINT 'create schema fact'
--	EXE sp_executesql N'CREATE SCHEMA fact;'
--END

