# class ColumnType(Enum):
# 	SourceIdentifier = 1
# 	SourceDimLookup = 2 
# 	SourceFact = 3

class StagingColumn:
	_name = ''
	def __getattribute__(self, name):
		if name == 'ColumnType':
			return ColumnType.SourceIdentifier



# for stagingTable in stagingDatabase:
# 	for StagingColumn in stagingTable:
# 		columnType = stagingColumn.ColumnType
# 		if columnType == :
# 			ColumnType.SourceIdentifier:
# 				pass
# 			ColumnType.SourceDimLookup:
# 				pass
# 			ColumnType.SourceFact:
# 				pass

import re

column_name = 'Sub Account Key'

re_pattern = ''
